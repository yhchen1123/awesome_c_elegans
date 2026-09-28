#!/usr/bin/env python3
"""Render README.md and categories/*.md from data/papers.json (single source of truth).

Usage:
    python3 scripts/render.py            # render in place
    python3 scripts/render.py --check    # verify committed files match a fresh render

Exit code is non-zero in --check mode when any rendered file differs.
Also writes build/render_report.json (counts, C7 share) for PR-body generation.

Rendering notes (README is awesome-linted; categories/*.md are not):
  * The H1 is an HTML heading so the species epithet keeps its correct lowercase
    (and italic) form — awesome-lint's title-case rule only inspects mdast headings.
  * Each paper is listed once in README, under its primary category
    (categories[0]); multi-category entries carry an "also filed under" hint, and
    category pages under categories/ contain the full cross-listed listings.
    (awesome-lint double-link forbids repeating a main link across sections.)
  * README entries use `- [title](url) - author, *venue* year ` + inline-code badges
"""
import argparse
import datetime
import difflib
import json
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY = ROOT / "config" / "taxonomy.yaml"
PAPERS = ROOT / "data" / "papers.json"

# Category code -> stable filename slug
SLUGS = {
    "C0": "measurement-tracking",
    "C1": "cell-representation",
    "C2": "wt-dynamics",
    "C3": "morphology-mechanics",
    "C4": "molecular-regulation",
    "C5": "perturbation-causal",
    "C6": "fate-lineage-biology",
    "C7": "methods-transfer",
    "C8": "datasets-benchmarks-software",
    "C9": "reviews-perspectives",
}

# Cross-links between related categories (topical proximity)
RELATED = {
    "C0": ["C1", "C8"],
    "C1": ["C0", "C2", "C7"],
    "C2": ["C3", "C5", "C6"],
    "C3": ["C2", "C4", "C5"],
    "C4": ["C5", "C6"],
    "C5": ["C2", "C3", "C4"],
    "C6": ["C4", "C9"],
    "C7": ["C0", "C1"],
    "C8": ["C0", "C4"],
    "C9": ["C6"],
}

GENERATED_NOTE = "<!-- Auto-generated from data/papers.json by scripts/render.py. Do not edit manually. -->"


def load_taxonomy():
    with open(TAXONOMY, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_papers():
    with open(PAPERS, encoding="utf-8") as f:
        return json.load(f)


def anchor(heading):
    """GitHub-slugger style anchor for a section heading (ASCII headings only)."""
    out = []
    for ch in heading.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch == " ":
            out.append("-")
    return "".join(out)


def first_author(authors):
    if not authors:
        return "Unknown"
    fam = authors[0].strip().split()[-1]
    return f"{fam} et al." if len(authors) > 1 else fam


def badges(p):
    out = [f"`{p['tier']}`", f"`{p['evidence']}`"]
    out += [f"`{s}`" for s in p.get("standards", [])]
    if p.get("retracted"):
        out.append("`❌ retracted`")
    return " ".join(out)


def note_text(p):
    note = p.get("relevance_note", "").strip()
    if p.get("evidence") == "emerging-evidence":
        note = "⚠️ emerging evidence: " + note
    if p.get("retracted"):
        note = "⚠️ This paper has been retracted. " + note
    return note


def also_filed(p):
    """Inline hint for secondary categories (README single-listing policy)."""
    rest = p.get("categories", [])[1:]
    if not rest:
        return ""
    return " · also filed under " + " ".join(f"`{c}`" for c in rest)


def render_entry_readme(p):
    """awesome-lint compliant entry: plain link, ' - ' separator, italic note."""
    title = p["title"]
    if p.get("retracted"):
        title = f"❌ {title}"
    head = (f"[{title}]({p['url']}) - {first_author(p.get('authors', []))}, "
            f"*{p['venue']}* {p['year']} {badges(p)}{also_filed(p)}")
    return f"- {head}<br>\n  *{note_text(p)}*"


def render_entry_page(p):
    """Rich entry for category pages (not awesome-linted)."""
    head = (f"**[{p['title']}]({p['url']})** — {first_author(p.get('authors', []))}, "
            f"*{p['venue']}* {p['year']} {badges(p)}")
    if p.get("retracted"):
        head = f"~~{head}~~"
    return f"- {head}<br>\n  {note_text(p)}"


def sort_key(p):
    return (-int(p.get("year") or 0), p.get("added", ""), p.get("title", "").lower())


def sorted_papers(papers):
    return sorted(papers, key=sort_key)


def primary_grouped(papers):
    """README grouping: each paper appears once, under categories[0]."""
    grouped = {code: [] for code in SLUGS}
    for p in sorted_papers(papers):
        cats = [c for c in p.get("categories", []) if c in grouped]
        if cats:
            grouped[cats[0]].append(p)
    return grouped


def full_grouped(papers):
    """Category-page grouping: a paper appears in every assigned category."""
    grouped = {code: [] for code in SLUGS}
    for p in sorted_papers(papers):
        for c in p.get("categories", []):
            if c in grouped:
                grouped[c].append(p)
    return grouped


def cross_listed(papers, code):
    """Papers whose primary category is elsewhere but which also carry `code`."""
    return [p for p in sorted_papers(papers)
            if p.get("categories") and p["categories"][0] != code and code in p["categories"][1:]]


def c7_stats(papers):
    c7 = [p for p in papers if "C7" in p.get("categories", [])]
    t3 = [p for p in c7 if p.get("tier") == "T3-transfer"]
    share = (len(t3) / len(c7)) if c7 else 0.0
    return len(c7), len(t3), share


def render_readme(tax, papers):
    cats = tax["categories"]
    grouped = primary_grouped(papers)
    total = len(papers)
    last_update = max((p.get("added", "") for p in papers), default="")
    c7_n, c7_t3, c7_share = c7_stats(papers)

    lines = []
    # HTML H1 keeps "C. elegans" lowercase/italic; awesome-lint title-case only
    # inspects mdast headings (HTML headings at document start are supported).
    lines.append("<h1>Awesome <i>C. elegans</i> Embryogenesis</h1>")
    lines.append("")
    lines.append(GENERATED_NOTE)
    lines.append("")
    lines.append("[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)")
    lines.append(
        f"![papers](https://img.shields.io/badge/papers-{total}-blue) "
        f"![last update](https://img.shields.io/badge/last_update-{last_update.replace('-', '--')}-green)"
    )
    lines.append("")
    lines.append(
        "> AI-curated, human-audited multidisciplinary literature tracking for *C. elegans* "
        "embryogenesis research — from lineage-resolved atlases and live imaging to mechanics, "
        "molecular regulation, and dynamical modeling. Updated weekly by automation; every update "
        "lands as a reviewed PR."
    )
    lines.append("")
    lines.append(
        "This repository is maintained by an **AI-search + human-PR-audit** loop: a weekly GitHub "
        "Actions run queries Europe PMC (PubMed + bioRxiv/medRxiv) and arXiv for new literature, an "
        "LLM classifies candidates into the taxonomy below and writes Chinese relevance notes, and all "
        "changes are delivered as a pull request for human review — nothing is pushed to `main` "
        "directly. A monthly digest summarizes the month's additions by theme and watches for "
        "retractions. Each category also has a dedicated page under `categories/` with the full "
        "cross-listed entries. See `CONTRIBUTING.md` for inclusion criteria and `docs/DEVELOPMENT.md` "
        "for operations. License: CC0-1.0 (see `LICENSE`)."
    )
    lines.append("")
    if c7_share > 0.30:
        lines.append(
            f"> ⚠️ **C7 soft-cap warning:** T3-transfer entries make up {c7_share:.0%} of Methods "
            f"Transfer ({c7_t3}/{c7_n}), exceeding the 30% soft cap. Maintainers should consider "
            "tightening arXiv queries or triaging low-relevance entries."
        )
        lines.append("")
    lines.append("## Contents")
    lines.append("")
    for code in SLUGS:
        name = cats[code]["name"]
        lines.append(f"- [{name}](#{anchor(name)})")
    lines.append("")
    for code in SLUGS:
        c = cats[code]
        lines.append(f"## {c['name']}")
        lines.append("")
        lines.append(f"**{c['zh']}** · {code}")
        lines.append("")
        entries = grouped[code]
        if entries:
            for p in entries:
                lines.append(render_entry_readme(p))
        else:
            lines.append("No entries yet.")
        cross = cross_listed(papers, code)
        if cross:
            lines.append("")
            lines.append(
                f"*See the [category page](categories/{code}-{SLUGS[code]}.md) for "
                f"{len(cross)} cross-listed entr{'ies' if len(cross) > 1 else 'y'} filed primarily elsewhere.*"
            )
        lines.append("")
    return "\n".join(lines)


def render_category_page(tax, papers, code):
    cats = tax["categories"]
    c = cats[code]
    grouped = full_grouped(papers)
    lines = []
    lines.append(f"# {code}: {c['name']}（{c['zh']}）")
    lines.append("")
    lines.append(GENERATED_NOTE)
    lines.append("")
    lines.append(f"> **Scope**: {c['scope']}")
    lines.append("")
    lines.append("[← Back to README](../README.md)")
    lines.append("")
    entries = grouped[code]
    lines.append(f"## Papers ({len(entries)})")
    lines.append("")
    if entries:
        for p in entries:
            lines.append(render_entry_page(p))
    else:
        lines.append("No entries yet.")
    lines.append("")
    lines.append("## Related categories")
    lines.append("")
    for r in RELATED.get(code, []):
        rc = cats[r]
        lines.append(f"- [{r}: {rc['name']}]({r}-{SLUGS[r]}.md) — {rc['zh']}")
    lines.append("")
    return "\n".join(lines)


def render_all(outdir):
    tax = load_taxonomy()
    papers = load_papers()
    files = {"README.md": render_readme(tax, papers)}
    for code in SLUGS:
        files[f"categories/{code}-{SLUGS[code]}.md"] = render_category_page(tax, papers, code)
    written = []
    for rel, content in files.items():
        path = outdir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(rel)
    return files, tax, papers


def write_report(papers):
    grouped = full_grouped(papers)
    c7_n, c7_t3, c7_share = c7_stats(papers)
    report = {
        "total": len(papers),
        "per_category": {code: len(v) for code, v in grouped.items()},
        "c7_total": c7_n,
        "c7_t3_transfer": c7_t3,
        "c7_t3_share": round(c7_share, 4),
        "c7_soft_cap_exceeded": c7_share > 0.30,
        "generated_at": datetime.date.today().isoformat(),
    }
    report_path = ROOT / "build" / "render_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check():
    with tempfile.TemporaryDirectory() as tmp:
        files, _, _ = render_all(Path(tmp))
        problems = []
        for rel, content in files.items():
            current_path = ROOT / rel
            if not current_path.exists():
                problems.append(f"{rel}: missing (would be created)")
                continue
            current = current_path.read_text(encoding="utf-8")
            if current != content:
                diff = "\n".join(
                    difflib.unified_diff(
                        current.splitlines(), content.splitlines(),
                        fromfile=f"current/{rel}", tofile=f"rendered/{rel}", lineterm="",
                    )
                )
                problems.append(f"{rel}: out of date\n{diff}")
        if problems:
            print("render check FAILED — rendered artifacts are stale:", file=sys.stderr)
            for p in problems:
                print(f"\n--- {p}", file=sys.stderr)
            return 1
        print("render check OK — all rendered artifacts are up to date.")
        return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="verify committed files match a fresh render")
    args = ap.parse_args()
    if args.check:
        sys.exit(check())
    files, tax, papers = render_all(ROOT)
    write_report(papers)
    print(f"rendered {len(files)} files from {len(papers)} papers.")


if __name__ == "__main__":
    main()
