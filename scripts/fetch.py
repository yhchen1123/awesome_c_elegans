#!/usr/bin/env python3
"""Fetch candidate papers from Europe PMC and arXiv.

Usage:
    python3 scripts/fetch.py --out build/candidates_raw.json --report build/fetch_report.json
    python3 scripts/fetch.py --window-days 30 ...   # widen window for smoke tests

Outputs:
    --out:    candidates_raw.json — flat list of candidates, each with matched_queries
    --report: fetch_report.json   — per-query result counts and failed_sources

Fault tolerance: a failing source (timeout / HTTP error / rate limit) is logged to
failed_sources and the run continues; the script exits non-zero only if ALL sources fail.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent

ATOM_NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def user_agent():
    email = os.environ.get("EPMC_EMAIL", "").strip() or "unset@example.org"
    return f"awesome_c_elegans/0.1 (mailto:{email})"


def http_get(url, params=None, retries=3, timeout=60):
    """GET with retry/backoff on 5xx and transient errors.

    Falls back to the system curl binary on HTTP 406: export.arxiv.org
    TLS-fingerprint-blocks Python HTTP stacks (requests/urllib3 get 406 while
    curl succeeds with identical URL and headers). curl is available by default
    on macOS, Linux and GitHub Actions runners.
    """
    last_err = None
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers={"User-Agent": user_agent()}, timeout=timeout)
            if r.status_code == 406 and shutil.which("curl"):
                return _curl_get(url, params, timeout)
            if r.status_code >= 500:
                raise requests.HTTPError(f"{r.status_code} server error")
            r.raise_for_status()
            return r.text
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(2 ** (attempt + 1))
    raise RuntimeError(f"GET {url} failed after {retries} attempts: {last_err}")


def _curl_get(url, params, timeout):
    from urllib.parse import urlencode
    full = f"{url}?{urlencode(params)}" if params else url
    out = subprocess.run(
        ["curl", "-sL", "-m", str(timeout), "-A", user_agent(), full],
        capture_output=True, text=True, timeout=timeout + 10,
    )
    if out.returncode != 0:
        raise RuntimeError(f"curl exited {out.returncode}: {out.stderr.strip()}")
    return out.stdout


def compute_window(window_days, today=None):
    today = today or datetime.date.today()
    return today - datetime.timedelta(days=window_days), today


def fetch_epmc(cfg, from_date, to_date, report):
    """Europe PMC: paginate each configured query until exhausted."""
    base = cfg["europe_pmc"]["base"]
    page_size = int(cfg["europe_pmc"].get("page_size", 100))
    candidates = []
    for qname, qcfg in cfg["europe_pmc"]["queries"].items():
        query = qcfg["query"].format(from_date=from_date.isoformat(), to_date=to_date.isoformat())
        hint = qcfg.get("categories_hint", [])
        cursor = "*"
        fetched = 0
        try:
            while True:
                text = http_get(
                    base,
                    params={"query": query, "format": "json", "pageSize": page_size,
                            "resultType": "core", "cursorMark": cursor},
                )
                payload = json.loads(text)
                results = payload.get("resultList", {}).get("result", [])
                for it in results:
                    doi = (it.get("doi") or "").strip()
                    src = it.get("source", "")
                    rec = {
                        "id": doi or f"{src}:{it.get('id', '')}",
                        "doi": doi or None,
                        "title": (it.get("title") or "").strip(),
                        "authors": [a.strip() for a in (it.get("authorString") or "").split(",") if a.strip()],
                        "venue": (it.get("journalTitle") or ("bioRxiv/medRxiv" if src == "PPR" else "")).strip(),
                        "year": int(it["pubYear"]) if str(it.get("pubYear", "")).isdigit() else None,
                        "abstract": it.get("abstractText") or "",
                        "first_publication_date": it.get("firstPublicationDate"),
                        "src": src,
                        "url": f"https://doi.org/{doi}" if doi else f"https://europepmc.org/article/{src}/{it.get('id', '')}",
                        "matched_queries": [qname],
                        "categories_hint": hint,
                        "fetch_source": "epmc",
                    }
                    candidates.append(rec)
                fetched += len(results)
                next_cursor = payload.get("nextCursorMark")
                if not results or not next_cursor or next_cursor == cursor:
                    break
                cursor = next_cursor
                time.sleep(1.0)  # EPMC courtesy delay between pages
            report["queries"][f"epmc:{qname}"] = {"results": fetched, "status": "ok"}
        except Exception as e:  # noqa: BLE001 - fault tolerance per spec
            report["queries"][f"epmc:{qname}"] = {"results": fetched, "status": f"failed: {e}"}
            report["failed_sources"].append(f"epmc:{qname}: {e}")
    return candidates


def fetch_arxiv(cfg, from_date, to_date, report):
    """arXiv Atom API: one request per query, filter by published date window."""
    base = cfg["arxiv"]["base"]
    max_results = int(cfg["arxiv"].get("max_results", 200))
    candidates = []
    for qname, qcfg in cfg["arxiv"]["queries"].items():
        hint = qcfg.get("categories_hint", [])
        fetched = 0
        try:
            text = http_get(
                base,
                params={"search_query": qcfg["query"], "sortBy": "submittedDate",
                        "sortOrder": "descending", "max_results": max_results},
            )
            root = ET.fromstring(text)
            for entry in root.findall("a:entry", ATOM_NS):
                published = (entry.findtext("a:published", "", ATOM_NS) or "")[:10]
                try:
                    pub_date = datetime.date.fromisoformat(published)
                except ValueError:
                    continue
                if not (from_date <= pub_date <= to_date):
                    continue
                raw_id = (entry.findtext("a:id", "", ATOM_NS) or "").strip()
                arxiv_id = raw_id.rsplit("/abs/", 1)[-1]
                base_id = arxiv_id.rsplit("v", 1)[0] if "v" in arxiv_id else arxiv_id
                cats = [c.attrib.get("term", "") for c in entry.findall("a:category", ATOM_NS)]
                candidates.append({
                    "id": base_id,
                    "arxiv_id": base_id,
                    "doi": None,
                    "title": " ".join((entry.findtext("a:title", "", ATOM_NS) or "").split()),
                    "authors": [a.findtext("a:name", "", ATOM_NS) for a in entry.findall("a:author", ATOM_NS)],
                    "venue": "arXiv",
                    "year": pub_date.year,
                    "abstract": " ".join((entry.findtext("a:summary", "", ATOM_NS) or "").split()),
                    "first_publication_date": published,
                    "src": "ARXIV",
                    "arxiv_categories": cats,
                    "url": f"https://arxiv.org/abs/{base_id}",
                    "matched_queries": [qname],
                    "categories_hint": hint,
                    "fetch_source": "arxiv",
                })
                fetched += 1
            report["queries"][f"arxiv:{qname}"] = {"results": fetched, "status": "ok"}
            time.sleep(3)  # arXiv API courtesy delay
        except Exception as e:  # noqa: BLE001
            report["queries"][f"arxiv:{qname}"] = {"results": fetched, "status": f"failed: {e}"}
            report["failed_sources"].append(f"arxiv:{qname}: {e}")
    return candidates


def merge_matched_queries(candidates):
    """Merge duplicates within the candidate batch, unioning matched_queries."""
    merged = {}
    for c in candidates:
        key = (c.get("doi") or c["id"]).lower()
        if key in merged:
            prev = merged[key]
            prev["matched_queries"] = sorted(set(prev["matched_queries"]) | set(c["matched_queries"]))
            prev["categories_hint"] = sorted(set(prev.get("categories_hint", [])) | set(c.get("categories_hint", [])))
        else:
            merged[key] = c
    return list(merged.values())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="build/candidates_raw.json")
    ap.add_argument("--report", default="build/fetch_report.json")
    ap.add_argument("--window-days", type=int, default=None, help="override config window_days")
    ap.add_argument("--only-category", default=None, metavar="C0-C9",
                    help="只运行 categories_hint 覆盖该分类的查询（工作日轮询模式）")
    args = ap.parse_args()

    with open(ROOT / "config" / "queries.yaml", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if args.only_category:
        cat = args.only_category
        for source in ("europe_pmc", "arxiv"):
            qs = cfg[source]["queries"]
            cfg[source]["queries"] = {
                name: q for name, q in qs.items() if cat in (q.get("categories_hint") or [])
            }
        n = sum(len(cfg[s]["queries"]) for s in ("europe_pmc", "arxiv"))
        print(f"category filter {cat}: {n} queries selected")
        if n == 0:
            print(f"warning: no query covers {cat}（可在 queries.yaml 补充该分类的检索式）", file=sys.stderr)
    window_days = args.window_days or int(cfg.get("window_days", 10))
    from_date, to_date = compute_window(window_days)
    print(f"fetch window: {from_date} .. {to_date} ({window_days} days)")

    report = {
        "window": {"from": from_date.isoformat(), "to": to_date.isoformat()},
        "queries": {},
        "failed_sources": [],
    }

    candidates = fetch_epmc(cfg, from_date, to_date, report)
    candidates += fetch_arxiv(cfg, from_date, to_date, report)
    candidates = merge_matched_queries(candidates)

    report["total_candidates"] = len(candidates)

    out_path = ROOT / args.out
    report_path = ROOT / args.report
    out_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(candidates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for q, info in report["queries"].items():
        print(f"  {q}: {info['results']} results ({info['status']})")
    print(f"total unique candidates: {len(candidates)}")

    n_queries = len(report["queries"])
    if n_queries > 0 and len(report["failed_sources"]) >= n_queries:
        print("ALL sources failed — exiting non-zero.", file=sys.stderr)
        sys.exit(1)
    if report["failed_sources"]:
        print(f"warning: {len(report['failed_sources'])} source(s) failed (see report).", file=sys.stderr)


if __name__ == "__main__":
    main()
