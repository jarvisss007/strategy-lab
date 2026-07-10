#!/usr/bin/env python3
"""Learning meter — one row per day snapshotting every accumulation counter across
the whole stack, appended to progress.csv. This is the guarantee that "there is
always progress": if these counters aren't growing, something is broken and the
Progress tab shows it. Run daily by refresh_all.sh (launchd).
Run: /opt/anaconda3/bin/python learning_meter.py"""
import csv, os
import datetime as dt

LAB = os.path.dirname(os.path.abspath(__file__))
RADAR = os.path.join(os.path.expanduser("~"), "stock-radar")
OUT = os.path.join(LAB, "progress.csv")


def rows(path):
    try:
        with open(path) as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def count_lines(path, contains=None):
    try:
        with open(path) as f:
            return sum(1 for ln in f if (contains in ln if contains else ln.strip()))
    except Exception:
        return 0


def main():
    today = str(dt.date.today())
    led = rows(os.path.join(RADAR, "agent", "ledger.csv"))
    scored = [r for r in led if r.get("outcome") in ("right", "wrong")]
    plans = rows(os.path.join(RADAR, "agent", "plans.csv"))
    dlog = rows(os.path.join(LAB, "daytype_log.csv"))
    briefs_dir = os.path.join(RADAR, "agent", "briefs")
    briefs = len([f for f in os.listdir(briefs_dir) if f.endswith(".md")]) if os.path.isdir(briefs_dir) else 0
    rec = {
        "date": today,
        "briefs": briefs,
        "ledger_calls": len(led),
        "ledger_scored": len(scored),
        "ledger_right": sum(1 for r in scored if r["outcome"] == "right"),
        "plans_total": len(plans),
        "plans_triggered": sum(1 for p in plans if p.get("status") == "triggered"),
        "lessons_entries": count_lines(os.path.join(RADAR, "agent", "lessons.md"), contains="- "),
        "recorder_namedays": len(dlog),
        "recorder_sessions": len({r["date"] for r in dlog}),
        "kb_rows": len(rows(os.path.join(LAB, "knowledge_base.csv"))),
        "discoveries_rows": len(rows(os.path.join(LAB, "discoveries.csv"))),
    }
    existing = rows(OUT)
    if any(r["date"] == today for r in existing):
        existing = [r for r in existing if r["date"] != today] + [dict((k, str(v)) for k, v in rec.items())]
        with open(OUT, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rec.keys()))
            w.writeheader()
            w.writerows(existing)
    else:
        new = not os.path.exists(OUT)
        with open(OUT, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rec.keys()))
            if new:
                w.writeheader()
            w.writerow(rec)
    print("progress:", rec)


if __name__ == "__main__":
    main()
