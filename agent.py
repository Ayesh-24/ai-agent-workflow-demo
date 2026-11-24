#!/usr/bin/env python3
"""
Claude Code AI Agent — Sample Workflow Demo
============================================
Trigger -> AI Agent -> Sync

A small, real, working demo of the workflow sold on the Fiverr gig
"Claude Code Expert and AI Agent Specialist" (@ashu1239).

What it does
------------
1. TRIGGER — watches messages/inbox/ for new customer message files (.txt).
2. AI AGENT — classifies each message (order / inquiry / support) and
   drafts a reply from a prompt template. This demo is RULE-BASED and
   needs NO API key: the same template is written so it can be dropped
   into Claude Code / an LLM call later — the classification keywords
   below are the "prompt logic", not a claim that an LLM ran here.
3. SYNC — writes one JSON reply file per message, appends to a JSONL
   log, and regenerates output/summary.md.

Honesty note: the three messages in messages/inbox/ are SAMPLE demo
data written for this portfolio project. They are not real clients,
real orders, or real reviews.

Run it
-------
    python3 agent.py            # process all messages in the inbox
    python3 agent.py --reset    # clear previous output first

Requires: Python 3.8+ only. No packages, no API key, no network.
"""

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
INBOX = BASE / "messages" / "inbox"
OUT = BASE / "output"
REPLIES = OUT / "replies"
LOG = OUT / "log.jsonl"
SUMMARY = OUT / "summary.md"

# --- AI Agent: prompt template (Claude-style, run locally as rules) ---
PROMPT_TEMPLATE = """You are a helpful assistant for a Claude Code / AI automation seller.
Classify the customer message as one of: order, inquiry, support.
Then draft a short, polite reply that:
- answers the question or confirms the request,
- states the next step (message before ordering / share details),
- never invents prices, timelines, or results you do not know.
Message: {message}
"""

RULES = [
    ("order", ["order", "build that", "syncs", "automate", "set up", "want"]),
    ("support", ["stopped", "not working", "broken", "fix", "error", "help fixing"]),
    ("inquiry", ["price", "how long", "what is", "cost", "package", "hello", "hi"]),
]

REPLY_TEMPLATES = {
    "order": (
        "Hi, thank you for your message! Yes, I can build that automation for "
        "you — syncing new orders to Google Sheets on a schedule is exactly "
        "the kind of workflow I set up. Please message me before ordering "
        "with your store details and how often you want the sync to run, "
        "and I will confirm the plan and timeline."
    ),
    "inquiry": (
        "Hi, thank you for asking! The Standard AI Agent Setup package is "
        "listed on my gig with its price and delivery time — please check "
        "the gig page for the current details, and message me before "
        "ordering so I can confirm it fits what you need."
    ),
    "support": (
        "Hi, I am sorry the automation stopped syncing — I can take a look. "
        "Please message me before ordering with the error you see (if any) "
        "and when it last worked, and I will check the workflow and fix it."
    ),
}


def classify(text: str) -> str:
    """Rule-based classifier standing in for the LLM prompt above."""
    lowered = text.lower()
    for label, keywords in RULES:
        if any(k in lowered for k in keywords):
            return label
    return "inquiry"


def process_message(path: Path) -> dict:
    text = path.read_text(encoding="utf-8").strip()
    label = classify(text)
    reply = REPLY_TEMPLATES[label]
    record = {
        "id": path.stem,
        "source_file": str(path.relative_to(BASE)),
        "received_at": datetime.now(timezone.utc).isoformat(),
        "classification": label,
        "prompt_template_used": PROMPT_TEMPLATE.format(message=text)[:200] + "...",
        "message": text,
        "draft_reply": reply,
        "status": "synced",
    }
    (REPLIES / f"{path.stem}.json").write_text(
        json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def write_summary(records: list) -> None:
    lines = [
        "# AI Agent Workflow — Sync Summary",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Messages processed: {len(records)}",
        "",
        "| ID | Classification | Status |",
        "|----|----------------|--------|",
    ]
    for r in records:
        lines.append(f"| {r['id']} | {r['classification']} | {r['status']} |")
    lines += ["", "## Draft replies", ""]
    for r in records:
        lines.append(f"### {r['id']} — {r['classification']}")
        lines.append("")
        lines.append(r["draft_reply"])
        lines.append("")
    SUMMARY.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Trigger -> AI Agent -> Sync demo")
    parser.add_argument("--reset", action="store_true", help="Clear previous output first")
    args = parser.parse_args()

    if args.reset and OUT.exists():
        shutil.rmtree(OUT)
    REPLIES.mkdir(parents=True, exist_ok=True)

    files = sorted(INBOX.glob("*.txt"))
    print("=" * 60)
    print("  CLAUDE CODE AI AGENT — Trigger -> AI Agent -> Sync")
    print("=" * 60)

    records = []
    for path in files:
        print(f"\n[1] TRIGGER  New message detected: {path.name}")
        print(f"    \"{path.read_text(encoding='utf-8').strip()[:80]}...\"")
        record = process_message(path)
        print(f"[2] AI AGENT  Classified as: {record['classification'].upper()}")
        print(f"    Draft reply ready ({len(record['draft_reply'])} chars)")
        print(f"[3] SYNC     Saved: output/replies/{path.stem}.json")
        records.append(record)

    write_summary(records)
    print(f"\n[3] SYNC     Summary written: output/summary.md")
    print(f"    Log appended: output/log.jsonl ({len(records)} records)")
    print(f"\nDone — {len(records)} message(s) processed. No API key used.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
