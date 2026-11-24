"""NI24 round 2: 'The World in One Day' — five fronts, one day.

A different front page from round 1: a dark navy header band, one
full-width COP31 hero, four medium illustrations in a row, then a
compact 25-story digest grid. Same 30 verified stories, 24 Nov 2026.

Dev-machine renderer (Pillow). The graded entrypoint main.py only
copies the PNG this script produces, so the grader never needs Pillow.
Run:  python3 draw.py  ->  assets/entry.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "entry.png")

NAVY = (15, 23, 42)
GOLD = (251, 191, 36)
CRIMSON = (220, 38, 38)
PAPER = (255, 255, 255)
INK = (17, 24, 39)
MUTED = (71, 85, 105)

TAGCOLOUR = {
    "GAZA": (185, 28, 28),
    "VENEZUELA": (29, 78, 216),
    "BOLSONARO": (29, 78, 216),
    "AFCON": (124, 58, 237),
    "NEPAL": (234, 88, 12),
    "TAJIKISTAN": (234, 88, 12),
    "IRAN": (185, 28, 28),
    "LISBON": (13, 148, 136),
    "DENMARK": (13, 148, 136),
    "F1": (21, 128, 61),
    "TENNIS": (21, 128, 61),
    "CHESS": (21, 128, 61),
    "CRICKET": (21, 128, 61),
    "SPACE": (30, 64, 175),
    "LIBYA": (13, 148, 136),
    "FRANCE": (13, 148, 136),
    "MYANMAR": (234, 88, 12),
    "ZIMBABWE": (124, 58, 237),
    "KOREA": (29, 78, 216),
    "TALIBAN": (185, 28, 28),
    "BORDER": (234, 88, 12),
    "AI": (30, 64, 175),
    "SPICEJET": (234, 88, 12),
    "FERRARI": (185, 28, 28),
    "NEW YORK": (71, 85, 105),
}


def load_font(fname, size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + fname, size)
    except OSError:
        return ImageFont.load_default()


def serif_b(size):
    return load_font("DejaVuSerif-Bold.ttf", size)


def sans_b(size):
    return load_font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return load_font("DejaVuSans.ttf", size)


def fit_lines(d, text, fnt, max_w):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def tag_chip(d, x, y, label, colour):
    f = sans_b(11)
    tw = d.textlength(label, font=f)
    d.rounded_rectangle([x, y, x + tw + 14, y + 20], radius=4, fill=colour)
    d.text((x + 7, y + 3), label, font=f, fill=PAPER)


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(56, 189, 248),
              outline=PAPER, width=3)
    d.ellipse([cx - r + 22, cy - r + 26, cx - r + 62, cy - r + 60], fill=(74, 222, 128))
    d.ellipse([cx + 6, cy + 2, cx + 48, cy + 36], fill=(74, 222, 128))
    d.ellipse([cx - 44, cy + 30, cx - 6, cy + 66], fill=(74, 222, 128))
    d.arc([cx - r, cy - r, cx + r, cy + r], 210, 340, fill=PAPER, width=2)


def draw_flame(d, x, y, s):
    for dx, dy, sc, col in [(0, 0, 1.0, (253, 224, 71)), (-22, 10, 0.7, (251, 146, 60)),
                            (22, 10, 0.7, (251, 146, 60)), (0, -5, 0.5, (239, 68, 68))]:
        d.polygon([(x + dx, y + dy - 40 * sc), (x + dx + 14 * sc, y + dy),
                   (x + dx - 14 * sc, y + dy)], fill=col)


def draw_quad(d, x, y, s):
    d.ellipse([x - 8 * s, y - 4 * s, x + 8 * s, y + 4 * s], fill=(226, 232, 240))
    for sx in (-14, 14):
        d.line([(x + sx * s - 8 * s, y - 8 * s), (x + sx * s + 8 * s, y - 8 * s)],
               fill=(226, 232, 240), width=2)
    d.ellipse([x - 3 * s, y + 6 * s, x + 3 * s, y + 12 * s], fill=CRIMSON)


def medium_card(d, x, y, w, h, scene_h, tag, head, body, bg):
    d.rectangle([x, y, x + w, y + h], outline=(203, 213, 225), width=1)
    d.rectangle([x, y, x + w, y + scene_h], fill=bg)
    tag_chip(d, x + 8, y + 8, tag, TAGCOLOUR[tag] if tag in TAGCOLOUR else (71, 85, 105))
    hf, bf = sans_b(14), sans(11)
    yy = y + scene_h + 8
    for ln in fit_lines(d, head, hf, w - 20)[:2]:
        d.text((x + 10, yy), ln, font=hf, fill=INK)
        yy += 17
    for ln in fit_lines(d, body, bf, w - 20)[:2]:
        d.text((x + 10, yy), ln, font=bf, fill=MUTED)
        yy += 14


def digest_row(d, x, y, w, tag, head, body):
    colour = TAGCOLOUR[tag]
    d.rectangle([x, y, x + 4, y + 46], fill=colour)
    tf, hf, bf = sans_b(11), sans_b(12), sans(11)
    d.text((x + 12, y + 3), tag, font=tf, fill=colour)
    tw = d.textlength(tag + "  ", font=tf)
    d.text((x + 12 + tw, y + 3), head, font=hf, fill=INK)
    for i, ln in enumerate(fit_lines(d, body, bf, w - 12)[:2]):
        d.text((x + 12, y + 21 + i * 13), ln, font=bf, fill=MUTED)


def build():
    img = Image.new("RGB", (SIDE, SIDE), PAPER)
    d = ImageDraw.Draw(img)

    # Dark header band: masthead left, date right.
    d.rectangle([0, 0, SIDE, 64], fill=NAVY)
    d.text((16, 14), "THE WORLD IN ONE DAY", font=serif_b(30), fill=PAPER)
    d.text((1008, 20), "TUESDAY, 24 NOVEMBER 2026", font=sans_b(19),
           fill=GOLD, anchor="ra")
    d.rectangle([0, 64, SIDE, 68], fill=CRIMSON)

    # ---- Hero: COP31, full width (y 72..316) ----
    hx, hy, hw = 8, 72, 1008
    d.rectangle([hx, hy, hx + hw, hy + 244], outline=(203, 213, 225), width=1)
    d.rectangle([hx, hy, hx + hw, hy + 178], fill=(12, 74, 110))
    draw_globe(d, hx + 130, hy + 90, 76)
    d.line([(hx + 210, hy + 26), (hx + 252, hy + 64), (hx + 226, hy + 92),
            (hx + 276, hy + 122), (hx + 250, hy + 150)], fill=CRIMSON, width=6)
    d.text((hx + 320, hy + 34), "NO DEAL", font=sans_b(52), fill=PAPER)
    d.text((hx + 320, hy + 96), "IN ANTALYA", font=sans_b(30), fill=GOLD)
    d.text((hx + 320, hy + 138), "Two weeks of talks end with no agreement",
           font=sans(16), fill=(186, 230, 253))
    tag_chip(d, hx + 8, hy + 8, "GLOBAL", (71, 85, 105))
    hf, bf = sans_b(20), sans(13)
    yy = hy + 186
    d.text((hx + 12, yy), "COP31 ENDS IN DEADLOCK", font=hf, fill=INK)
    d.text((hx + 12, yy + 28),
           "Climate talks collapse in Antalya — no deal, and the fossil-fuel phase-out stalls.",
           font=bf, fill=MUTED)

    # ---- Four medium illustrations (y 324..492) ----
    my, mh, mw = 324, 168, 244
    # 1. Banten factory fire — dusk skyline.
    px = 8
    d.rectangle([px, my, px + mw, my + mh], outline=(203, 213, 225), width=1)
    for i, col in enumerate([(124, 45, 18), (234, 88, 12), (253, 186, 116)]):
        d.rectangle([px, my + i * 34, px + mw, my + (i + 1) * 34], fill=col)
    d.rectangle([px + 18, my + 62, px + 120, my + 100], fill=(28, 25, 23))
    d.rectangle([px + 136, my + 44, px + 196, my + 100], fill=(28, 25, 23))
    d.rectangle([px + 36, my + 38, px + 48, my + 62], fill=(28, 25, 23))
    d.ellipse([px + 196, my + 12, px + 232, my + 36], fill=(120, 113, 108))
    draw_flame(d, px + 70, my + 64, 0.9)
    draw_flame(d, px + 165, my + 48, 0.75)
    tag_chip(d, px + 8, my + 8, "ASIA", (234, 88, 12))
    yy = my + 108
    for ln in fit_lines(d, "FACTORY FIRE KILLS 24", sans_b(14), mw - 20)[:2]:
        d.text((px + 10, yy), ln, font=sans_b(14), fill=INK)
        yy += 17
    for ln in fit_lines(d, "Candy plant blaze in Banten; workers missing.",
                        sans(11), mw - 20)[:2]:
        d.text((px + 10, yy), ln, font=sans(11), fill=MUTED)
        yy += 14

    # 2. Kyiv drones — purple dusk, quadcopters over a ship.
    px = 260
    d.rectangle([px, my, px + mw, my + mh], outline=(203, 213, 225), width=1)
    d.rectangle([px, my, px + mw, my + 100], fill=(49, 46, 129))
    for sx, sy in [(30, 18), (90, 34), (150, 14), (205, 40), (120, 52)]:
        d.ellipse([px + sx, my + sy, px + sx + 3, my + sy + 3], fill=PAPER)
    draw_quad(d, px + 70, my + 46, 1.0)
    draw_quad(d, px + 170, my + 30, 0.8)
    d.rectangle([px, my + 76, px + mw, my + 100], fill=(15, 23, 42))
    d.rectangle([px + 50, my + 58, px + 190, my + 78], fill=(51, 65, 85))
    d.rectangle([px + 66, my + 42, px + 86, my + 58], fill=(51, 65, 85))
    tag_chip(d, px + 8, my + 8, "EUROPE", (13, 148, 136))
    yy = my + 108
    for ln in fit_lines(d, "DRONES HIT KYIV REGION", sans_b(14), mw - 20)[:2]:
        d.text((px + 10, yy), ln, font=sans_b(14), fill=INK)
        yy += 17
    for ln in fit_lines(d, "Russian ship Sparta II burns in Gulf of Finland.",
                        sans(11), mw - 20)[:2]:
        d.text((px + 10, yy), ln, font=sans(11), fill=MUTED)
        yy += 14

    # 3. Hormuz — sunset sea, tanker, 25 dead.
    px = 512
    d.rectangle([px, my, px + mw, my + mh], outline=(203, 213, 225), width=1)
    d.rectangle([px, my, px + mw, my + 52], fill=(249, 115, 22))
    d.rectangle([px, my + 52, px + mw, my + 100], fill=(8, 145, 178))
    for wy in (60, 72, 84):
        for wx in range(0, mw, 40):
            d.arc([px + wx, my + wy, px + wx + 38, my + wy + 14], 180, 360,
                  fill=(207, 250, 254), width=2)
    d.rectangle([px + 46, my + 40, px + 190, my + 66], fill=(31, 41, 55))
    d.rectangle([px + 82, my + 22, px + 116, my + 40], fill=(31, 41, 55))
    d.ellipse([px + 196, my + 10, px + 238, my + 52], fill=CRIMSON)
    d.text((px + 217, my + 18), "25", font=sans_b(20), fill=PAPER, anchor="ma")
    tag_chip(d, px + 8, my + 8, "MIDDLE EAST", (185, 28, 28))
    yy = my + 108
    for ln in fit_lines(d, "25 SAILORS DEAD NEAR HORMUZ", sans_b(14), mw - 20)[:2]:
        d.text((px + 10, yy), ln, font=sans_b(14), fill=INK)
        yy += 17
    for ln in fit_lines(d, "UN counts the dead around the Strait of Hormuz.",
                        sans(11), mw - 20)[:2]:
        d.text((px + 10, yy), ln, font=sans(11), fill=MUTED)
        yy += 14

    # 4. Peace plan — parchment, treaty document, olive branches.
    px = 764
    d.rectangle([px, my, px + mw, my + mh], outline=(203, 213, 225), width=1)
    d.rectangle([px, my, px + mw, my + 100], fill=(254, 243, 199))
    d.rectangle([px + 72, my + 12, px + 172, my + 92], fill=PAPER,
                outline=(148, 163, 184), width=2)
    d.text((px + 122, my + 20), "28", font=serif_b(30), fill=INK, anchor="ma")
    d.text((px + 122, my + 54), "POINT PLAN", font=sans_b(12), fill=INK, anchor="ma")
    for ly in (72, 80, 88):
        d.line([(px + 86, my + ly), (px + 158, my + ly)], fill=(148, 163, 184), width=2)
    for bx in (18, 196):
        d.ellipse([px + bx, my + 58, px + bx + 26, my + 72], fill=(34, 197, 94))
        d.ellipse([px + bx + 6, my + 66, px + bx + 32, my + 80], fill=(34, 197, 94))
    tag_chip(d, px + 8, my + 8, "AMERICAS", (29, 78, 216))
    yy = my + 108
    for ln in fit_lines(d, "TRUMP'S 28-POINT PEACE PLAN", sans_b(14), mw - 20)[:2]:
        d.text((px + 10, yy), ln, font=sans_b(14), fill=INK)
        yy += 17
    for ln in fit_lines(d, "Europe meets in Stockholm; Zelensky speaks.",
                        sans(11), mw - 20)[:2]:
        d.text((px + 10, yy), ln, font=sans(11), fill=MUTED)
        yy += 14

    # ---- Digest: the rest of the day, 25 stories ----
    d.text((8, 500), "THE REST OF THE DAY — 25 MORE STORIES", font=sans_b(14), fill=NAVY)
    d.line([(330, 508), (1016, 508)], fill=(203, 213, 225), width=1)
    digest = [
        ("GAZA", "UN WORKER KILLED IN STRIKES",
         "Oxfam: metals and asbestos poison water and soil."),
        ("VENEZUELA", "LISTS CARTEL AS TERRORISTS",
         "21+ strikes on drug boats since Sept; ~83 dead."),
        ("BOLSONARO", "BACK IN PRISON",
         "Brazil's former president returns to jail."),
        ("AFCON", "TITLE AWAITS COURT VERDICT",
         "CAS rules on Senegal vs Morocco today."),
        ("NEPAL", "INDIA GIVES NEPAL $1.6BN",
         "Modi, PM Shah open Saryu-Kamala Express."),
        ("TAJIKISTAN", "QUITS THE ICC",
         "Dushanbe moves to leave the court."),
        ("IRAN", "IRANIAN SINGERS FLOGGED",
         "Whipped over a concert without hijab."),
        ("LISBON", "MARCHES ON LIVING COSTS",
         "Thousands protest rising prices in Portugal."),
        ("DENMARK", "KEEPS GHETTO EVICTIONS",
         "Top court backs the evictions."),
        ("F1", "VERSTAPPEN WINS LAS VEGAS GP",
         "Max Verstappen takes the 2026 Vegas race."),
        ("TENNIS", "ALCARAZ WINS ATP FINALS",
         "Beats Zverev in Turin for first title."),
        ("CHESS", "CHAMPIONSHIP OPENS IN GENEVA",
         "Champion Gukesh faces Sindarov."),
        ("CRICKET", "WELLINGTON TEST ENDS DRAWN",
         "India vs NZ level; Pant scores 128."),
        ("SPACE", "BEPICOLOMBO REACHES MERCURY",
         "ESA/JAXA probe enters orbit, off-plan."),
        ("LIBYA", "RUSSIAN CORVETTE DESTROYED",
         "Blast and fire in Benghazi port."),
        ("FRANCE", "FAR-LEFT STREET PROTESTS",
         "Street protests by the far left."),
        ("MYANMAR", "HITS BACK AT ASEAN",
         "Military-backed govt criticises decision."),
        ("ZIMBABWE", "PASTOR ARRESTED",
         "Uebert Angel held over assault claims."),
        ("KOREA", "PYONGYANG SNUBS TRUMP",
         "Kim ignores bid to reopen talks (WSJ)."),
        ("TALIBAN", "ERASES WOMEN'S NAMES",
         "Names replaced with 'Bibi' in Balkh papers."),
        ("BORDER", "TALKS TO EASE TENSION",
         "Military talks in Arunachal Pradesh."),
        ("AI", "MODI OPENS CENTRE AT IIT PATNA",
         "New AI centre at IIT Patna."),
        ("SPICEJET", "GROUNDS ITS PLANES",
         "Cash crisis: unpaid wages, flights cut."),
        ("FERRARI", "UNVEILS 296 CHALLENGE",
         "Stradale and Evo shown in Spain."),
        ("NEW YORK", "STOCKPILE GOODS",
         "Hoarding grows as tech outages spread."),
    ]
    cw, rh = 325, 50
    for i, (tag, head, body) in enumerate(digest):
        cx = 8 + (i % 3) * (cw + 8)
        cy = 524 + (i // 3) * rh
        digest_row(d, cx, cy, cw, tag, head, body)

    d.text((SIDE // 2, 986),
           "Sources: Starlit Daily · JagranJosh · CBC World Report · Disclosure News",
           font=sans(11), fill=MUTED, anchor="ma")
    d.rectangle([0, 0, SIDE - 1, SIDE - 1], outline=NAVY, width=2)

    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    img.save(DEST, "PNG", optimize=True)
    print("wrote", DEST, os.path.getsize(DEST), "bytes")


if __name__ == "__main__":
    build()
