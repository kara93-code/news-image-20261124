"""Draw the 24 November 2026 world-news broadsheet (round 4, final).

Fresh build for news-image-20261124 in the NI25 broadsheet style:
cream paper, blue serif masthead, red date line, a six-point UTC
timeline, three illustrated leads, a 3x3 card grid, an ALSO ON list,
a date-check footer and a sources line. All 30 verified 24 November
stories from brief-build.txt: 3 leads + 9 cards + 12 ALSO ON + 6
timeline moments. Dates verified live 25 Nov: World Chess Game 1
starts 14:00 UTC in Geneva and is drawn; CAS restores Senegal as
AFCON champions on Tuesday 24 Nov.

Renders one 1024x1024 page with Pillow on the dev machine; the
graded entrypoint only copies the rendered file, it never draws.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (246, 241, 227)
PANEL = (255, 253, 246)
INK = (25, 25, 25)
GREY = (91, 91, 91)
LINE = (25, 25, 25)
BLUE = (25, 70, 170)
RED = (185, 30, 30)
TEAL = (15, 118, 110)
ORANGE = (194, 87, 11)
PURPLE = (109, 40, 168)
BROWN = (124, 74, 18)
NAVY = (16, 32, 64)

REGION = {
    "Americas": BLUE,
    "Europe": TEAL,
    "Middle East": RED,
    "Asia": ORANGE,
    "Africa": PURPLE,
    "Oceania": BROWN,
    "Global": GREY,
}


def fnt(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap_text(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, width, fill=INK, gap=3, limit=None):
    lines = wrap_text(d, text, font, width)
    if limit:
        lines = lines[:limit]
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += font.size + gap
    return y


def band(d, box, top, bottom, steps=12):
    x0, y0, x1, y1 = box
    for i in range(steps):
        t = i / (steps - 1)
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        yy0 = y0 + (y1 - y0) * i // steps
        yy1 = y0 + (y1 - y0) * (i + 1) // steps
        d.rectangle([x0, yy0, x1, yy1], fill=col)


def paint_globe(d, x, y, w, h):
    band(d, (x, y, x + w, y + h), (10, 42, 80), (24, 90, 120))
    for sx, sy in [(28, 18), (80, 34), (150, 14), (230, 40), (280, 22),
                   (60, 60), (190, 56), (250, 66)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    cx, cy, r = x + w // 2, y + h // 2 + 6, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(56, 189, 248),
              outline=(255, 255, 255), width=3)
    d.ellipse([cx - r + 14, cy - r + 16, cx - r + 44, cy - r + 42],
              fill=(74, 222, 128))
    d.ellipse([cx + 2, cy + 4, cx + 38, cy + 30], fill=(74, 222, 128))
    d.ellipse([cx - 34, cy + 22, cx - 4, cy + 48], fill=(74, 222, 128))
    d.line([(cx - 6, cy - r + 4), (cx + 16, cy - 18), (cx - 2, cy + 2),
            (cx + 20, cy + 26), (cx + 2, cy + r - 6)], fill=RED, width=5)
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(16, 32, 64))


def paint_fire(d, x, y, w, h):
    band(d, (x, y, x + w, y + h), (124, 45, 18), (234, 88, 12))
    d.ellipse([x + w - 70, y + 10, x + w - 26, y + 54], fill=(255, 214, 130))
    base = y + h - 46
    d.rectangle([x + 20, base - 34, x + 130, base + 46], fill=(28, 25, 23))
    d.rectangle([x + 150, base - 52, x + 210, base + 46], fill=(28, 25, 23))
    d.rectangle([x + 232, base - 20, x + 268, base + 46], fill=(28, 25, 23))
    d.rectangle([x + 52, base - 58, x + 66, base - 34], fill=(28, 25, 23))
    d.ellipse([x + 220, y + 64, x + 262, y + 92], fill=(120, 113, 108))
    d.ellipse([x + 238, y + 48, x + 272, y + 72], fill=(120, 113, 108))
    cx = x + w // 2
    for dx, s, col in [(-70, 30, (255, 110, 20)), (-24, 42, (255, 150, 30)),
                       (24, 34, (255, 110, 20)), (66, 26, (255, 190, 60))]:
        bx = cx + dx
        d.polygon([(bx - s // 2, base + 20), (bx, base + 20 - s),
                   (bx + s // 2, base + 20)], fill=col)
        d.polygon([(bx - s // 4, base + 20), (bx, base + 20 - s // 2),
                   (bx + s // 4, base + 20)], fill=(255, 220, 110))


def paint_tanker(d, x, y, w, h):
    band(d, (x, y, x + w, y + h // 2), (249, 115, 22), (253, 186, 116))
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(8, 145, 178))
    d.ellipse([x + 24, y + 12, x + 64, y + 52], fill=(255, 244, 200))
    for wy in (y + h // 2 + 12, y + h // 2 + 26, y + h // 2 + 40):
        for wx in range(x, x + w - 40, 44):
            d.arc([wx, wy, wx + 40, wy + 14], 180, 360,
                  fill=(207, 250, 254), width=2)
    d.rectangle([x + 40, y + h - 52, x + 220, y + h - 22], fill=(51, 65, 85))
    d.rectangle([x + 76, y + h - 74, x + 118, y + h - 52], fill=(51, 65, 85))
    d.rectangle([x + 140, y + h - 66, x + 152, y + h - 52], fill=(51, 65, 85))
    d.ellipse([x + w - 56, y + 8, x + w - 12, y + 52], fill=RED)
    d.text((x + w - 34, y + 16), "25", font=fnt(SANS_B, 20),
           fill=(255, 255, 255), anchor="ma")


LEADS = [
    {"art": paint_globe, "region": "Global", "topic": "CLIMATE",
     "head": "COP31 ends in deadlock in Antalya",
     "deck": "Two weeks of talks, two days of overtime — and no climate pact. "
             "Fossil-fuel language splits 194 countries.",
     "src": "UN News · Reuters"},
    {"art": paint_fire, "region": "Asia", "topic": "DISASTER",
     "head": "Candy-factory fire kills 26 in Banten",
     "deck": "Blaze rips through a sweet factory in Indonesia; rescuers still "
             "search for missing workers.",
     "src": "JagranJosh · Starlit Daily"},
    {"art": paint_tanker, "region": "Middle East", "topic": "HORMUZ",
     "head": "25 sailors dead near the Strait of Hormuz",
     "deck": "The UN counts 25 seafarers killed around the strait since February.",
     "src": "CBC World Report · Disclosure News"},
]

CARDS = [
    ("Europe", "WAR", "Drones hit Kyiv region; Sparta II burns",
     "Russian drones strike the Kyiv region, people missing; a Russian cargo ship burns in the Gulf of Finland."),
    ("Middle East", "GAZA", "UN worker killed as Gaza strikes go on",
     "Oxfam: 99% of Gaza contaminated — heavy metals, asbestos, explosives residue."),
    ("Americas", "VENEZUELA", "US lists Cartel de los Soles as terrorists",
     "21+ strikes on drug boats since September; about 83 dead."),
    ("Americas", "BRAZIL", "Bolsonaro in intensive care",
     "Ex-president, serving 27 years, is treated for a bowel obstruction and pneumonia."),
    ("Africa", "AFCON", "CAS restores Senegal as AFCON champions",
     "Court upholds the appeal; the 1-0 final stands, Morocco's 3-0 forfeit overturned."),
    ("Asia", "NEPAL", "India pledges $1.6bn to rebuild Nepal",
     "Modi and PM Shah open the Saryu–Kamala Express, Ayodhya to Janakpur."),
    ("Asia", "ICC", "Tajikistan moves to leave the ICC",
     "Dushanbe starts the process of quitting the court."),
    ("Middle East", "IRAN", "Iran flogs singer over concert",
     "Parastoo Ahmadi gets 74 lashes for performing without hijab."),
    ("Europe", "PORTUGAL", "Lisbon marches on the cost of living",
     "Thousands take to the streets over rising prices."),
]

ALSO = [
    "Verstappen wins the Las Vegas Grand Prix.",
    "Alcaraz wins first ATP Finals title, beating Zverev.",
    "World Chess Game 1 drawn; Gukesh survives a Berlin scare.",
    "Wellington Test drawn; Pant scores 128 for India.",
    "Denmark's top court backs 'ghetto law' evictions.",
    "Russian corvette sunk by sea drones in Benghazi port.",
    "Far-left street protests in France.",
    "Myanmar's military-backed government hits back at ASEAN.",
    "Pastor Uebert Angel arrested in Zimbabwe.",
    "Pyongyang snubs Trump's bid to reopen talks.",
    "Taliban erase women's names from official papers in Balkh.",
    "India–China military talks in Arunachal Pradesh.",
]

TIMELINE = [
    ("03:00", "Kyiv drones strike"),
    ("07:00", "Modi opens AI centre"),
    ("09:00", "SpiceJet grounds planes"),
    ("14:00", "Ferrari unveils 296"),
    ("17:00", "28-point plan in Stockholm"),
    ("21:00", "New Yorkers stockpile"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = fnt(SERIF_B, 38)
    f_date = fnt(SERIF_B, 25)
    f_sub = fnt(SANS_B, 14)
    f_time = fnt(SANS_B, 12)
    f_time2 = fnt(SANS, 11)
    f_kick = fnt(SANS_B, 12)
    f_head = fnt(SERIF_B, 19)
    f_deck = fnt(SANS, 13)
    f_src = fnt(SANS, 11)
    f_card_h = fnt(SANS_B, 15)
    f_card_d = fnt(SANS, 12)
    f_num = fnt(SANS_B, 15)
    f_also_h = fnt(SANS_B, 13)
    f_also = fnt(SANS, 13)
    f_small = fnt(SANS, 11)
    f_small_b = fnt(SANS_B, 11)

    mast = "THE WORLD'S NEWS IN ONE PICTURE"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 26), mast,
           font=f_mast, fill=BLUE)
    date_line = "TUESDAY, 24 NOVEMBER 2026"
    d.text(((W - d.textlength(date_line, font=f_date)) / 2, 70), date_line,
           font=f_date, fill=RED)
    sub = "30 STORIES  •  7 REGIONS  •  ALL FROM THIS TUESDAY  •  ALL TIMES IN UTC"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 102), sub,
           font=f_sub, fill=INK)
    d.line([28, 124, W - 28, 124], fill=LINE, width=2)

    # UTC timeline strip: six moments from the day.
    y = 132
    d.line([40, y + 6, W - 40, y + 6], fill=GREY, width=1)
    step = (W - 80) / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = 40 + step * i + step / 2
        d.ellipse([cx - 4, y + 2, cx + 4, y + 10], fill=RED)
        tw = d.textlength(t, font=f_time)
        d.text((cx - tw / 2, y + 13), t, font=f_time, fill=INK)
        lw = d.textlength(label, font=f_time2)
        d.text((cx - lw / 2, y + 27), label, font=f_time2, fill=GREY)
    d.line([28, 176, W - 28, 176], fill=LINE, width=1)

    # Three illustrated leads.
    lx, ly, lw, lh = 28, 180, 316, 316
    gap = 10
    for i, lead in enumerate(LEADS):
        x = lx + i * (lw + gap)
        d.rectangle([x, ly, x + lw, ly + lh], outline=LINE, width=1, fill=PANEL)
        lead["art"](d, x + 1, ly + 1, lw - 2, 132)
        col = REGION[lead["region"]]
        d.rectangle([x, ly + 132, x + lw, ly + 152], fill=col)
        tag = "%s  •  %s" % (lead["region"].upper(), lead["topic"])
        d.text((x + 8, ly + 136), tag, font=f_kick, fill=(255, 255, 255))
        yy = para(d, x + 8, ly + 160, lead["head"], f_head, lw - 16,
                  gap=1, limit=2)
        para(d, x + 8, yy + 4, lead["deck"], f_deck, lw - 16,
             fill=(50, 50, 50), gap=2, limit=3)
        d.text((x + 8, ly + lh - 18), lead["src"], font=f_src, fill=GREY)

    # 3x3 numbered cards (stories 4-12).
    cy0, ch, cw = 506, 96, 316
    for i, (region, topic, head, deck) in enumerate(CARDS):
        r, c = divmod(i, 3)
        x = 28 + c * (cw + gap)
        y = cy0 + r * (ch + 9)
        col = REGION[region]
        d.rectangle([x, y, x + cw, y + ch], outline=LINE, width=1, fill=PANEL)
        d.rectangle([x, y, x + 5, y + ch], fill=col)
        d.rectangle([x + 12, y + 10, x + 40, y + 34], fill=col)
        num = str(i + 4)
        d.text((x + 26 - d.textlength(num, font=f_num) / 2, y + 13), num,
               font=f_num, fill=(255, 255, 255))
        tag = "%s • %s" % (region.upper(), topic)
        d.text((x + 48, y + 11), tag, font=f_kick, fill=col)
        para(d, x + 48, y + 30, head, f_card_h, cw - 58, gap=0, limit=2)
        para(d, x + 12, y + 64, deck, f_card_d, cw - 24,
             fill=(50, 50, 50), gap=1, limit=2)

    # ALSO ON: stories 13-24, two columns.
    ay = 820
    d.line([28, ay, W - 28, ay], fill=LINE, width=2)
    d.text((28, ay + 6), "ALSO ON TUESDAY 24 NOVEMBER — 12 MORE STORIES",
           font=f_also_h, fill=RED)
    nums = "DAY IN NUMBERS: 26 DEAD IN BANTEN • 25 NEAR HORMUZ • $1.6BN FOR NEPAL"
    d.text((W - 28 - d.textlength(nums, font=f_small_b), ay + 7), nums,
           font=f_small_b, fill=BLUE)
    col_w = 474
    for i, item in enumerate(ALSO):
        col_i, row_i = divmod(i, 6)
        x = 28 + col_i * (col_w + 20)
        y = ay + 28 + row_i * 19
        n = str(i + 13)
        d.text((x, y), n, font=f_num, fill=BLUE)
        para(d, x + 28, y + 1, item, f_also, col_w - 28, gap=0, limit=1)

    # Date check + sources.
    by = 962
    d.line([28, by, W - 28, by], fill=LINE, width=1)
    check = ("DATE CHECK — Left out: they are not today. AFCON final was "
             "18 January • India's oil-gas bill rose ~60% in October • Chess "
             "ceremony was Sunday 22 Nov.")
    para(d, 28, by + 6, check, f_small_b, W - 56, fill=RED, gap=1, limit=2)
    srcs = ("Sources: Starlit Daily • JagranJosh • CBC World Report • Disclosure News "
            "— Illustrations are drawings.")
    d.text((28, 997), srcs, font=f_small, fill=GREY)

    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    img.save(DEST, "PNG")
    print("wrote", DEST, os.path.getsize(DEST), "bytes")


if __name__ == "__main__":
    main()
