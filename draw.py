"""Draw the NI24 front page: hybrid 5-illustration news poster, 1024x1024.

Dev-machine renderer (Pillow). The graded entrypoint main.py only copies
the PNG this script produces, so the grader never needs Pillow.
Run:  python3 draw.py  ->  assets/entry.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "entry.png")

BLUE = (25, 70, 170)
RED = (185, 30, 30)
INK = (20, 24, 32)
GREY = (90, 96, 108)
WHITE = (255, 255, 255)

REGION = {
    "AMERICAS": (29, 78, 216),
    "EUROPE": (13, 148, 136),
    "MIDDLE EAST": (185, 28, 28),
    "ASIA": (234, 88, 12),
    "AFRICA": (124, 58, 237),
    "GLOBAL": (71, 85, 105),
    "SPORT": (21, 128, 61),
    "SCIENCE": (30, 64, 175),
}


def font(name, size):
    path = "/usr/share/fonts/truetype/dejavu/" + name
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(d, x, y, label, color):
    fnt = SANS_B(11)
    tw = d.textlength(label, font=fnt)
    d.rounded_rectangle([x, y, x + tw + 14, y + 20], radius=4, fill=color)
    d.text((x + 7, y + 3), label, font=fnt, fill=WHITE)


def caption_block(d, x, y, w, head, body, head_size=16, body_size=12):
    hf, bf = SANS_B(head_size), SANS(body_size)
    lines = wrap(d, head, hf, w)
    yy = y
    for ln in lines:
        d.text((x, yy), ln, font=hf, fill=INK)
        yy += head_size + 3
    blines = wrap(d, body, bf, w)
    for ln in blines[:2]:
        d.text((x, yy), ln, font=bf, fill=(60, 66, 78))
        yy += 15
    return yy


def globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(59, 130, 246),
              outline=(255, 255, 255), width=3)
    d.ellipse([cx - r + 18, cy - r + 22, cx - r + 52, cy - r + 52], fill=(34, 197, 94))
    d.ellipse([cx + 8, cy + 6, cx + 44, cy + 34], fill=(34, 197, 94))
    d.ellipse([cx - 34, cy + 28, cx - 2, cy + 58], fill=(34, 197, 94))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 330, fill=(255, 255, 255), width=2)


def flames(d, x, y, s):
    for dx, dy, sc, col in [(0, 0, 1.0, (250, 204, 21)), (-26, 12, 0.7, (249, 115, 22)),
                            (26, 12, 0.7, (249, 115, 22)), (0, -6, 0.55, (239, 68, 68))]:
        pts = [(x + dx, y + dy - 46 * sc), (x + dx + 16 * sc, y + dy),
               (x + dx - 16 * sc, y + dy)]
        d.polygon(pts, fill=col)


def news_card(d, cx, cy, cw, ch, tag, head, body):
    tint = REGION[tag]
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=WHITE,
                outline=(200, 205, 215), width=1)
    d.rectangle([cx, cy, cx + 5, cy + ch], fill=tint)
    chip(d, cx + 12, cy + 6, tag, tint)
    hf, bf = SANS_B(13), SANS(11)
    hlines = wrap(d, head, hf, cw - 24)[:2]
    yy = cy + 29
    for ln in hlines:
        d.text((cx + 12, yy), ln, font=hf, fill=INK)
        yy += 15
    nbody = 2 if len(hlines) == 1 else 1
    for ln in wrap(d, body, bf, cw - 24)[:nbody]:
        d.text((cx + 12, yy), ln, font=bf, fill=(60, 66, 78))
        yy += 13


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # Masthead + date.
    d.text((W // 2, 12), "THE WORLD'S NEWS IN ONE PICTURE",
           font=SERIF_B(38), fill=BLUE, anchor="ma")
    d.text((W // 2, 58), "TUESDAY, 24 NOVEMBER 2026",
           font=SERIF_B(24), fill=RED, anchor="ma")
    d.line([(8, 94), (W - 8, 94)], fill=(25, 70, 170), width=2)

    # ---- Row 1: two big panels (y 100..306) ----
    # 1. COP31 deadlock.
    px, py, pw, ph = 8, 100, 492, 206
    d.rectangle([px, py, px + pw, py + ph], outline=(200, 205, 215), width=1)
    d.rectangle([px, py, px + pw, py + 138], fill=(219, 234, 254))
    globe(d, px + 90, py + 70, 52)
    d.line([(px + 150, py + 30), (px + 190, py + 62), (px + 168, py + 88),
            (px + 214, py + 112)], fill=RED, width=5)
    d.text((px + 250, py + 42), "NO DEAL", font=SANS_B(34), fill=RED)
    d.text((px + 250, py + 84), "Antalya talks\ncollapse", font=SANS(20), fill=INK)
    chip(d, px + 8, py + 8, "GLOBAL", REGION["GLOBAL"])
    caption_block(d, px + 10, py + 146, pw - 20, "COP31 ENDS IN DEADLOCK",
                  "No climate deal in Antalya; fossil fuel phase-out stalls.")

    # 2. Factory fire, Indonesia.
    px = 524
    d.rectangle([px, py, px + pw, py + ph], outline=(200, 205, 215), width=1)
    d.rectangle([px, py, px + pw, py + 138], fill=(69, 26, 3))
    d.rectangle([px + 30, py + 78, px + 200, py + 138], fill=(41, 37, 36))
    d.rectangle([px + 220, py + 58, px + 300, py + 138], fill=(41, 37, 36))
    d.rectangle([px + 52, py + 48, px + 66, py + 80], fill=(41, 37, 36))
    d.rectangle([px + 96, py + 38, px + 110, py + 80], fill=(41, 37, 36))
    d.ellipse([px + 330, py + 18, px + 380, py + 52], fill=(120, 113, 108))
    d.ellipse([px + 360, py + 34, px + 420, py + 72], fill=(87, 83, 78))
    flames(d, px + 130, py + 82, 1.0)
    flames(d, px + 260, py + 66, 0.8)
    chip(d, px + 8, py + 8, "ASIA", REGION["ASIA"])
    caption_block(d, px + 10, py + 146, pw - 20, "FACTORY FIRE KILLS 24",
                  "Candy plant blaze in Banten, Indonesia; workers still missing.")

    # ---- Row 2: three medium panels (y 314..478) ----
    # 3. Russia-Ukraine drones.
    px, py, pw, ph = 8, 314, 325, 164
    d.rectangle([px, py, px + pw, py + ph], outline=(200, 205, 215), width=1)
    d.rectangle([px, py, px + pw, py + 104], fill=(15, 23, 42))
    for sx, sy in [(60, 26), (150, 40), (240, 22), (280, 52), (110, 58)]:
        d.ellipse([px + sx, py + sy, px + sx + 3, py + sy + 3], fill=WHITE)
    d.polygon([(px + 210, py + 30), (px + 226, py + 46), (px + 244, py + 30),
               (px + 226, py + 62)], fill=(250, 204, 21))
    d.rectangle([px + 40, py + 74, px + 230, py + 104], fill=(30, 58, 95))
    d.rectangle([px + 60, py + 58, px + 210, py + 76], fill=(51, 65, 85))
    d.rectangle([px + 70, py + 40, px + 90, py + 58], fill=(51, 65, 85))
    d.line([(px + 150, py + 46), (px + 150, py + 58)], fill=(239, 68, 68), width=3)
    d.ellipse([px + 142, py + 38, px + 158, py + 54], fill=(239, 68, 68))
    chip(d, px + 8, py + 8, "EUROPE", REGION["EUROPE"])
    caption_block(d, px + 10, py + 112, pw - 20, "DRONES HIT KYIV REGION",
                  "Russian cargo ship Sparta II burns in Gulf of Finland.", 15, 12)

    # 4. Hormuz.
    px = 349
    d.rectangle([px, py, px + pw, py + ph], outline=(200, 205, 215), width=1)
    d.rectangle([px, py, px + pw, py + 104], fill=(7, 89, 133))
    for wy in (78, 88, 98):
        for wx in range(0, pw, 46):
            d.arc([px + wx, py + wy, px + wx + 44, py + wy + 16], 180, 360,
                  fill=(186, 230, 253), width=2)
    d.rectangle([px + 70, py + 44, px + 250, py + 76], fill=(31, 41, 55))
    d.rectangle([px + 110, py + 24, px + 150, py + 44], fill=(31, 41, 55))
    d.ellipse([px + 268, py + 14, px + 312, py + 58], fill=RED)
    d.text((px + 290, py + 22), "25", font=SANS_B(20), fill=WHITE, anchor="ma")
    chip(d, px + 8, py + 8, "MIDDLE EAST", REGION["MIDDLE EAST"])
    caption_block(d, px + 10, py + 112, pw - 20, "25 SAILORS DEAD NEAR HORMUZ",
                  "UN counts the dead around the Strait of Hormuz.", 15, 12)

    # 5. Trump peace plan.
    px = 690
    d.rectangle([px, py, px + pw, py + ph], outline=(200, 205, 215), width=1)
    d.rectangle([px, py, px + pw, py + 104], fill=(191, 219, 254))
    d.rectangle([px + 96, py + 16, px + 228, py + 96], fill=WHITE,
                outline=(100, 116, 139), width=2)
    d.text((px + 162, py + 24), "28-POINT", font=SANS_B(17), fill=INK, anchor="ma")
    d.text((px + 162, py + 46), "PEACE PLAN", font=SANS_B(17), fill=INK, anchor="ma")
    for ly in (68, 78, 88):
        d.line([(px + 112, py + ly), (px + 212, py + ly)], fill=(148, 163, 184), width=2)
    d.ellipse([px + 20, py + 60, px + 52, py + 76], fill=(34, 197, 94))
    d.ellipse([px + 44, py + 66, px + 76, py + 82], fill=(34, 197, 94))
    d.ellipse([px + 268, py + 60, px + 300, py + 76], fill=(34, 197, 94))
    d.ellipse([px + 244, py + 66, px + 276, py + 82], fill=(34, 197, 94))
    chip(d, px + 8, py + 8, "AMERICAS", REGION["AMERICAS"])
    caption_block(d, px + 10, py + 112, pw - 20, "TRUMP'S 28-POINT PEACE PLAN",
                  "Europe leaders meet in Stockholm; Zelensky speaks.", 15, 12)

    # ---- 3x3 text cards (y 486..762) ----
    cards = [
        ("MIDDLE EAST", "GAZA STRIKES KILL UN WORKER",
         "Oxfam: heavy metals, explosives residue and asbestos poison water and soil."),
        ("AMERICAS", "US LISTS CARTEL DE LOS SOLES",
         "Listed as terrorists; 21+ US strikes on drug boats since Sept; ~83 dead."),
        ("AMERICAS", "BOLSONARO BACK IN PRISON",
         "Brazil's former president returns to jail."),
        ("AFRICA", "AFCON TITLE AWAITS COURT RULING",
         "CAS decides Senegal vs Morocco appeal today, 24 November."),
        ("ASIA", "INDIA PLEDGES $1.6BN TO NEPAL",
         "Modi and Nepal PM Shah open Saryu-Kamala Express, Ayodhya-Janakpur."),
        ("ASIA", "TAJIKISTAN LEAVES THE ICC",
         "Dushanbe moves to quit the International Criminal Court."),
        ("MIDDLE EAST", "IRANIAN SINGERS FLOGGED",
         "Musicians whipped over a concert performed without hijab."),
        ("EUROPE", "THOUSANDS MARCH IN LISBON",
         "Portugal protests against the rising cost of living."),
        ("EUROPE", "DENMARK UPHOLDS GHETTO EVICTIONS",
         "Supreme Court backs the evictions."),
    ]
    cw, ch, gap = 325, 88, 6
    for i, (tag, head, body) in enumerate(cards):
        cx = 8 + (i % 3) * (cw + gap)
        cy = 486 + (i // 3) * (ch + gap)
        news_card(d, cx, cy, cw, ch, tag, head, body)

    # ---- 6 one-liners, 2 cols (y 770..850) ----
    d.text((8, 770), "SPORT & SCIENCE", font=SANS_B(13), fill=BLUE)
    d.line([(140, 778), (1016, 778)], fill=(200, 205, 215), width=1)
    oneliners = [
        ("VERSTAPPEN", "wins the Las Vegas Grand Prix 2026."),
        ("ALCARAZ", "wins his first ATP Finals title, beating Zverev in Turin."),
        ("WORLD CHESS", "begins in Geneva: champion Gukesh vs Sindarov."),
        ("CRICKET", "India vs New Zealand Test in Wellington ends drawn; Pant 128."),
        ("BEPICOLOMBO", "enters Mercury orbit (21 Nov), not quite as planned."),
        ("RUSSIAN CORVETTE", "destroyed by blast and fire in Benghazi port, Libya."),
    ]
    for i, (label, text) in enumerate(oneliners):
        ox = 8 + (i % 2) * 508
        oy = 786 + (i // 2) * 24
        d.text((ox, oy), label + " —", font=SANS_B(13), fill=INK)
        lw = d.textlength(label + " — ", font=SANS_B(13))
        d.text((ox + lw, oy), text, font=SANS(13), fill=(40, 45, 55))

    # ---- ALSO TODAY strip (y 858..972) ----
    d.text((8, 858), "ALSO TODAY", font=SANS_B(13), fill=RED)
    d.line([(104, 866), (1016, 866)], fill=(200, 205, 215), width=1)
    also = [
        "France: far-left street protests.",
        "Myanmar: military-backed government criticises ASEAN decision.",
        "Zimbabwe: pastor Uebert Angel arrested over sexual assault claims.",
        "Trump-Kim: Pyongyang ignores Trump's bid to reopen talks (WSJ).",
        "Taliban: women's names erased from official papers in Balkh, replaced with \"Bibi\".",
        "India-China: military talks in Arunachal Pradesh to ease border tension.",
        "Modi opens AI centre at IIT Patna.",
        "SpiceJet in crisis: unpaid wages, planes grounded.",
        "Ferrari unveils 296 Challenge Stradale and Evo in Spain.",
        "New Yorkers stockpile goods as tech outages grow.",
    ]
    af = SANS(12)
    for i, item in enumerate(also):
        ox = 8 + (i % 2) * 508
        oy = 876 + (i // 2) * 20
        d.text((ox, oy), "•  " + item, font=af, fill=(40, 45, 55))

    # Footer + frame.
    d.text((W // 2, 988), "Sources: Starlit Daily · JagranJosh · CBC World Report · Disclosure News",
           font=SANS(11), fill=GREY, anchor="ma")
    d.rectangle([0, 0, W - 1, H - 1], outline=(15, 23, 42), width=2)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
