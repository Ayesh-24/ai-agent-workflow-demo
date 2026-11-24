#!/usr/bin/env python3
"""Render 1280x720 slides for the workflow video (teal/mint/ink)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path("/home/hatch/workspace/fiverr-sample-project/video_frames")
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1280, 720
TEAL = (8, 127, 121)
MINT = (230, 245, 241)
INK = (21, 51, 51)
WHITE = (255, 255, 255)
DARK = (10, 40, 38)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FMB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def text_center(d, y, s, f, color, w=W):
    bbox = d.textbbox((0, 0), s, font=f)
    d.text(((w - (bbox[2] - bbox[0])) / 2, y), s, font=f, fill=color)

def wrap(d, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur:
        lines.append(cur)
    return lines

def slide_bg(color=MINT):
    img = Image.new("RGB", (W, H), color)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 10], fill=TEAL)
    d.rectangle([0, H - 10, W, H], fill=TEAL)
    return img, d

def kicker(d, s, y=70):
    text_center(d, y, s, font(FB, 30), TEAL)

def title(d, s, y=130, size=64):
    for i, line in enumerate(wrap(d, s, font(FB, size), 1050)):
        text_center(d, y + i * 78, line, font(FB, size), INK)

def body(d, lines, y=330, size=34, color=INK):
    for i, line in enumerate(lines):
        text_center(d, y + i * 52, line, font(FR, size), color)

def step_badge(d, n):
    d.ellipse([590, 210, 690, 310], fill=TEAL)
    text_center(d, 232, str(n), font(FB, 52), WHITE, w=1280)

# 1 — Title
img, d = slide_bg(TEAL)
text_center(d, 120, "CLAUDE CODE EXPERT", font(FB, 72), WHITE)
text_center(d, 220, "AI Agents  •  MCP Servers  •  Automations", font(FR, 36), (200, 240, 235))
d.line([340, 320, 940, 320], fill=(120, 200, 190), width=3)
text_center(d, 360, "My Workflow", font(FB, 56), WHITE)
text_center(d, 450, "Trigger  →  AI Agent  →  Sync", font(FB, 40), (200, 240, 235))
text_center(d, 560, "A real sample project — built with Python, no API key needed",
            font(FR, 28), (200, 240, 235))
img.save(OUT / "01-title.png")

# 2 — Step 1 Trigger
img, d = slide_bg()
kicker(d, "STEP 1")
step_badge(d, 1)
title(d, "TRIGGER", y=320, size=60)
body(d, ["A new customer message arrives in", "messages/inbox/msg-002.txt",
         "", '"...syncs new Shopify orders', 'to Google Sheets every hour..."'], y=430)
img.save(OUT / "02-trigger.png")

# 3 — Terminal (screen-recording style)
img = Image.new("RGB", (W, H), (12, 24, 22))
d = ImageDraw.Draw(img)
d.rectangle([40, 40, 1240, 680], fill=(18, 34, 32), outline=TEAL, width=3)
d.ellipse([70, 62, 88, 80], fill=(255, 95, 86))
d.ellipse([100, 62, 118, 80], fill=(255, 189, 46))
d.ellipse([130, 62, 148, 80], fill=(39, 201, 63))
d.text((70, 100), "terminal — fiverr-sample-project", font=font(FM, 24), fill=(150, 200, 195))
lines = [
    ("$ python3 agent.py --reset", (255, 255, 255), FMB),
    ("", (255, 255, 255), FM),
    ("[1] TRIGGER  New message detected: msg-002.txt", (120, 220, 205), FMB),
    ('    "Hello, I want to order an automation that', (220, 235, 230), FM),
    ('     syncs new Shopify orders to Google Sheets..."', (220, 235, 230), FM),
    ("[2] AI AGENT  Classified as: ORDER", (120, 220, 205), FMB),
    ("    Draft reply ready (306 chars)", (220, 235, 230), FM),
    ("[3] SYNC     Saved: output/replies/msg-002.json", (120, 220, 205), FMB),
    ("", (255, 255, 255), FM),
    ("Done — 3 message(s) processed. No API key used.", (90, 230, 120), FMB),
]
y = 150
for s, c, f in lines:
    d.text((70, y), s, font=font(f, 27), fill=c)
    y += 42
img.save(OUT / "03-terminal.png")

# 4 — Step 2 AI Agent
img, d = slide_bg()
kicker(d, "STEP 2")
step_badge(d, 2)
title(d, "AI AGENT", y=320, size=60)
body(d, ["Classifies the message:  ORDER", "",
         "Drafts a polite reply from a", "Claude-style prompt template",
         "— no prices or timelines invented"], y=430)
img.save(OUT / "04-agent.png")

# 5 — Step 3 Sync
img, d = slide_bg()
kicker(d, "STEP 3")
step_badge(d, 3)
title(d, "SYNC", y=320, size=60)
body(d, ["output/replies/msg-002.json", "output/log.jsonl",
         "output/summary.md", "", "✓  Saved and logged — synced"], y=430)
img.save(OUT / "05-sync.png")

# 6 — Results
img, d = slide_bg()
kicker(d, "RESULT")
title(d, "3 messages processed", y=150, size=56)
body(d, ["msg-001  →  inquiry   ✓ synced",
         "msg-002  →  order     ✓ synced",
         "msg-003  →  support   ✓ synced", "",
         "Sample data only — no fake clients,",
         "no fake orders, no fake reviews"], y=300)
img.save(OUT / "06-results.png")

# 7 — End CTA
img, d = slide_bg(TEAL)
text_center(d, 180, "Message Me", font(FB, 84), WHITE)
text_center(d, 290, "Before Ordering", font(FB, 84), WHITE)
d.line([340, 420, 940, 420], fill=(120, 200, 190), width=3)
text_center(d, 460, "Claude Code Expert  •  AI Agents  •  MCP Servers  •  Automations",
            font(FR, 30), (200, 240, 235))
text_center(d, 540, "Trigger  →  AI Agent  →  Sync", font(FB, 36), (200, 240, 235))
img.save(OUT / "07-cta.png")

print("slides:", sorted(p.name for p in OUT.glob("*.png")))
