"""Generate a Foundry Toolkit-focused Build recap deck.

    python deck/build_deck.py

Produces: deck/Build2026-Recap-Agents.pptx
"""

from __future__ import annotations

import pathlib

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR
from pptx.util import Emu, Pt

# Palette
AZURE = RGBColor(0x00, 0x78, 0xD4)
DARK = RGBColor(0x20, 0x20, 0x20)
GREY = RGBColor(0x60, 0x60, 0x60)
CODEBG = RGBColor(0x1E, 0x1E, 0x1E)
CODEFG = RGBColor(0xE6, 0xE6, 0xE6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

# 16:9
W = Emu(12192000)
H = Emu(6858000)

prs = Presentation()
prs.slide_width = W
prs.slide_height = H
BLANK = prs.slide_layouts[6]


def _tb(slide, left, top, width, height):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    return box, tf


def _fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def _band(slide, color=AZURE, height=Emu(120000), top=Emu(0)):
    from pptx.enum.shapes import MSO_SHAPE

    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, top, W, height)
    _fill(bar, color)
    return bar


def notes(slide, text: str):
    slide.notes_slide.notes_text_frame.text = text.strip()


def title_slide(title: str, subtitle: str, footer: str):
    s = prs.slides.add_slide(BLANK)
    bg = s.shapes.add_shape(1, 0, 0, W, H)
    _fill(bg, AZURE)
    _, tf = _tb(s, Emu(700000), Emu(2200000), Emu(10800000), Emu(2200000))
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = title
    r.font.size = Pt(44)
    r.font.bold = True
    r.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    r2 = p2.add_run()
    r2.text = subtitle
    r2.font.size = Pt(22)
    r2.font.color.rgb = RGBColor(0xE8, 0xF0, 0xFB)

    _, ff = _tb(s, Emu(700000), Emu(5900000), Emu(10800000), Emu(500000))
    fr = ff.paragraphs[0].add_run()
    fr.text = footer
    fr.font.size = Pt(14)
    fr.font.color.rgb = RGBColor(0xD6, 0xE6, 0xF7)
    return s


def section_slide(kicker: str, title: str):
    s = prs.slides.add_slide(BLANK)
    bg = s.shapes.add_shape(1, 0, 0, W, H)
    _fill(bg, DARK)
    _, tf = _tb(s, Emu(700000), Emu(2700000), Emu(10800000), Emu(1600000))
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = kicker.upper()
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = AZURE
    p2 = tf.add_paragraph()
    r2 = p2.add_run()
    r2.text = title
    r2.font.size = Pt(40)
    r2.font.bold = True
    r2.font.color.rgb = WHITE
    return s


def content_slide(title: str, bullets, subtitle: str | None = None):
    s = prs.slides.add_slide(BLANK)
    _band(s)
    _, tt = _tb(s, Emu(600000), Emu(300000), Emu(11000000), Emu(900000))
    tr = tt.paragraphs[0].add_run()
    tr.text = title
    tr.font.size = Pt(30)
    tr.font.bold = True
    tr.font.color.rgb = DARK
    if subtitle:
        sp = tt.add_paragraph()
        sr = sp.add_run()
        sr.text = subtitle
        sr.font.size = Pt(15)
        sr.font.italic = True
        sr.font.color.rgb = GREY

    _, bf = _tb(s, Emu(700000), Emu(1500000), Emu(10800000), Emu(4900000))
    first = True
    for text, level in bullets:
        p = bf.paragraphs[0] if first else bf.add_paragraph()
        first = False
        p.level = level
        run = p.add_run()
        bullet = "•  " if level == 0 else "–  "
        run.text = bullet + text
        run.font.size = Pt(20 - level * 2)
        run.font.color.rgb = DARK if level == 0 else GREY
        p.space_after = Pt(6)
    return s


def code_slide(title: str, code: str, caption: str | None = None):
    s = prs.slides.add_slide(BLANK)
    _band(s)
    _, tt = _tb(s, Emu(600000), Emu(300000), Emu(11000000), Emu(800000))
    tr = tt.paragraphs[0].add_run()
    tr.text = title
    tr.font.size = Pt(28)
    tr.font.bold = True
    tr.font.color.rgb = DARK

    panel = s.shapes.add_shape(1, Emu(600000), Emu(1350000), Emu(11000000), Emu(4650000))
    _fill(panel, CODEBG)
    tf = panel.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Emu(200000)
    tf.margin_top = Emu(150000)
    first = True
    for line in code.strip("\n").split("\n"):
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        r = p.add_run()
        r.text = line if line else " "
        r.font.name = "Menlo"
        r.font.size = Pt(14)
        r.font.color.rgb = CODEFG

    if caption:
        _, cf = _tb(s, Emu(600000), Emu(6150000), Emu(11000000), Emu(500000))
        cr = cf.paragraphs[0].add_run()
        cr.text = caption
        cr.font.size = Pt(13)
        cr.font.italic = True
        cr.font.color.rgb = GREY
    return s


# Slides
s = title_slide(
    "Foundry Toolkit for VS Code",
    "A simple, practical Build 2026 recap session\nfocused on the in-editor AI dev loop",
    "Metro Toronto Azure Community · 25-minute session",
)
notes(
    s,
    """
    Today is intentionally focused on one thing: Foundry Toolkit for VS Code.
    No deep framework internals. Just a repeatable workflow attendees can use right away.
    """,
)

s = content_slide(
    "What changed at Build (and why this matters)",
    [
        ("Foundry Toolkit for VS Code is now GA", 0),
        ("The full agent dev loop now lives in the editor", 0),
        ("Faster iteration: discover → test → generate → inspect → evaluate", 0),
        ("Lower risk demos and easier onboarding for new teams", 0),
    ],
)
notes(s, "Set context quickly: this is a productivity and reliability story.")

s = content_slide(
    "Session agenda — 25 minutes",
    [
        ("What the toolkit is (2-3 min)", 0),
        ("Live loop in VS Code (catalog, playground, builder, inspector)", 0),
        ("Tracing + evaluation in the same workflow", 0),
        ("Practical checklist and fallback plan", 0),
    ],
)
notes(s, "Tell audience this is hands-on and reproducible.")

s = section_slide("Live workflow", "One loop, six toolkit features")
notes(s, "Transition into live walkthrough.")

s = content_slide(
    "1) Model Catalog",
    [
        ("Pick a model you already have access to", 0),
        ("Explain provider flexibility and model selection criteria", 0),
        ("Keep this short — goal is to start testing quickly", 0),
    ],
    subtitle="Outcome: model selected for playground + builder",
)

s = content_slide(
    "2) Playground",
    [
        ("Paste prompt from foundry-toolkit/agent-builder-prompt.md", 0),
        ("Run a couple prompt variations", 0),
        ("Tune style, tone, and parameters before code generation", 0),
    ],
    subtitle="Outcome: prompt validated before coding",
)

s = content_slide(
    "3) Agent Builder + 4) Agent Inspector",
    [
        ("Generate agent scaffold directly from tested prompt", 0),
        ("Show generated structure and how to run it locally", 0),
        ("Use Agent Inspector to visualize turns and debug behavior", 0),
    ],
    subtitle="Outcome: prompt becomes runnable code with observability",
)

s = code_slide(
    "Run the baseline sample",
    """
source .venv/bin/activate
make single

# Optional backend switch in .env
MODEL_BACKEND=foundry
FOUNDRY_PROJECT_ENDPOINT=<your-project-endpoint>
FOUNDRY_MODEL=<your-model-or-deployment>
""",
    caption="demos/00_single_agent.py is the simplest runtime demo path",
)
notes(s, "Run one clean sample during the session to keep it simple and reliable.")

s = code_slide(
    "5) Tracing",
    """
# in .env
ENABLE_TRACING=true

# tracing wiring in code
from agent_framework.observability import configure_otel_providers
configure_otel_providers(vs_code_extension_port=4317)

make single
""",
    caption="Show spans in Foundry Toolkit Tracing panel after the run",
)
notes(s, "Explain that tracing gives transparent execution details for debugging and trust.")

s = content_slide(
    "6) Evaluation",
    [
        ("Load foundry-toolkit/evaluation/dataset.jsonl", 0),
        ("Run built-in evaluators and compare variants", 0),
        ("Use results as quality gates before broader rollout", 0),
    ],
    subtitle="Outcome: measurable quality, not guesswork",
)

s = content_slide(
    "Demo checklist you can reuse",
    [
        ("Preflight: smoke test + single-agent run", 0),
        ("Keep one golden prompt and one fallback backend", 0),
        ("Prefer one successful end-to-end loop over many partial demos", 0),
        ("If issues occur, pivot to Inspector/Tracing screenshots and continue", 0),
    ],
)

s = content_slide(
    "Resources",
    [
        ("Foundry Toolkit overview: code.visualstudio.com/docs/intelligentapps/overview", 0),
        ("Install link: aka.ms/foundrytk", 0),
        ("Session runbook: docs/DEMO_SCRIPT.md", 0),
        ("Toolkit demo guide: foundry-toolkit/README.md", 0),
        ("Repo: github.com/hkaanturgut/agent-framework-foundry-demo", 0),
    ],
)

s = title_slide(
    "Thank you!",
    "Questions?\nIf you only remember one thing: run the full loop inside VS Code.",
    "Foundry Toolkit for VS Code · Build 2026 Recap",
)

out = pathlib.Path(__file__).resolve().parent / "Build2026-Recap-Agents.pptx"
prs.save(out)
print(f"Wrote {out} ({len(prs.slides)} slides)")

