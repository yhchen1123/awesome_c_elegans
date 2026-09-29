#!/usr/bin/env python3
"""Monthly digest generator.

Usage:
    python3 scripts/digest.py                # full run: LLM summaries + OpenAlex refresh
    python3 scripts/digest.py --dry-run      # skeleton only: no LLM, no network writes

Behavior:
  1. Collect entries added during the previous calendar month and group them by
     primary category (C0–C9).
  2. Each section gets a 3–5 sentence Chinese LLM summary built ONLY from the
     section's titles + relevance notes (anti-hallucination: restatement only).
  3. Citation movers: refresh OpenAlex cited_by_count for the whole DB; list the
     top 10 by month-over-month increase (minimum +5); then persist new counts.
  4. Retraction watch: OpenAlex is_retracted scan of the whole DB; hits are
     flagged retracted: true in papers.json and alerted at the top of the digest.
  5. New entries are listed with their curated Chinese notes under each category.
  6. Cross-links (optional): an agent/LLM-authored markdown fragment (--insights)
     synthesizing interactions between papers — method combinations, tensions,
     and hypothesis seeds — injected as a dedicated section.

Outputs digest/YYYY-MM.md and updates papers.json (citations / retracted only).
Also writes build/pr_body.md for the monthly audit PR.
"""
import argparse
import datetime
import json
import os
import sys
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_section_defs():
    """Digest sections = taxonomy categories (C0–C9), loaded from config."""
    with open(ROOT / "config" / "taxonomy.yaml", encoding="utf-8") as f:
        cats = yaml.safe_load(f)["categories"]
    return [(code, c["name"], c.get("zh", "")) for code, c in cats.items()]


SUMMARY_PROMPT = """你是 awesome_c_elegans 文献库的编辑。下面是本月某个分类小节收录的条目（标题 + 既有中文注解）。
请用 3-5 句中文概括本小节的整体进展。铁律：只允许复述条目已有信息，禁止引入任何条目之外的结论、数字或文献。直接输出摘要文本，不要加标题。"""


def prev_month(today=None):
    today = today or datetime.date.today()
    first = today.replace(day=1)
    last_prev = first - datetime.timedelta(days=1)
    return last_prev.replace(day=1), last_prev


def load_db():
    with open(ROOT / "data" / "papers.json", encoding="utf-8") as f:
        return json.load(f)


def save_db(db):
    with open(ROOT / "data" / "papers.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
        f.write("\n")


def openalex_refresh(db, dry_run=False):
    """Batch-refresh citations + retraction status by DOI (50 per call).

    Returns (movers, retracted_hits); each mover = {id, title, old, new, delta}.
    """
    by_doi = {p["doi"].lower(): p for p in db if p.get("doi")}
    dois = sorted(by_doi)
    movers, retracted = [], []
    email = os.environ.get("EPMC_EMAIL", "").strip()
    headers = {"User-Agent": f"awesome_c_elegans/0.1 (mailto:{email or 'unset@example.org'})"}
    for i in range(0, len(dois), 20):  # 大批次易被限流；doi 过滤为单键 OR（doi:a|b，重复 doi: 键会被视为 filter 间 OR 而 400）
        chunk = dois[i:i + 20]
        filt = "doi:" + "|".join(chunk)
        try:
            r = requests.get("https://api.openalex.org/works",
                             params={"filter": filt, "per-page": 25}, headers=headers, timeout=60)
            if r.status_code != 200:
                print(f"  openalex batch {i // 50 + 1}: HTTP {r.status_code}", file=sys.stderr)
                continue
            for w in r.json().get("results", []):
                doi = (w.get("doi") or "").lower().replace("https://doi.org/", "")
                p = by_doi.get(doi)
                if not p:
                    continue
                old = p.get("citations", 0) or 0
                new = w.get("cited_by_count", old)
                delta = new - old
                if delta >= 5:
                    movers.append({"id": p["id"], "title": p["title"],
                                   "old": old, "new": new, "delta": delta})
                if w.get("is_retracted") and not p.get("retracted"):
                    retracted.append({"id": p["id"], "title": p["title"]})
                    if not dry_run:
                        p["retracted"] = True
                if not dry_run:
                    p["citations"] = new
        except Exception as e:  # noqa: BLE001
            print(f"  openalex batch {i // 50 + 1} failed: {e}", file=sys.stderr)
    movers.sort(key=lambda m: -m["delta"])
    return movers[:10], retracted


def section_of(p):
    return p.get("categories", ["C9"])[0]


def llm_summarize(entries, cfg):
    if not cfg.get("api_key"):
        return None
    lines = [f"- {p['title']}：{p.get('relevance_note', '')}" for p in entries]
    try:
        from classify import llm_chat  # reuse the hardened client
        return llm_chat(
            [{"role": "system", "content": SUMMARY_PROMPT},
             {"role": "user", "content": "\n".join(lines)}],
            {"api_key": cfg["api_key"], "base_url": cfg["base_url"], "model": cfg["model"]},
        ).strip()
    except Exception as e:  # noqa: BLE001
        print(f"  section summary LLM failed: {e}", file=sys.stderr)
        return None


def entry_line(p):
    note = p.get("relevance_note", "")
    flag = " ⚠️ emerging evidence" if p.get("evidence") == "emerging-evidence" else ""
    return f"- [{p['title']}]({p['url']}) — {p.get('venue', '')} {p.get('year', '')} `{p['tier']}`{flag}：{note}"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="skeleton only: no LLM summaries, no OpenAlex refresh, no DB writes")
    ap.add_argument("--month", default=None, metavar="YYYY-MM",
                    help="cover the given calendar month instead of the previous one")
    ap.add_argument("--summaries", default=None, metavar="PATH",
                    help="JSON file mapping category code -> section summary text "
                         "(agent-authored summaries in local mode; takes precedence over LLM)")
    ap.add_argument("--insights", default=None, metavar="PATH",
                    help="markdown file with cross-paper synthesis (method combinations, "
                         "tensions, hypothesis seeds), injected as the Cross-links section")
    args = ap.parse_args()

    if args.month:
        m_start = datetime.date.fromisoformat(args.month + "-01")
        m_end = (m_start.replace(day=28) + datetime.timedelta(days=7)).replace(day=1) - datetime.timedelta(days=1)
    else:
        m_start, m_end = prev_month()
    month_label = m_start.strftime("%Y-%m")
    db = load_db()
    new_entries = [p for p in db if m_start.isoformat() <= p.get("added", "") <= m_end.isoformat()]

    cfg = {
        "api_key": os.environ.get("LLM_API_KEY", "").strip(),
        "base_url": os.environ.get("LLM_BASE_URL", "").strip() or "https://api.moonshot.cn/v1",
        "model": os.environ.get("LLM_MODEL", "").strip() or "kimi-k2-0905-preview",
    }
    supplied_summaries = {}
    if args.summaries:
        with open(args.summaries, encoding="utf-8") as f:
            supplied_summaries = json.load(f)
    insights_md = None
    if args.insights:
        insights_md = Path(args.insights).read_text(encoding="utf-8").strip()

    movers, retracted = ([], [])
    if not args.dry_run:
        print("refreshing OpenAlex citations / retraction status...")
        movers, retracted = openalex_refresh(db)
        save_db(db)

    # group new entries by primary category
    section_defs = load_section_defs()
    sections = {code: [] for code, _, _ in section_defs}
    for p in new_entries:
        sec = section_of(p)
        sections.setdefault(sec if sec in sections else "C9", []).append(p)

    lines = [f"# Monthly Digest {month_label}", ""]
    lines.append("<!-- Auto-generated by scripts/digest.py. -->")
    lines.append("")
    lines.append(f"收录窗口：{m_start.isoformat()} — {m_end.isoformat()}；新增 {len(new_entries)} 条。")
    lines.append("")

    lines.append("## ⚠️ Retraction watch")
    lines.append("")
    if args.dry_run:
        lines.append("（dry-run：未执行 OpenAlex 撤稿扫描）")
    elif retracted:
        for r in retracted:
            lines.append(f"- ❌ **{r['title']}** (`{r['id']}`) 被 OpenAlex 标记为 retracted，已更新 `retracted: true`，请人工复核。")
    else:
        lines.append("全库扫描未发现新的撤稿标记。")
    lines.append("")

    for code, name, zh in section_defs:
        entries = sections.get(code, [])
        lines.append(f"## {code} — {name}（{zh}）（{len(entries)} 条）")
        lines.append("")
        if not entries:
            lines.append("本月无新增。")
        else:
            summary = supplied_summaries.get(code)
            if summary is None and not args.dry_run:
                summary = llm_summarize(entries, cfg)
            if summary:
                lines.append(summary)
                lines.append("")
            for p in entries:
                lines.append(entry_line(p))
        lines.append("")

    if insights_md:
        lines.append("## 🔗 Cross-links（交叉洞察：方法、发现与观点的相互作用）")
        lines.append("")
        lines.append("> 本节由策展 agent 撰写：梳理本月条目之间的相互作用——可组合的方法、"
                     "相互印证或冲突的发现、以及由此涌现的可检验猜想。所有内容均基于已收录条目的"
                     "公开信息，供读者与 AI 二次加工。")
        lines.append("")
        lines.append(insights_md)
        lines.append("")

    lines.append("## 📈 Citation movers（环比增速 Top 10，新增引用 ≥5）")
    lines.append("")
    if args.dry_run:
        lines.append("（dry-run：未刷新引用数）")
    elif movers:
        lines.append("| 文献 | 原引用 | 现引用 | Δ |")
        lines.append("|---|---|---|---|")
        for m in movers:
            lines.append(f"| {m['title'][:60]} | {m['old']} | {m['new']} | +{m['delta']} |")
    else:
        lines.append("本月无显著引用增长。")
    lines.append("")

    out = ROOT / "digest" / f"{month_label}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(new_entries)} new entries, "
          f"{len(movers)} movers, {len(retracted)} retractions)")

    pr = ROOT / "build" / "pr_body.md"
    pr.parent.mkdir(parents=True, exist_ok=True)
    pr.write_text(
        f"## 📊 Monthly digest {month_label}\n\n"
        f"- 新增条目：{len(new_entries)}（见 `digest/{month_label}.md`）\n"
        f"- Citation movers：{len(movers)}；Retraction 命中：{len(retracted)}\n"
        f"- `papers.json` 仅更新 citations / retracted 字段。\n\n"
        "*Generated by scripts/digest.py. Nothing is merged without human review.*\n",
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    main()
