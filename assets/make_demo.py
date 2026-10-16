#!/usr/bin/env python3
"""Generate the Super-Memory 15s demo GIF (terminal animation)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 820, 470
LH = 27            # line height
TOP = 54           # first content line y
PADX = 24
TITLE_H = 38

# Catppuccin Mocha-ish palette
BG     = (30, 30, 46)
TITLE  = (24, 24, 37)
TEXT   = (205, 214, 244)
DIM    = (108, 112, 134)
GREEN  = (166, 227, 161)
MAUVE  = (203, 166, 247)
GOLD   = (249, 226, 175)
BLUE   = (137, 180, 250)
RED    = (243, 139, 168)
CURSOR = (205, 214, 244)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FBB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
font = ImageFont.truetype(FB, 18)
fontb = ImageFont.truetype(FBB, 18)
small = ImageFont.truetype(FB, 13)

frames, durations = [], []


def seglen(d, segs):
    return sum(d.textlength(t, font=(fontb if b else font)) for t, b, _ in segs)


def slice_segs(segs, n):
    out, c = [], 0
    for t, b, col in segs:
        if c >= n:
            break
        take = min(len(t), n - c)
        out.append((t[:take], b, col))
        c += take
    return out


def render(lines, partial=None, cursor=False):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, TITLE_H], fill=TITLE)
    for i, col in enumerate((RED, GOLD, GREEN)):
        d.ellipse([18 + i * 20, 14, 30 + i * 20, 26], fill=col)
    d.text((W // 2, TITLE_H // 2), "Claude Code", font=small, fill=DIM, anchor="mm")

    rows = list(lines) + ([partial] if partial is not None else [])
    for r, segs in enumerate(rows):
        x = PADX
        y = TOP + r * LH
        for t, b, col in segs:
            d.text((x, y), t, font=(fontb if b else font), fill=col)
            x += d.textlength(t, font=(fontb if b else font))
    if cursor and partial is not None:
        cx = PADX + seglen(d, partial)
        cy = TOP + len(lines) * LH
        d.rectangle([cx + 1, cy + 2, cx + 11, cy + 23], fill=CURSOR)
    return img


def frame(img, ms):
    frames.append(img)
    durations.append(ms)


def hold(lines, ms, partial=None, cursor=False):
    frame(render(lines, partial, cursor), ms)


def type_line(lines, segs, step=3, ms=52, end_pause=260):
    """Typewriter-reveal a line, then commit it to `lines`."""
    total = sum(len(t) for t, _, _ in segs)
    for i in range(0, total + 1, step):
        frame(render(lines, slice_segs(segs, i), cursor=True), ms)
    hold(lines, end_pause, partial=segs, cursor=True)
    lines.append(segs)


def out_line(lines, segs, ms=360):
    """Show an output line instantly."""
    lines.append(segs)
    hold(lines, ms)


# ---- Scene 1: say something once --------------------------------------
L = []
type_line(L, [("$ ", False, GREEN), ("claude", False, TEXT)], step=3, ms=40, end_pause=180)
out_line(L, [("", False, TEXT)], ms=120)
type_line(L, [("> ", False, GREEN),
              ("from now on, deploy Capta every Friday at 6pm", False, TEXT)])
hold(L, 450)
out_line(L, [("● ", False, MAUVE), ("Got it.", False, TEXT)], ms=650)
type_line(L, [("> ", False, GREEN), ("thanks, that's all", False, TEXT)])
hold(L, 500)

# ---- Scene 2: Super-Memory quietly captures ---------------------------
out_line(L, [("— session ended —", False, DIM)], ms=500)
out_line(L, [("◆ Super-Memory", False, GOLD), ("  distilling…", False, DIM)], ms=800)
out_line(L, [("  ✓ saved: ", False, GREEN), ("capta-deploy-schedule", False, DIM)], ms=500)
hold(L, 1900)

# ---- Scene 3: days later, it remembers --------------------------------
L2 = [[("— days later, new session —", False, DIM)]]
hold(L2, 900)
type_line(L2, [("$ ", False, GREEN), ("claude", False, TEXT)], step=3, ms=40, end_pause=160)
type_line(L2, [("> ", False, GREEN), ("/memory-review", False, BLUE)])
hold(L2, 450)
out_line(L2, [("◆ Super-Memory", True, GOLD), (" — 1 fact remembered:", False, TEXT)], ms=500)
out_line(L2, [("  1. Capta deploy schedule", False, TEXT)], ms=450)
out_line(L2, [("     \"Deploy Capta every Friday at 6pm\"", False, BLUE)], ms=700)
out_line(L2, [("", False, TEXT)], ms=120)
out_line(L2, [("✓ Claude already knows. You wrote nothing.", False, GREEN)], ms=600)
hold(L2, 2600)

total = sum(durations)
print(f"frames={len(frames)}  total={total/1000:.1f}s")

# Clean quantization: one shared adaptive palette, NO dithering, so flat areas
# stay noise-free and the file compresses well.
base = frames[0].convert("RGB").quantize(colors=64, method=Image.MEDIANCUT,
                                         dither=Image.NONE)
qframes = [f.convert("RGB").quantize(palette=base, dither=Image.NONE)
           for f in frames]

out = os.path.join(os.path.dirname(__file__), "demo.gif")
qframes[0].save(out, save_all=True, append_images=qframes[1:],
                duration=durations, loop=0, optimize=True, disposal=2)
print("wrote", out, f"{os.path.getsize(out)/1024:.0f} KB")

# save representative frames for visual QA
frames[-1].save(os.path.join(os.path.dirname(__file__), "_lastframe.png"))
frames[len(frames) // 2].save(os.path.join(os.path.dirname(__file__), "_midframe.png"))
