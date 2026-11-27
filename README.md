# Claude Code AI Agent — Sample Workflow Project

A small, real, working portfolio demo for the Fiverr gig
**"Claude Code Expert and AI Agent Specialist"** — Ayesha Madni (@ashu1239).

- **Fiverr gig:** https://www.fiverr.com/ashu1239/be-your-claude-code-expert-and-set-up-ai-agents-mcp-servers-and-automations
- **Workflow video:** `fiverr-workflow-video.mp4` (66 seconds, Trigger → AI Agent → Sync) — the same video on the gig page
- **Author:** Ayesha Madni
- **Skills shown:** Claude Code, AI agents, MCP servers, Python, automation

## About this project

This project shows, in working code, exactly what the gig delivers:
a customer message comes in, an AI agent understands it and drafts a
reply, and the result is synced and saved — nothing is faked, nothing
is hidden. A buyer can run it in one minute and see the whole workflow
with their own eyes.

## The workflow: Trigger → AI Agent → Sync

| Step | What happens |
|------|--------------|
| **1. Trigger** | A new customer message file arrives in `messages/inbox/` |
| **2. AI Agent** | The agent classifies it — `order`, `inquiry` or `support` — and drafts a polite reply from a Claude-style prompt template |
| **3. Sync** | The result is saved to `output/replies/<id>.json`, appended to `output/log.jsonl`, and summarised in `output/summary.md` |

## Run it

```bash
python3 agent.py            # process all messages in the inbox
python3 agent.py --reset    # clear previous output first
```

Requires Python 3.8+ only. **No packages, no API key, no network.**

## What the gig builds for you

- **Basic — Claude Code Setup ($90):** set up Claude Code for your project, with clean, commented code.
- **Standard — AI Agent Setup ($100):** build an AI agent like this one, adapted to your own messages and workflow, with database integration.
- **Premium — Full AI Automation System ($250):** a complete automation system — trigger, agent, MCP server connection and sync — built and documented for your business.

Message before ordering, so the exact scope, tools and accounts can be agreed first.

## Honest scope

- The classifier in this demo is **rule-based** — the prompt template in
  `agent.py` is written so it can be dropped into Claude Code / an LLM
  call later, but this demo does not call any AI API and does not claim to.
- The three messages in `messages/inbox/` are **sample demo data** written
  for this portfolio project. They are not real clients, real orders,
  or real reviews.
- Draft replies never invent prices or timelines — they point the
  customer to the gig page and ask them to message before ordering.

## Project layout

```
ai-agent-workflow-demo/
├── agent.py                  # Trigger → AI Agent → Sync (the whole demo)
├── messages/inbox/           # sample incoming messages (msg-001..003)
├── output/
│   ├── replies/              # one JSON reply file per message
│   ├── log.jsonl             # append-only sync log
│   └── summary.md            # regenerated summary table + replies
├── demo-run-output.txt       # captured output of a real run
├── fiverr-workflow-video.mp4 # 66-second workflow video (same as on the gig)
└── README.md                 # this file
```

## Demo run

See `demo-run-output.txt` for the captured terminal output of
`python3 agent.py --reset`. It processes 3 sample messages:
`msg-001 → inquiry`, `msg-002 → order`, `msg-003 → support`.

## Video

`fiverr-workflow-video.mp4` shows the workflow step by step:
title → Step 1 Trigger → the real terminal run → Step 2 AI Agent →
Step 3 Sync → results → "Message Me Before Ordering". It is the video
on the Fiverr gig, so buyers see the same project here and there.
