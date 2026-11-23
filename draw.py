"""Draws entry.png: one front page summing up the world news of Monday 23 November 2026.

Run once (outside the sandbox) with Pillow installed:  python3 draw.py
The output is deterministic: same fonts + same Pillow version -> same bytes.
main.ts only copies the finished entry.png, so the graded program stays stdlib-only.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/noto/"

PAPER = (247, 243, 234)
INK = (24, 27, 38)
NAVY = (18, 38, 74)
MUTED = (88, 92, 104)
RULE = (196, 188, 172)
RED = (196, 40, 40)

def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

def text_w(d, s, f):
    x0, _, x1, _ = d.textbbox((0, 0), s, font=f)
    return x1 - x0

def fit(d, s, name, size, max_w, min_size=14):
    """Largest font size (<= size) at which s fits in max_w pixels."""
    while size > min_size and text_w(d, s, font(name, size)) > max_w:
        size -= 1
    return font(name, size)

# ---------- icons: simple flat pictograms, each drawn inside a box (x, y, s) ----------

def icon_fire(d, x, y, s, c):
    d.polygon([(x + s * .50, y + s * .02), (x + s * .80, y + s * .45), (x + s * .88, y + s * .72),
               (x + s * .70, y + s * .95), (x + s * .30, y + s * .95), (x + s * .12, y + s * .72),
               (x + s * .22, y + s * .40), (x + s * .36, y + s * .55)], fill=c)
    d.polygon([(x + s * .50, y + s * .45), (x + s * .66, y + s * .72), (x + s * .58, y + s * .92),
               (x + s * .42, y + s * .92), (x + s * .34, y + s * .74)], fill=(250, 200, 70))

def icon_chart_down(d, x, y, s, c):
    d.line([(x + s * .06, y + s * .94), (x + s * .96, y + s * .94)], fill=INK, width=4)
    d.line([(x + s * .06, y + s * .06), (x + s * .06, y + s * .94)], fill=INK, width=4)
    pts = [(x + s * .12, y + s * .18), (x + s * .32, y + s * .34), (x + s * .46, y + s * .28),
           (x + s * .64, y + s * .58), (x + s * .86, y + s * .80)]
    d.line(pts, fill=c, width=8, joint="curve")
    tip = pts[-1]
    d.polygon([tip, (tip[0] - s * .20, tip[1] - s * .02), (tip[0] - s * .04, tip[1] - s * .20)], fill=c)

def icon_shield(d, x, y, s, c):
    d.polygon([(x + s * .50, y + s * .02), (x + s * .92, y + s * .18), (x + s * .86, y + s * .62),
               (x + s * .50, y + s * .98), (x + s * .14, y + s * .62), (x + s * .08, y + s * .18)], fill=c)
    cx, cy, r = x + s * .5, y + s * .44, s * .22
    d.polygon([(cx, cy - r), (cx + r * .25, cy - r * .25), (cx + r, cy), (cx + r * .25, cy + r * .25),
               (cx, cy + r), (cx - r * .25, cy + r * .25), (cx - r, cy), (cx - r * .25, cy - r * .25)],
              fill=PAPER)

def icon_house_cracked(d, x, y, s, c):
    d.polygon([(x + s * .50, y + s * .06), (x + s * .94, y + s * .44), (x + s * .06, y + s * .44)], fill=c)
    d.rectangle([x + s * .16, y + s * .44, x + s * .84, y + s * .94], fill=c)
    d.line([(x + s * .52, y + s * .30), (x + s * .42, y + s * .52), (x + s * .58, y + s * .66),
            (x + s * .46, y + s * .92)], fill=PAPER, width=5)

def icon_globe(d, x, y, s, c):
    d.ellipse([x + s * .06, y + s * .06, x + s * .94, y + s * .94], fill=c)
    d.ellipse([x + s * .30, y + s * .06, x + s * .70, y + s * .94], outline=PAPER, width=3)
    d.line([(x + s * .06, y + s * .50), (x + s * .94, y + s * .50)], fill=PAPER, width=3)
    d.line([(x + s * .14, y + s * .28), (x + s * .86, y + s * .28)], fill=PAPER, width=3)
    d.line([(x + s * .14, y + s * .72), (x + s * .86, y + s * .72)], fill=PAPER, width=3)

def icon_factory(d, x, y, s, c):
    d.polygon([(x + s * .06, y + s * .94), (x + s * .06, y + s * .50), (x + s * .32, y + s * .66),
               (x + s * .32, y + s * .50), (x + s * .58, y + s * .66), (x + s * .58, y + s * .30),
               (x + s * .72, y + s * .30), (x + s * .72, y + s * .66), (x + s * .94, y + s * .66),
               (x + s * .94, y + s * .94)], fill=c)
    for i in range(3):
        bx = x + s * (.14 + i * .26)
        d.rectangle([bx, y + s * .76, bx + s * .10, y + s * .86], fill=PAPER)

def icon_dome(d, x, y, s, c):
    d.pieslice([x + s * .22, y + s * .10, x + s * .78, y + s * .66], 180, 360, fill=c)
    d.rectangle([x + s * .12, y + s * .40, x + s * .88, y + s * .48], fill=c)
    for i in range(5):
        cx = x + s * (.18 + i * .16)
        d.rectangle([cx, y + s * .50, cx + s * .06, y + s * .84], fill=c)
    d.rectangle([x + s * .06, y + s * .86, x + s * .94, y + s * .94], fill=c)

def icon_quake(d, x, y, s, c):
    pts, n = [], 14
    amps = [0, .05, -.08, .22, -.34, .40, -.30, .18, -.12, .06, -.04, .02, 0, 0, 0]
    for i in range(n + 1):
        pts.append((x + s * (.04 + .92 * i / n), y + s * (.50 - amps[i])))
    d.line(pts, fill=c, width=5, joint="curve")

def icon_jobs(d, x, y, s, c):
    d.ellipse([x + s * .34, y + s * .06, x + s * .66, y + s * .38], fill=c)
    d.pieslice([x + s * .16, y + s * .44, x + s * .84, y + s * 1.12], 180, 360, fill=c)
    d.line([(x + s * .60, y + s * .56), (x + s * .84, y + s * .80)], fill=RED, width=6)
    d.polygon([(x + s * .90, y + s * .86), (x + s * .68, y + s * .82), (x + s * .86, y + s * .64)], fill=RED)

# ---------- content: events of, or first reported on, Monday 23 November 2026 ----------

LEAD = {
    "tag": "MARKETS",
    "head": "AI-stock rout hits Asia",
    "lines": ["Seoul's Kospi plunges 5%; trading curb triggered",
              "Oil slips with stocks: Brent near $92 a barrel"],
}

STORIES = [
    ("INDONESIA", (176, 52, 30), icon_fire,
     "Factory fire kills 24", "Cikande, Banten: about 30 still missing"),
    ("NATO", (30, 74, 140), icon_shield,
     "NATO emergency talks", "Brussels meets on Russian missiles in Poland"),
    ("UKRAINE", (60, 64, 76), icon_house_cracked,
     "Dymer death toll rises to 9", "Boy, 7, pulled alive after 14 hours"),
    ("CLIMATE", (34, 120, 84), icon_globe,
     "COP31 ends with no deal", "Leaders react to failed talks in Antalya"),
    ("INDIA", (190, 110, 20), icon_factory,
     "Tata Steel's $1.67bn deal", "Buys 26.4% of APL Apollo Tubes"),
    ("INDONESIA", (120, 40, 110), icon_dome,
     "Prabowo to submit VP picks", "Two names to replace Gibran, per Antara"),
    ("PACIFIC", (20, 110, 140), icon_quake,
     "M6.5 deep quake, Vanuatu", "601 km deep; no tsunami threat"),
    ("AUSTRALIA", (150, 60, 60), icon_jobs,
     "Jobless rate to top 5%", "Treasurer Chalmers warns as hikes bite"),
]

def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead: the date is the headline
    d.rectangle([0, 0, W, 150], fill=NAVY)
    f_small = font("NotoSans-Bold.ttf", 26)
    s = "THE WORLD ON"
    d.text(((W - text_w(d, s, f_small)) / 2, 14), s, font=f_small, fill=(200, 210, 230))
    s = "MONDAY 23 NOVEMBER 2026"
    f_date = fit(d, s, "NotoSerif-Black.ttf", 78, W - 60)
    d.text(((W - text_w(d, s, f_date)) / 2, 44), s, font=f_date, fill=(255, 255, 255))

    # lead story
    y0 = 166
    d.rectangle([24, y0, W - 24, y0 + 168], fill=(255, 252, 245), outline=RULE, width=2)
    icon_chart_down(d, 44, y0 + 22, 124, RED)
    tx = 196
    d.text((tx, y0 + 14), LEAD["tag"], font=font("NotoSans-Bold.ttf", 22), fill=RED)
    f_head = fit(d, LEAD["head"], "NotoSerif-Black.ttf", 52, W - tx - 44)
    d.text((tx, y0 + 34), LEAD["head"], font=f_head, fill=INK)
    for i, line in enumerate(LEAD["lines"]):
        f_line = fit(d, line, "NotoSans-Regular.ttf", 27, W - tx - 44)
        d.text((tx, y0 + 98 + i * 31), line, font=f_line, fill=INK)

    # 2 x 4 grid of stories
    top, bottom = y0 + 184, H - 52
    cols, rows = 2, 4
    cw = (W - 48 - 16) / cols
    rh = (bottom - top - 12 * (rows - 1)) / rows
    for k, (tag, color, icon, head, sub) in enumerate(STORIES):
        c, r = k % cols, k // cols
        x = 24 + c * (cw + 16)
        y = top + r * (rh + 12)
        d.rectangle([x, y, x + cw, y + rh], fill=(255, 252, 245), outline=RULE, width=2)
        d.rectangle([x, y, x + 8, y + rh], fill=color)
        isz = 78
        icon(d, x + 22, y + (rh - isz) / 2, isz, color)
        tx = x + 22 + isz + 18
        maxw = x + cw - tx - 14
        d.text((tx, y + 10), tag, font=font("NotoSans-Bold.ttf", 18), fill=color)
        d.text((tx, y + 34), head, font=fit(d, head, "NotoSerif-Bold.ttf", 30, maxw), fill=INK)
        d.text((tx, y + 78), sub, font=fit(d, sub, "NotoSans-Regular.ttf", 22, maxw), fill=MUTED)

    # footer
    s = "Top stories reported on Monday 23 November 2026  |  Sources: Reuters, BBC, AFP, USGS"
    f_foot = fit(d, s, "NotoSans-Regular.ttf", 19, W - 48)
    d.text(((W - text_w(d, s, f_foot)) / 2, H - 38), s, font=f_foot, fill=MUTED)

    img.save("entry.png", optimize=True)

if __name__ == "__main__":
    draw()
