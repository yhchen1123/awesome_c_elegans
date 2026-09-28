#!/usr/bin/env python3
"""Validate data/papers.json and rendered artifacts.

Checks:
  1. JSON Schema validation of every entry
  2. Global id uniqueness
  3. Category codes within taxonomy enum
  4. `added` date format (YYYY-MM-DD)
  5. Rendered artifacts up to date (delegates to render.py --check)

Exit code 0 when everything passes; otherwise prints a problem list and exits 1.
"""
import re
import subprocess
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent

SCHEMA = {
    "type": "object",
    "required": ["id", "title", "authors", "venue", "year", "categories", "tier", "evidence", "url", "added", "source"],
    "properties": {
        "id": {"type": "string", "description": "DOI / arXiv ID / bioRxiv DOI / manual:slug, globally unique"},
        "title": {"type": "string"},
        "authors": {"type": "array", "items": {"type": "string"}},
        "venue": {"type": "string"},
        "year": {"type": "integer"},
        "categories": {
            "type": "array",
            "items": {"enum": ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]},
            "minItems": 1,
        },
        "tags": {"type": "array", "items": {"type": "string"}, "description": "modality + species tags"},
        "tier": {"enum": ["T1-core", "T2-adjacent", "T3-transfer"]},
        "evidence": {"enum": ["peer-reviewed", "preprint", "emerging-evidence"]},
        "standards": {
            "type": "array",
            "items": {"enum": ["embryo-level-split", "open-loop-rollout", "uncertainty-quantified",
                               "perturbation-holdout", "shortcut-audit"]},
        },
        "relevance_note": {"type": "string", "description": "中文注解，1-2 句"},
        "url": {"type": "string"},
        "doi": {"type": "string"},
        "preprint_id": {"type": "string", "description": "若已正式发表，保留预印本链接"},
        "citations": {"type": "integer", "description": "OpenAlex cited_by_count，月度更新"},
        "retracted": {"type": "boolean"},
        "confidence": {"type": "number", "description": "LLM 分类置信度 0-1；manual 条目为 1.0"},
        "needs_review": {"type": "boolean"},
        "added": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
        "source": {"type": "string", "description": "manual / epmc / arxiv / issue"},
    },
}

VALID_SOURCES = {"manual", "epmc", "arxiv", "issue"}
VALID_TIERS = {"T1-core", "T2-adjacent", "T3-transfer"}
VALID_EVIDENCE = {"peer-reviewed", "preprint", "emerging-evidence"}
VALID_STANDARDS = {"embryo-level-split", "open-loop-rollout", "uncertainty-quantified",
                   "perturbation-holdout", "shortcut-audit"}


def main():
    import json
    problems = []

    with open(ROOT / "config" / "taxonomy.yaml", encoding="utf-8") as f:
        tax = yaml.safe_load(f)
    valid_categories = set(tax["categories"].keys())
    valid_tags = set(tax.get("modality_tags", [])) | set(tax.get("species_tags", []))

    with open(ROOT / "data" / "papers.json", encoding="utf-8") as f:
        papers = json.load(f)

    validator = jsonschema.Draft7Validator(SCHEMA)
    seen_ids = {}
    for i, p in enumerate(papers):
        label = p.get("id", f"<entry #{i}>")
        for err in validator.iter_errors(p):
            problems.append(f"{label}: schema: {err.message}")
        pid = p.get("id")
        if pid in seen_ids:
            problems.append(f"{label}: duplicate id (also at index {seen_ids[pid]})")
        else:
            seen_ids[pid] = i
        for c in p.get("categories", []):
            if c not in valid_categories:
                problems.append(f"{label}: unknown category {c}")
        for t in p.get("tags", []):
            if t not in valid_tags:
                problems.append(f"{label}: unknown tag {t}")
        if p.get("tier") and p["tier"] not in VALID_TIERS:
            problems.append(f"{label}: invalid tier {p['tier']}")
        if p.get("evidence") and p["evidence"] not in VALID_EVIDENCE:
            problems.append(f"{label}: invalid evidence {p['evidence']}")
        for s in p.get("standards", []):
            if s not in VALID_STANDARDS:
                problems.append(f"{label}: invalid standard {s}")
        if p.get("source") and p["source"] not in VALID_SOURCES:
            problems.append(f"{label}: invalid source {p['source']}")
        added = p.get("added", "")
        if added and not re.match(r"^\d{4}-\d{2}-\d{2}$", added):
            problems.append(f"{label}: bad added date {added!r}")
        if p.get("evidence") in {"preprint", "emerging-evidence"} and "evidence" not in p:
            problems.append(f"{label}: preprint without explicit evidence label")
        conf = p.get("confidence")
        if conf is not None and not (0.0 <= conf <= 1.0):
            problems.append(f"{label}: confidence {conf} out of [0,1]")

    if problems:
        print("papers.json validation FAILED:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(1)
    print(f"papers.json OK ({len(papers)} entries, schema + uniqueness + enums passed).")

    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "render.py"), "--check"])
    if r.returncode != 0:
        print("validate FAILED: rendered artifacts are stale (run scripts/render.py).", file=sys.stderr)
        sys.exit(1)
    print("validate OK.")


if __name__ == "__main__":
    main()
