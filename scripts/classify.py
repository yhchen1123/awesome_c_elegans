#!/usr/bin/env python3
"""Classify candidate papers with an OpenAI-compatible LLM.

Modes:
    weekly pipeline:  python3 scripts/classify.py --in build/candidates_new.json --db data/papers.json
    reclassify:       python3 scripts/classify.py --reclassify --since YYYY-MM-DD [--include-manual]
    manual add:       python3 scripts/classify.py --add <DOI> [--yes]

Anti-hallucination rules (hard requirements):
  * Title, authors, year, DOI, URL come ONLY from the fetch-stage API metadata.
    The LLM never generates bibliographic fields.
  * The LLM output `id` must exactly match an input candidate id, otherwise the
    entry is discarded and logged.

Output validation (any failure → entry discarded + logged):
  1. output parses as JSON
  2. id exactly equals the input id
  3. categories / tier / evidence / standards values within taxonomy enums
  4. relevance_note non-empty and contains Chinese characters
  confidence < 0.6 → needs_review: true (still accepted, pinned atop the PR body)
  confidence < --min-confidence (default 0.4) → discarded

Also writes build/pr_body.md (new-entry count, per-category distribution,
needs_review list on top, failed-source warnings, C7 share). The script is
idempotent: with no accepted entries, papers.json is untouched and the
create-pull-request action finds no diff (no empty PR).
"""
import argparse
import datetime
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent

SYSTEM_PROMPT = """You are a curator for awesome_c_elegans, a literature intelligence repository tracking C. elegans embryogenesis research across measurement & imaging, developmental dynamics, morphology & mechanics, molecular regulation, perturbation experiments, and transferable computational methods.

You will receive a paper's title, abstract, and candidate category hints. Return a JSON object with EXACTLY these fields:
- "id": the input id, copied verbatim
- "categories": array of 1-3 codes from [C0 measurement/tracking, C1 representation learning, C2 WT dynamics/variability, C3 morphology/mechanics/force inference/simulators, C4 molecular regulation (scRNA/TF/signaling/RNA-protein), C5 perturbation & causal inference, C6 fate specification & lineage biology, C7 methods transfer (non-elegans but transferable), C8 datasets/benchmarks/software, C9 reviews]
- "tags": subset of modality tags [imaging, scRNA, protein-reporter, morphology-3D, mechanics, lineage, perturbation, theory-model] plus species tags [c-elegans, c-briggsae, other-species]
- "tier": "T1-core" (directly about C. elegans embryogenesis) / "T2-adjacent" (other worm stages or directly relevant general methods) / "T3-transfer" (other species or pure methodology with clear transfer value)
- "evidence": "peer-reviewed" if journal-published, "preprint" if bioRxiv/medRxiv/arXiv only
- "standards": subset of [embryo-level-split, open-loop-rollout, uncertainty-quantified, perturbation-holdout, shortcut-audit] — only when the abstract explicitly indicates it; otherwise []
- "relevance_note": 1-2 sentences IN CHINESE, explaining: which research area it belongs to; what it contributes (new method/dataset/benchmark/finding). Never invent results not in the abstract.
- "confidence": 0.0-1.0
Return ONLY the JSON object."""

VALID_TIERS = {"T1-core", "T2-adjacent", "T3-transfer"}
VALID_EVIDENCE = {"peer-reviewed", "preprint", "emerging-evidence"}
VALID_STANDARDS = {"embryo-level-split", "open-loop-rollout", "uncertainty-quantified",
                   "perturbation-holdout", "shortcut-audit"}
PREPRINT_SOURCES = {"PPR", "ARXIV"}


def load_taxonomy():
    with open(ROOT / "config" / "taxonomy.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def has_cjk(s):
    return bool(re.search(r"[\u4e00-\u9fff]", s or ""))


# ---------------------------------------------------------------- LLM client

def llm_config():
    return {
        "api_key": os.environ.get("LLM_API_KEY", "").strip(),
        "base_url": os.environ.get("LLM_BASE_URL", "").strip() or "https://api.moonshot.cn/v1",
        "model": os.environ.get("LLM_MODEL", "").strip() or "kimi-k2-0905-preview",
    }


def llm_chat(messages, cfg, retries=2):
    """One chat-completion call with exponential backoff; falls back to plain
    prompt-constrained JSON if the endpoint rejects response_format."""
    url = f"{cfg['base_url'].rstrip('/')}/chat/completions"
    payload = {
        "model": cfg["model"],
        "temperature": 0,
        "messages": messages,
        "response_format": {"type": "json_object"},
    }
    last_err = None
    for attempt in range(retries + 1):
        try:
            r = requests.post(
                url,
                headers={"Authorization": f"Bearer {cfg['api_key']}",
                         "Content-Type": "application/json"},
                json=payload,
                timeout=180,
            )
            if r.status_code == 400 and "response_format" in payload:
                # endpoint does not support json_object mode → degrade gracefully
                payload.pop("response_format")
                continue
            if r.status_code >= 500 or r.status_code == 429:
                raise requests.HTTPError(f"{r.status_code}: {r.text[:200]}")
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:  # noqa: BLE001
            last_err = e
            if attempt < retries:
                time.sleep(2 ** (attempt + 1))
    raise RuntimeError(f"LLM call failed after {retries + 1} attempts: {last_err}")


def parse_json_strict(text):
    """Strict JSON extraction: raw parse, then fenced-block strip, then first
    {...} span. Raises ValueError on failure."""
    text = (text or "").strip()
    if not text:
        raise ValueError("empty LLM response")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if m:
        return json.loads(m.group(1))
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        return json.loads(m.group(0))
    raise ValueError("no JSON object found in LLM response")


# ---------------------------------------------------------------- validation

def validate_llm_output(obj, cand_id, tax):
    """Return list of validation errors (empty = valid)."""
    errors = []
    if not isinstance(obj, dict):
        return ["output is not a JSON object"]
    if obj.get("id") != cand_id:
        errors.append(f"id mismatch: got {obj.get('id')!r}, expected {cand_id!r}")
        return errors  # id mismatch is fatal; further checks meaningless
    valid_cats = set(tax["categories"].keys())
    cats = obj.get("categories")
    if not isinstance(cats, list) or not (1 <= len(cats) <= 3) or not set(cats) <= valid_cats:
        errors.append(f"categories invalid: {cats!r}")
    valid_tags = set(tax.get("modality_tags", [])) | set(tax.get("species_tags", []))
    tags = obj.get("tags", [])
    if not isinstance(tags, list) or not set(tags) <= valid_tags:
        errors.append(f"tags invalid: {tags!r}")
    if obj.get("tier") not in VALID_TIERS:
        errors.append(f"tier invalid: {obj.get('tier')!r}")
    if obj.get("evidence") not in VALID_EVIDENCE:
        errors.append(f"evidence invalid: {obj.get('evidence')!r}")
    stds = obj.get("standards", [])
    if not isinstance(stds, list) or not set(stds) <= VALID_STANDARDS:
        errors.append(f"standards invalid: {stds!r}")
    note = obj.get("relevance_note", "")
    if not isinstance(note, str) or not note.strip() or not has_cjk(note):
        errors.append("relevance_note empty or lacks Chinese characters")
    conf = obj.get("confidence")
    if not isinstance(conf, (int, float)) or not (0.0 <= conf <= 1.0):
        errors.append(f"confidence invalid: {conf!r}")
    return errors


def classify_candidate(cand, cfg, tax):
    """Return (llm_output, None) or (None, error_string)."""
    hints = ", ".join(cand.get("categories_hint") or []) or "(none)"
    user = (
        f"id: {cand['id']}\n"
        f"matched category hints: {hints}\n"
        f"venue: {cand.get('venue', '')} (year {cand.get('year', '')}, source {cand.get('src', '')})\n"
        f"title: {cand.get('title', '')}\n"
        f"abstract: {(cand.get('abstract') or '')[:4000]}"
    )
    raw = llm_chat(
        [{"role": "system", "content": SYSTEM_PROMPT},
         {"role": "user", "content": user}],
        cfg,
    )
    try:
        obj = parse_json_strict(raw)
    except ValueError as e:
        return None, f"unparseable JSON: {e}"
    errors = validate_llm_output(obj, cand["id"], tax)
    if errors:
        return None, "; ".join(errors)
    return obj, None


def build_entry(cand, out):
    """Merge LLM fields with fetch-stage metadata (bibliographic fields NEVER
    come from the LLM)."""
    evidence = out["evidence"]
    if cand.get("src") in PREPRINT_SOURCES and evidence == "peer-reviewed":
        evidence = "preprint"  # preprint sources cannot assert peer review
    conf = float(out["confidence"])
    entry = {
        "id": cand["id"],
        "title": cand.get("title", "").strip(),
        "authors": cand.get("authors", []),
        "venue": cand.get("venue", "").strip() or ("arXiv" if cand.get("src") == "ARXIV" else ""),
        "year": int(cand["year"]) if cand.get("year") else datetime.date.today().year,
        "categories": out["categories"],
        "tags": out.get("tags", []),
        "tier": out["tier"],
        "evidence": evidence,
        "standards": out.get("standards", []),
        "relevance_note": out["relevance_note"].strip(),
        "url": cand.get("url") or (f"https://doi.org/{cand['doi']}" if cand.get("doi") else ""),
        "confidence": round(conf, 3),
        "needs_review": conf < 0.6,
        "added": datetime.date.today().isoformat(),
        "source": cand.get("fetch_source", "epmc"),
    }
    if cand.get("doi"):
        entry["doi"] = cand["doi"]
    if cand.get("arxiv_id"):
        entry["arxiv_id"] = cand["arxiv_id"]
    return entry


# ---------------------------------------------------------------- PR body

def c7_share(db):
    c7 = [p for p in db if "C7" in p.get("categories", [])]
    t3 = [p for p in c7 if p.get("tier") == "T3-transfer"]
    return (len(t3) / len(c7)) if c7 else 0.0, len(c7), len(t3)


def write_pr_body(path, accepted, discarded, unclassified, db, fetch_report_path=None):
    lines = ["## 📚 Automated literature update", ""]
    lines.append(f"**New entries: {len(accepted)}** "
                 f"(discarded by validation: {len(discarded)}, "
                 f"unclassified after retries: {len(unclassified)})")
    lines.append("")
    review = [e for e in accepted if e.get("needs_review")]
    if review:
        lines.append(f"### ⚠️ Needs review ({len(review)}) — low-confidence classifications")
        lines.append("")
        for e in review:
            lines.append(f"- **{e['title']}** (`{e['id']}`) — confidence {e['confidence']}, "
                         f"categories {', '.join(e['categories'])}")
        lines.append("")
    if accepted:
        dist = {}
        for e in accepted:
            for c in e["categories"]:
                dist[c] = dist.get(c, 0) + 1
        lines.append("### Category distribution")
        lines.append("")
        for c in sorted(dist):
            lines.append(f"- {c}: {dist[c]}")
        lines.append("")
        lines.append("### New entries")
        lines.append("")
        for e in accepted:
            lines.append(f"- {e['title']} (`{e['id']}`) — {', '.join(e['categories'])}, "
                         f"{e['tier']}, {e['evidence']}, confidence {e['confidence']}")
        lines.append("")
    if unclassified:
        lines.append("### 🗂️ Unclassified staging (LLM failed after retries)")
        lines.append("")
        for c in unclassified:
            lines.append(f"- {c.get('title', c.get('id'))} (`{c.get('id')}`)")
        lines.append("")
    if discarded:
        lines.append("### 🗑️ Discarded by output validation (see classify_log.json)")
        lines.append("")
        for d in discarded:
            lines.append(f"- `{d['id']}` — {d['reason']}")
        lines.append("")
    if fetch_report_path and Path(fetch_report_path).exists():
        rep = json.loads(Path(fetch_report_path).read_text(encoding="utf-8"))
        failed = rep.get("failed_sources", [])
        if failed:
            lines.append("### ⚠️ Fetch warnings (failed sources)")
            lines.append("")
            for f in failed:
                lines.append(f"- {f}")
            lines.append("")
    share, n, t3 = c7_share(db)
    flag = " ⚠️ **over the 30% soft cap**" if share > 0.30 else ""
    lines.append(f"C7 T3-transfer share: {share:.0%} ({t3}/{n}){flag}")
    lines.append("")
    lines.append("---")
    lines.append("*Generated by scripts/classify.py. Nothing is merged without human review.*")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------- modes

def mode_pipeline(args, tax, cfg):
    cand_path = ROOT / args.inp
    db_path = ROOT / args.db
    candidates = json.loads(cand_path.read_text(encoding="utf-8")) if cand_path.exists() else []
    db = json.loads(db_path.read_text(encoding="utf-8"))

    if not candidates:
        print("no candidates — nothing to classify (idempotent no-op).")
        write_pr_body(ROOT / "build" / "pr_body.md", [], [], [], db,
                      ROOT / "build" / "fetch_report.json")
        return 0

    if not cfg["api_key"]:
        print("LLM_API_KEY is required for classification (set it in repo secrets).", file=sys.stderr)
        return 2

    accepted, discarded, unclassified = [], [], []
    for i, cand in enumerate(candidates, 1):
        print(f"[{i}/{len(candidates)}] {cand['id']}: {cand.get('title', '')[:70]}", flush=True)
        try:
            out, err = classify_candidate(cand, cfg, tax)
        except Exception as e:  # noqa: BLE001 - LLM call failed after retries
            print(f"    unclassified: {e}", flush=True)
            unclassified.append(cand)
            continue
        if err:
            print(f"    discarded: {err}", flush=True)
            discarded.append({"id": cand["id"], "title": cand.get("title"), "reason": err})
            continue
        if float(out["confidence"]) < args.min_confidence:
            discarded.append({"id": cand["id"], "title": cand.get("title"),
                              "reason": f"confidence {out['confidence']} < {args.min_confidence}"})
            print(f"    discarded: confidence too low ({out['confidence']})", flush=True)
            continue
        entry = build_entry(cand, out)
        accepted.append(entry)
        print(f"    ok: {entry['categories']} {entry['tier']} conf={entry['confidence']}", flush=True)

    if accepted:
        db.extend(accepted)
        db_path.write_text(json.dumps(db, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"appended {len(accepted)} entries to {args.db}")
    else:
        print("no entries accepted — database untouched.")

    log = {
        "run_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "model": cfg["model"],
        "accepted": [e["id"] for e in accepted],
        "discarded": discarded,
        "unclassified": [c.get("id") for c in unclassified],
    }
    log_path = ROOT / "build" / "classify_log.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if unclassified:
        (ROOT / "build" / "unclassified.json").write_text(
            json.dumps(unclassified, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_pr_body(ROOT / "build" / "pr_body.md", accepted, discarded, unclassified, db,
                  ROOT / "build" / "fetch_report.json")
    return 0


def fetch_abstract_for_doi(doi):
    """Best-effort abstract lookup for reclassify / add modes."""
    try:
        r = requests.get(
            "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
            params={"query": f'DOI:"{doi}"', "format": "json", "resultType": "core"},
            timeout=30)
        if r.status_code == 200:
            results = r.json().get("resultList", {}).get("result", [])
            if results:
                return results[0].get("abstractText") or ""
    except Exception:  # noqa: BLE001
        pass
    return ""


def mode_reclassify(args, tax, cfg):
    if not cfg["api_key"]:
        print("LLM_API_KEY is required for reclassification.", file=sys.stderr)
        return 2
    db_path = ROOT / args.db
    db = json.loads(db_path.read_text(encoding="utf-8"))
    since = args.since
    changed = []
    for p in db:
        if p.get("added", "") < since:
            continue
        if p.get("source") == "manual" and not args.include_manual:
            continue
        cand = {
            "id": p["id"], "title": p["title"], "authors": p.get("authors", []),
            "venue": p.get("venue", ""), "year": p.get("year"), "src": "",
            "abstract": fetch_abstract_for_doi(p.get("doi", "")) if p.get("doi") else "",
            "categories_hint": p.get("categories", []), "fetch_source": p.get("source", "epmc"),
        }
        out, err = classify_candidate(cand, cfg, tax)
        if err:
            print(f"  reclassify failed for {p['id']}: {err} (entry kept as-is)")
            continue
        for field in ("categories", "tags", "tier", "evidence", "standards", "relevance_note"):
            p[field] = out[field] if field != "relevance_note" else out[field].strip()
        p["confidence"] = round(float(out["confidence"]), 3)
        p["needs_review"] = p["confidence"] < 0.6
        changed.append(p["id"])
        print(f"  reclassified {p['id']} -> {p['categories']} (conf {p['confidence']})")
    if changed:
        db_path.write_text(json.dumps(db, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"reclassified {len(changed)} entries since {since}.")
    return 0


def mode_add(args, tax, cfg):
    doi = args.add.strip()
    r = requests.get(f"https://api.crossref.org/works/{doi}", timeout=30)
    if r.status_code != 200:
        print(f"CrossRef lookup failed for {doi}: HTTP {r.status_code}", file=sys.stderr)
        return 1
    m = r.json()["message"]
    authors = [" ".join(x for x in [a.get("given", ""), a.get("family", "")] if x).strip()
               for a in m.get("author", [])]
    year = None
    for k in ("published-print", "published-online", "issued", "created"):
        if m.get(k, {}).get("date-parts"):
            year = m[k]["date-parts"][0][0]
            break
    venue = re.sub(r"<[^>]+>", "", (m.get("container-title") or [""])[0]).strip()
    if not venue:
        venue = "bioRxiv" if doi.startswith("10.1101/") else (m.get("publisher") or "")
    cand = {
        "id": doi, "doi": doi,
        "title": re.sub(r"<[^>]+>", "", (m.get("title") or [""])[0]).strip(),
        "authors": authors, "venue": venue, "year": year,
        "abstract": m.get("abstract") or fetch_abstract_for_doi(doi),
        "src": "PPR" if doi.startswith("10.1101/") else "MED",
        "url": f"https://doi.org/{doi}",
        "categories_hint": [], "fetch_source": "manual",
    }
    print(f"fetched: {cand['title']} ({venue} {year})")
    if not cfg["api_key"]:
        print("LLM_API_KEY not set — cannot classify. Aborting without changes.", file=sys.stderr)
        return 2
    out, err = classify_candidate(cand, cfg, tax)
    if err:
        print(f"classification failed validation: {err}", file=sys.stderr)
        return 1
    entry = build_entry(cand, out)
    entry["source"] = "manual"
    print(json.dumps(entry, indent=2, ensure_ascii=False))
    if not args.yes:
        answer = input("Add this entry to data/papers.json? [y/N] ").strip().lower()
        if answer != "y":
            print("aborted; no changes made.")
            return 0
    db_path = ROOT / args.db
    db = json.loads(db_path.read_text(encoding="utf-8"))
    if any(p["id"].lower() == entry["id"].lower() for p in db):
        print("entry already exists in database; no changes made.")
        return 0
    db.append(entry)
    db_path.write_text(json.dumps(db, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"added {entry['id']}. Now run: python3 scripts/render.py && python3 scripts/validate.py")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="inp", default="build/candidates_new.json")
    ap.add_argument("--db", default="data/papers.json")
    ap.add_argument("--min-confidence", type=float, default=0.4,
                    help="discard LLM classifications below this confidence (default 0.4)")
    ap.add_argument("--reclassify", action="store_true",
                    help="re-run classification for DB entries added since --since")
    ap.add_argument("--since", default="1970-01-01", help="YYYY-MM-DD cutoff for --reclassify")
    ap.add_argument("--include-manual", action="store_true",
                    help="also reclassify manually curated entries")
    ap.add_argument("--add", metavar="DOI", help="fetch metadata, classify, confirm, add one paper")
    ap.add_argument("--yes", action="store_true", help="skip interactive confirmation for --add")
    args = ap.parse_args()

    tax = load_taxonomy()
    cfg = llm_config()

    if args.add:
        sys.exit(mode_add(args, tax, cfg))
    if args.reclassify:
        sys.exit(mode_reclassify(args, tax, cfg))
    sys.exit(mode_pipeline(args, tax, cfg))


if __name__ == "__main__":
    main()
