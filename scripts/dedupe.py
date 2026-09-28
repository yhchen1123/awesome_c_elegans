#!/usr/bin/env python3
"""Dedupe fetched candidates against the existing database.

Usage:
    python3 scripts/dedupe.py --in build/candidates_raw.json --db data/papers.json --out build/candidates_new.json

Three-level dedupe, in order:
  1. DOI exact match (lowercase-normalized)
  2. arXiv / bioRxiv ID match
  3. Title fingerprint (lowercase, punctuation stripped, whitespace collapsed,
     trailing version suffix v\\d+ removed)

Also merges bioRxiv preprints into their published versions via CrossRef
relation.is-preprint-of when the published version is already in the database
(keeps preprint_id, upgrades evidence to peer-reviewed — recorded in the output
as "_merged_into" actions in the report, not written into the DB here).

Candidates colliding with an existing DB id are dropped: DB entries are
human-maintained and API metadata must not overwrite human fields.
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent


def norm_doi(doi):
    return (doi or "").strip().lower()


def biorxiv_id(doi):
    """Extract the bioRxiv/medRxiv identifier part from a 10.1101 DOI."""
    m = re.match(r"^10\.1101/(.+)$", norm_doi(doi))
    return m.group(1) if m else None


def arxiv_base(arxiv_id):
    if not arxiv_id:
        return None
    return re.sub(r"v\d+$", "", arxiv_id.strip())


def title_fingerprint(title):
    t = (title or "").lower()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+v\d+$", "", t)          # trailing version number
    t = re.sub(r"\s+", " ", t).strip()
    return t


def db_indexes(db):
    by_doi, by_preprint, by_arxiv, by_title = {}, {}, {}, {}
    for p in db:
        d = norm_doi(p.get("doi") or (p["id"] if p["id"].startswith("10.") else ""))
        if d:
            by_doi[d] = p
            bp = biorxiv_id(d)
            if bp:
                by_preprint[bp] = p
        if p.get("preprint_id"):
            by_preprint[biorxiv_id(p["preprint_id"]) or norm_doi(p["preprint_id"])] = p
        ax = arxiv_base(p.get("arxiv_id") or (p["id"] if not p["id"].startswith(("10.", "manual:")) else ""))
        if ax:
            by_arxiv[ax] = p
        fp = title_fingerprint(p.get("title"))
        if fp:
            by_title[fp] = p
    return by_doi, by_preprint, by_arxiv, by_title


def crossref_published_doi(preprint_doi, crossref_base):
    """Return the published-version DOI via CrossRef relation.is-preprint-of, if any."""
    try:
        r = requests.get(f"{crossref_base}/{preprint_doi}",
                         headers={"User-Agent": user_agent()}, timeout=30)
        if r.status_code != 200:
            return None
        relations = r.json().get("message", {}).get("relation", {})
        for rel in relations.get("is-preprint-of", []):
            if rel.get("id-type") == "doi":
                return norm_doi(rel.get("id"))
    except Exception as e:  # noqa: BLE001 - network faults must not break dedupe
        print(f"  warning: CrossRef relation lookup failed for {preprint_doi}: {e}", file=sys.stderr)
    return None


def user_agent():
    email = os.environ.get("EPMC_EMAIL", "").strip() or "unset@example.org"
    return f"awesome_c_elegans/0.1 (mailto:{email})"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--db", default="data/papers.json")
    ap.add_argument("--out", default="build/candidates_new.json")
    ap.add_argument("--report", default=None, help="optional dedupe report path")
    args = ap.parse_args()

    with open(ROOT / args.inp, encoding="utf-8") as f:
        candidates = json.load(f)
    with open(ROOT / args.db, encoding="utf-8") as f:
        db = json.load(f)
    with open(ROOT / "config" / "queries.yaml", encoding="utf-8") as f:
        crossref_base = yaml.safe_load(f).get("crossref", {}).get("base", "https://api.crossref.org/works")

    by_doi, by_preprint, by_arxiv, by_title = db_indexes(db)

    new, dropped, merges = [], [], []
    for c in candidates:
        doi = norm_doi(c.get("doi"))
        # Level 1: DOI exact
        if doi and doi in by_doi:
            dropped.append({"id": c["id"], "reason": "doi-exists", "existing": by_doi[doi]["id"]})
            continue
        # Level 2: arXiv / bioRxiv ID
        bp = biorxiv_id(doi)
        if bp and bp in by_preprint:
            dropped.append({"id": c["id"], "reason": "preprint-id-exists", "existing": by_preprint[bp]["id"]})
            continue
        ax = arxiv_base(c.get("arxiv_id") or (c["id"] if c.get("fetch_source") == "arxiv" else None))
        if ax and ax in by_arxiv:
            dropped.append({"id": c["id"], "reason": "arxiv-id-exists", "existing": by_arxiv[ax]["id"]})
            continue
        # Level 3: title fingerprint
        fp = title_fingerprint(c.get("title"))
        if fp and fp in by_title:
            dropped.append({"id": c["id"], "reason": "title-match", "existing": by_title[fp]["id"]})
            continue
        # preprint → published merge check (bioRxiv candidates only)
        if bp:
            published_doi = crossref_published_doi(doi, crossref_base)
            if published_doi and published_doi in by_doi:
                merges.append({
                    "preprint": doi,
                    "published": published_doi,
                    "action": "merge: set preprint_id + upgrade evidence on the DB entry",
                })
                dropped.append({"id": c["id"], "reason": "preprint-of-existing", "existing": by_doi[published_doi]["id"]})
                continue
            time.sleep(0.2)
        new.append(c)

    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(new, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report = {"input": len(candidates), "new": len(new), "dropped": dropped, "merges": merges}
    if args.report:
        rpath = ROOT / args.report
        rpath.parent.mkdir(parents=True, exist_ok=True)
        rpath.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"dedupe: {len(candidates)} in -> {len(new)} new, {len(dropped)} dropped, {len(merges)} merges")


if __name__ == "__main__":
    main()
