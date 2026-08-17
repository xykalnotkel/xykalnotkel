from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path
import math
import random
import sys

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

SCENE = ASSETS / "xyspace_cosmic_scene_ai.png"
EMBLEM = ASSETS / "xyspace_emblem_ai.png"

W, H = 1200, 400
PURPLE = (119, 85, 185)
PURPLE_SOFT = (170, 145, 220)
WHITE = (246, 244, 250)
MUTED = (198, 193, 208)
INK = (10, 10, 15)


# ── Font resolution: Linux → macOS → Windows → Pillow default ──────────────

def _find_font(candidates: list[str]) -> str | None:
    """Return the first existing font path, or None."""
    for path in candidates:
        if Path(path).is_file():
            return path
    return None


FONT_BOLD = _find_font([
    # Linux (Debian/Ubuntu)
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    # macOS (Homebrew or system)
    "/Library/Fonts/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    # Windows
    "C:/Windows/Fonts/dejavusans-bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
])

FONT_REG = _find_font([
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/Library/Fonts/DejaVuSans.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "C:/Windows/Fonts/dejavusans.ttf",
    "C:/Windows/Fonts/arial.ttf",
])

FONT_MONO = _find_font([
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/Library/Fonts/DejaVuSansMono.ttf",
    "/System/Library/Fonts/SFNSMono.ttf",
    "C:/Windows/Fonts/dejavusansmono.ttf",
    "C:/Windows/Fonts/consola.ttf",
])

if not all([FONT_BOLD, FONT_REG, FONT_MONO]):
    missing = []
    if not FONT_BOLD:  missing.append("BOLD")
    if not FONT_REG:   missing.append("REGULAR")
    if not FONT_MONO:  missing.append("MONO")
    print(f"⚠  Font fallback: using Pillow default for {', '.join(missing)}.")
    print("   For best results, install DejaVu Sans or edit FONT_* paths.")


def fit_cover(im, size):
    tw, th = size
    ratio = max(tw / im.width, th / im.height)
    nw, nh = int(im.width * ratio), int(im.height * ratio)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return im.crop((left, top, left + tw, top + th))


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def draw_letterspaced(draw, xy, text, font, fill, spacing):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing


def make_base():
    scene = Image.open(SCENE).convert("RGB")
    scene = fit_cover(scene, (W, H))
    scene = ImageEnhance.Contrast(scene).enhance(1.04)
    base = scene.convert("RGBA")

    # Calm the left/middle zone so typography remains readable.
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for x in range(0, 790):
        alpha = int(178 * (1 - x / 900) ** 1.15)
        sd.line((x, 0, x, H), fill=(5, 5, 10, max(0, alpha)))
    base = Image.alpha_composite(base, shade)

    # Logo card and soft shadow.
    logo_size = 248
    lx, ly = 48, 76
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = ImageDraw.Draw(shadow)
    sh.rounded_rectangle((lx + 7, ly + 10, lx + logo_size + 7, ly + logo_size + 10), radius=42, fill=(0, 0, 0, 125))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    base = Image.alpha_composite(base, shadow)

    card = Image.new("RGBA", (logo_size, logo_size), (12, 12, 18, 248))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((1, 1, logo_size - 2, logo_size - 2), radius=40, outline=(130, 100, 184, 145), width=2)
    cd.rounded_rectangle((7, 7, logo_size - 8, logo_size - 8), radius=34, outline=(255, 255, 255, 24), width=1)

    emblem = Image.open(EMBLEM).convert("RGB")
    # Crop some empty margin from the AI emblem and keep its satin-black backdrop.
    emblem = emblem.crop((120, 120, 904, 904)).resize((218, 218), Image.Resampling.LANCZOS)
    emblem = ImageEnhance.Contrast(emblem).enhance(1.05)
    em_rgba = emblem.convert("RGBA")
    em_rgba.putalpha(rounded_mask((218, 218), 30))
    card.alpha_composite(em_rgba, (15, 15))
    base.alpha_composite(card, (lx, ly))

    # Precise typography rendered outside the AI model.
    d = ImageDraw.Draw(base)
    small = ImageFont.truetype(FONT_MONO, 15) if FONT_MONO else ImageFont.load_default()
    micro_bold = ImageFont.truetype(FONT_BOLD, 14) if FONT_BOLD else ImageFont.load_default()
    name_font = ImageFont.truetype(FONT_BOLD, 49) if FONT_BOLD else ImageFont.load_default()
    brand_font = ImageFont.truetype(FONT_BOLD, 26) if FONT_BOLD else ImageFont.load_default()
    sub_font = ImageFont.truetype(FONT_REG, 16) if FONT_REG else ImageFont.load_default()

    tx = 338
    d.rounded_rectangle((tx, 76, tx + 284, 108), radius=16, fill=(79, 52, 118, 190), outline=(168, 144, 211, 75), width=1)
    draw_letterspaced(d, (tx + 18, 83), "XYSPACE / CREATIVE TECH", micro_bold, WHITE, 0.7)

    d.text((tx, 128), "HAEKAL SAPUTRA", font=name_font, fill=(8, 7, 12, 170), stroke_width=5, stroke_fill=(8, 7, 12, 100))
    d.text((tx, 123), "HAEKAL SAPUTRA", font=name_font, fill=WHITE)
    d.text((tx + 2, 188), "APP DEVELOPMENT  •  WEB  •  GAME  •  AI  •  CLOUD", font=small, fill=PURPLE_SOFT)

    d.rounded_rectangle((tx, 235, tx + 488, 291), radius=16, fill=(12, 11, 18, 182), outline=(150, 125, 195, 72), width=1)
    d.ellipse((tx + 18, 255, tx + 26, 263), fill=PURPLE_SOFT)
    d.text((tx + 39, 249), "Building useful ideas beyond the ordinary.", font=sub_font, fill=MUTED)

    d.text((tx + 1, 324), "github.com/xykalnotkel", font=small, fill=(175, 168, 188))

    # A restrained purple baseline.
    d.rounded_rectangle((338, 355, 812, 359), radius=2, fill=(113, 75, 160, 138))
    d.rounded_rectangle((338, 355, 515, 359), radius=2, fill=(189, 166, 226, 205))
    return base


def draw_star(draw, x, y, r, fill):
    pts = [(x, y-r), (x+r*.28, y-r*.28), (x+r, y), (x+r*.28, y+r*.28),
           (x, y+r), (x-r*.28, y+r*.28), (x-r, y), (x-r*.28, y-r*.28)]
    draw.polygon(pts, fill=fill)


base = make_base()
base_rgb = base.convert("RGB")
base_rgb.save(ASSETS / "xyspace-header.png", "PNG", optimize=True)
# WebP — fast load (91% smaller), modern browsers
base_rgb.save(ASSETS / "xyspace-header.webp", "WEBP", quality=88, method=6)

# Avatar/app icon derived from the AI emblem, with safe inset and final sharpening.
em = Image.open(EMBLEM).convert("RGB")
em = ImageEnhance.Contrast(em).enhance(1.035)
em = em.resize((1024, 1024), Image.Resampling.LANCZOS)
em = em.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=4))
em.save(ASSETS / "xyspace-avatar.png", "PNG", optimize=True, dpi=(300, 300))
em.save(ASSETS / "xyspace-avatar.webp", "WEBP", quality=88, method=6)

# Animated hero: tiny drifting particles, twinkling stars, logo-orbit dots and a soft sweep.
random.seed(42)
particles = []
for _ in range(28):
    particles.append({
        "x": random.randint(18, W-18),
        "y": random.randint(24, H-24),
        "r": random.choice([1, 1, 1, 2, 2, 3]),
        "phase": random.random() * math.tau,
        "speed": random.uniform(.55, 1.4),
        "purple": random.random() < .62,
    })

frames = []
count = 32
for i in range(count):
    t = i / count
    frame = base.copy()
    fx = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(fx)

    for p in particles:
        xx = p["x"] + math.sin(math.tau * t * p["speed"] + p["phase"]) * 7
        yy = p["y"] + math.cos(math.tau * t * .72 + p["phase"]) * 4
        pulse = .55 + .45 * math.sin(math.tau * t + p["phase"]) ** 2
        color = (176, 145, 222, int(35 + 90*pulse)) if p["purple"] else (255, 255, 255, int(28 + 95*pulse))
        r = p["r"]
        d.ellipse((xx-r, yy-r, xx+r, yy+r), fill=color)

    for idx, (sx, sy, sr) in enumerate([(327, 55, 7), (870, 85, 5), (1028, 315, 6), (746, 42, 4)]):
        pulse = .35 + .65 * (math.sin(math.tau*t + idx*1.3) ** 2)
        draw_star(d, sx, sy, sr*(.7+.3*pulse), (238, 229, 250, int(48 + 150*pulse)))

    # Two dots orbit slowly around the emblem card.
    cx, cy = 172, 200
    for j, ang0 in enumerate((0, math.pi)):
        ang = math.tau*t + ang0
        ox = cx + math.cos(ang)*136
        oy = cy + math.sin(ang)*114
        rr = 3 if j == 0 else 2
        d.ellipse((ox-rr, oy-rr, ox+rr, oy+rr), fill=(180, 150, 224, 180 if j == 0 else 115))

    # Restrained satin sweep over the logo only.
    sweep_x = int(20 + t * 350)
    d.polygon([(sweep_x, 82), (sweep_x+20, 82), (sweep_x-72, 320), (sweep_x-92, 320)], fill=(255, 255, 255, 13))

    fx = fx.filter(ImageFilter.GaussianBlur(.25))
    frame = Image.alpha_composite(frame, fx).convert("RGB")
    frames.append(frame.quantize(colors=96, method=Image.Quantize.MEDIANCUT))

frames[0].save(
    ASSETS / "xyspace-header.gif",
    save_all=True,
    append_images=frames[1:],
    duration=90,
    loop=0,
    optimize=True,
    disposal=2,
)
# Animated WebP — ~80% smaller than GIF, same animation
try:
    # Rebuild RGB frames for WebP (avoid quantized palette)
    webp_frames = []
    for i in range(count):
        t = i / count
        frame = base.copy()
        fx = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(fx)
        for p in particles:
            xx = p["x"] + math.sin(math.tau * t * p["speed"] + p["phase"]) * 7
            yy = p["y"] + math.cos(math.tau * t * .72 + p["phase"]) * 4
            pulse = .55 + .45 * math.sin(math.tau * t + p["phase"]) ** 2
            color = (176, 145, 222, int(35 + 90*pulse)) if p["purple"] else (255, 255, 255, int(28 + 95*pulse))
            r = p["r"]
            d.ellipse((xx-r, yy-r, xx+r, yy+r), fill=color)
        for idx, (sx, sy, sr) in enumerate([(327, 55, 7), (870, 85, 5), (1028, 315, 6), (746, 42, 4)]):
            pulse = .35 + .65 * (math.sin(math.tau*t + idx*1.3) ** 2)
            draw_star(d, sx, sy, sr*(.7+.3*pulse), (238, 229, 250, int(48 + 150*pulse)))
        cx, cy = 172, 200
        for j, ang0 in enumerate((0, math.pi)):
            ang = math.tau*t + ang0
            ox = cx + math.cos(ang)*136
            oy = cy + math.sin(ang)*114
            rr = 3 if j == 0 else 2
            d.ellipse((ox-rr, oy-rr, ox+rr, oy+rr), fill=(180, 150, 224, 180 if j == 0 else 115))
        sweep_x = int(20 + t * 350)
        d.polygon([(sweep_x, 82), (sweep_x+20, 82), (sweep_x-72, 320), (sweep_x-92, 320)], fill=(255, 255, 255, 13))
        fx = fx.filter(ImageFilter.GaussianBlur(.25))
        webp_frame = Image.alpha_composite(frame, fx).convert("RGB")
        webp_frames.append(webp_frame)
    webp_frames[0].save(
        ASSETS / "xyspace-header-animated.webp",
        save_all=True,
        append_images=webp_frames[1:],
        duration=90,
        loop=0,
        quality=82,
        method=4,
    )
except Exception as e:
    print(f"WebP animated skipped: {e}")

# Social preview uses the same art direction in GitHub's preview proportion.
SW, SH = 1280, 640
social_bg = Image.new("RGB", (SW, SH), (10, 10, 15))
header_big = base_rgb.resize((SW, int(H * SW / W)), Image.Resampling.LANCZOS)
y = (SH - header_big.height) // 2
social_bg.paste(header_big, (0, y))
# Fade top/bottom into charcoal.
ov = Image.new("RGBA", (SW, SH), (0,0,0,0))
od = ImageDraw.Draw(ov)
for yy in range(SH):
    edge = min(yy, SH-1-yy)
    alpha = int(max(0, 1-edge/135)*205)
    if alpha:
        od.line((0,yy,SW,yy), fill=(9,9,14,alpha))
social_bg = Image.alpha_composite(social_bg.convert('RGBA'),ov).convert('RGB')
social_bg.save(ASSETS / "xyspace-social-preview.png", "PNG", optimize=True)
social_bg.save(ASSETS / "xyspace-social-preview.webp", "WEBP", quality=85, method=6)

# Also convert source AI assets to WebP for faster dev (keeps PNG as fallback)
for src_name in ["xyspace_cosmic_scene_ai.png", "xyspace_emblem_ai.png"]:
    src = ASSETS / src_name
    if src.exists():
        Image.open(src).convert("RGB").save(src.with_suffix(".webp"), "WEBP", quality=82, method=6)

print("Generated:")
for name in ["xyspace-header.png", "xyspace-header.webp", "xyspace-header.gif", "xyspace-header-animated.webp", "xyspace-avatar.png", "xyspace-avatar.webp", "xyspace-social-preview.png", "xyspace-social-preview.webp"]:
    p = ASSETS / name
    if p.exists():
        print(f"  ✓ {p.name} ({p.stat().st_size:,} bytes)")
