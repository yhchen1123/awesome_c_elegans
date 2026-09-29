#!/usr/bin/env python3
"""Print today's tracking category for the workday rotation.

规则：从纪元周（2026-W40）起，每个工作日推进一个分类，两周覆盖全部 C0–C9：
    index = (iso_week * 5 + weekday) mod 10   # weekday: Mon=0 .. Fri=4
周末不运行（定时任务仅周一到周五触发）。

Usage:
    python3 scripts/next_category.py            # 打印今日分类，如 C3
    python3 scripts/next_category.py --date 2026-10-05
"""
import argparse
import datetime

CATEGORIES = [f"C{i}" for i in range(10)]
EPOCH_WEEK = 40  # 2026 年第 40 个 ISO 周（2026-09-28 所在周）为 C0 起始周


def category_for(d: datetime.date) -> str:
    iso_week = d.isocalendar()[1]
    weekday = d.weekday()  # Mon=0
    return CATEGORIES[(iso_week * 5 + weekday) % 10]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=None, help="YYYY-MM-DD，默认今天")
    args = ap.parse_args()
    d = datetime.date.fromisoformat(args.date) if args.date else datetime.date.today()
    print(category_for(d))


if __name__ == "__main__":
    main()
