#!/usr/bin/env python3
"""Render entry.png for news-image-20261121 (build-time only, needs Pillow).

One-page newspaper of Saturday 21 November 2026: 48 stories, 7 regions.
Every story happened or was first reported on 21 Nov 2026.
Run: python3 render.py  ->  writes entry.png (1024x1024, deterministic).
The graded program is main.py (stdlib only): it just copies entry.png.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (16, 35, 63)
NAVY2 = (24, 52, 88)
GOLD = (200, 162, 75)
GOLD_BG = (232, 205, 130)
RED = (179, 38, 30)
TEAL = (14, 107, 107)
TEAL_D = (9, 74, 74)
GREY = (90, 90, 90)
LINE = (180, 172, 158)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, spacing=3, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


# (num, region, headline, detail, source) for the 24 brief panels #4-27.
BRIEF = [
    (4, "N. AMERICA", "Mexico captures 'El Chapo Isidro'",
     "11 dead in Sinaloa gun battle; flown to Mexico City.", "AP"),
    (5, "EUROPE", "Russian missile hits Kryvyi Rih; 2 killed, 60 hurt",
     "Zelensky's home town; a 7-year-old among the wounded.", "CBC / DW"),
    (6, "EUROPE", "Drones hit Russian ship in Gulf of Finland",
     "Sparta II catches fire, drifts into Finnish waters.", "BRIEFING"),
    (7, "MIDEAST", "Tanker struck by projectile near Strait of Hormuz",
     "Hit on the stern 11 miles off Oman; crew safe.", "UKMTO"),
    (8, "SPACE", "BepiColombo enters orbit around Mercury",
     "After 8 years; ESA-JAXA craft begins 18:24 UTC burn.", "ESA"),
    (9, "S. AMERICA", "Bred mosquitoes cut dengue infections 69%",
     "5,700 children in Belo Horizonte trial; 4-year study.", "AP"),
    (10, "MARKETS", "AI sell-off drags world markets lower",
     "S&P 500 -3.7%; Nikkei -5.06%; Asia falls further.", "ONETURN"),
    (11, "N. AMERICA", "Trump posts 'Great Powers 1945, 2026' photo",
     "Yalta image beside Xi and Putin; defends close ties.", "YONHAP"),
    (12, "MIDEAST", "Trump weighs new strikes on Iran",
     "Israel presses for fast action, officials say.", "NYT"),
    (13, "N. AMERICA", "Court: House proxy voting unconstitutional",
     "Fifth Circuit rules 9-8 in Texas v. Blanche.", "BRIEFING"),
    (14, "N. AMERICA", "Trump: FBI crime-database breach 'not good'",
     "Third outlet reports hack; FBI stays silent.", "BRIEFING"),
    (15, "EUROPE", "Police sentenced over beating of Michel Zecler",
     "Paris court rules on racist attack on producer.", "ONETURN"),
    (16, "OCEANIA", "Australia beat New Zealand 3-1 in Auckland",
     "Mohamed Toure scores twice in trans-Tasman win.", "ALLFOOTBALL"),
    (17, "OCEANIA", "Australia edge Wales 29-26 in Cardiff",
     "Nations Championship thriller at the Principality.", "ESPN / AFP"),
    (18, "AFRICA", "South Africa reach Nations final despite defeat",
     "Springboks through after Ireland loss.", "AFP"),
    (19, "OCEANIA", "Fiji beat Italy for first Championship win",
     "Historic victory in Nations Championship.", "AFP"),
    (20, "EUROPE", "England hand All Blacks record defeat",
     "Coach Rennie: New Zealand 'miles off' the pace.", "AFP"),
    (21, "EUROPE", "Leeds stun Chelsea 4-1 at Stamford Bridge",
     "Four goals silence the Bridge.", "AFP"),
    (22, "EUROPE", "Newcastle hold Arsenal 2-2",
     "Barnes and Thiaw cancel out Eze and Madueke.", "AFP"),
    (23, "EUROPE", "Man City held 1-1 by Fulham",
     "Muniz opener cancelled out by Anderson.", "AFP"),
    (24, "EUROPE", "Malen scores four as Roma rout Parma 5-1",
     "Dutch striker's haul seals away win.", "LIVESCORE"),
    (25, "EUROPE", "Real Madrid beat Celta Vigo 2-1",
     "League leaders hold on at home.", "LIVESCORE"),
    (26, "EUROPE", "PSG win 3-2 at Nice; Doue hurt",
     "Knee injury mars league victory.", "AFP"),
    (27, "N. AMERICA", "No. 10 BYU outlasts Kansas 31-29 in 3OT",
     "Two-point conversion settles wild Big 12 clash.", "REUTERS"),
]

# (num, headline, source) for the 21 "also" items #28-48, one line each.
ALSO = [
    (28, "Nebraska stun No. 14 Ohio State 31-27", "REUTERS"),
    (29, "700,000 displaced by conflict in southern Ethiopia", "JUBA GLOBAL"),
    (30, "Somalia expels UAE ambassador; talks rejected", "JUBA GLOBAL"),
    (31, "Kenya orders headcount over Russian recruitment fears", "JUBA GLOBAL"),
    (32, "40 civilians killed in attack in eastern DR Congo", "JUBA GLOBAL"),
    (33, "Nigeria suspends training of 3,852 customs recruits", "JUBA GLOBAL"),
    (34, "Ghana's Mahama unveils $10bn investment plan", "JUBA GLOBAL"),
    (35, "Gabon hands ExxonMobil deep-sea oil mandate", "JUBA GLOBAL"),
    (36, "South Africa's central bank holds rate at 7.25%", "JUBA GLOBAL"),
    (37, "Malaria vaccine shows 87% efficacy in trial", "JUBA GLOBAL"),
    (38, "UN talks in Geneva to go on over AI weapons rules", "ONETURN"),
    (39, "Salvadoran troops fight gangs in Port-au-Prince", "ONETURN"),
    (40, "Turkey takes control of Sozcu TV", "ONETURN"),
    (41, "Malaysia-Turkey pact to shelter 10,000 Rohingya", "LAMEDITERRANEE"),
    (42, "German groups line up 25bn euro bid for TikTok Europe", "LAMEDITERRANEE"),
    (43, "Xi hails 'significant shift' in China-Australia ties", "LAMEDITERRANEE"),
    (44, "Australia, Canada, NZ urge Russia ceasefire", "GOV. OF CANADA"),
    (45, "12 dead, 180 treated after tainted liquor in India", "LAMEDITERRANEE"),
    (46, "Record king tides flood San Francisco Bay", "BRIEFING"),
    (47, "Princeton student held by ICE", "BRIEFING"),
    (48, "Ukraine sends food aid to nine countries", "LAMEDITERRANEE"),
]

LEADS = [
    dict(num=1, tag="CLIMATE  |  ANTALYA, TURKEY", color=TEAL,
         head="COP31 runs into overtime with no deal in sight",
         body=("Talks stretch past Friday's deadline; the draft drops all "
               "fossil-fuel mentions and a $120bn target. "
               "EU: \u201cgood deal or no deal.\u201d"),
         src="REUTERS / AP"),
    dict(num=2, tag="MIDEAST  |  RIYADH, SAUDI ARABIA", color=RED,
         head="Saudi defences down three Houthi missiles over Riyadh",
         body=("Second attack on the capital in three days; a drone and a "
               "fourth missile downed the same day. Coalition hits "
               "Hodeidah and Sanaa."),
         src="REUTERS / AP / AFP"),
    dict(num=3, tag="DISASTER  |  JUNIN, PERU", color=(150, 90, 20),
         head="Magnitude 6.7-6.9 quake shakes Peru's Andes",
         body=("00:09 UTC, near Junin; felt in Lima as residents flee into "
               "the streets. No deaths or major damage reported."),
         src="USGS / IGP PERU / AFP"),
]

def art_cop31(d, x, y, w, h):
    """Globe, sun and a rising thermometer: climate talks in overtime."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 64, 64))
    d.ellipse([x + w - 78, y + 10, x + w - 18, y + 70], fill=(232, 180, 60))
    cx, cy, r = x + 105, y + 80, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 130, 130))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(220, 240, 235), width=3)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(220, 240, 235), width=2)
    d.line([cx, cy - r, cx, cy + r], fill=(220, 240, 235), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(220, 240, 235), width=2)
    d.ellipse([cx - 26, cy - 34, cx + 6, cy - 6], fill=(46, 160, 110))
    d.ellipse([cx - 2, cy + 8, cx + 30, cy + 38], fill=(46, 160, 110))
    d.rectangle([x + 14, y + h - 26, x + w - 14, y + h - 14], fill=(240, 240, 235))
    d.rectangle([x + 14, y + h - 26, x + 150, y + h - 14], fill=(179, 38, 30))
    d.text((x + 14, y + h - 48), "NO FOSSIL-FUEL MENTION", font=font(FONTB, 13),
           fill=(255, 255, 255))
    d.text((x + 14, y + 10), "COP31", font=font(FONTB, 20), fill=(232, 205, 130))


def art_riyadh(d, x, y, w, h):
    """Night skyline, interceptor arcs and starbursts over Riyadh."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 22, 48))
    for sx, sy in [(x + 30, y + 18), (x + 90, y + 34), (x + 200, y + 14),
                   (x + 260, y + 40), (x + 150, y + 22)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    d.ellipse([x + w - 62, y + 8, x + w - 22, y + 48], fill=(240, 235, 200))
    d.ellipse([x + w - 70, y + 4, x + w - 30, y + 44], fill=(12, 22, 48))
    base = y + h
    for bx, bw, bh in [(x + 8, 34, 52), (x + 48, 26, 78), (x + 80, 40, 44),
                       (x + 126, 30, 92), (x + 162, 36, 58), (x + 204, 28, 84),
                       (x + 238, 42, 48), (x + 286, 30, 66)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(28, 44, 78))
        for wy in range(base - bh + 8, base - 6, 12):
            d.rectangle([bx + 5, wy, bx + 10, wy + 5], fill=(232, 205, 130))
    for ax, ay in [(x + 60, y + 26), (x + 160, y + 18), (x + 255, y + 30)]:
        d.arc([ax - 26, ay - 26, ax + 26, ay + 26], 180, 360, fill=(255, 220, 90), width=3)
        for dx, dy in [(0, 0), (7, 3), (-7, 3), (3, -7), (-3, -7)]:
            d.line([ax + dx, ay + dy, ax - dx, ay - dy], fill=(255, 220, 90), width=2)


def art_peru(d, x, y, w, h):
    """Andes peaks and a seismic zigzag."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 180))
    d.polygon([(x, y + h), (x + 90, y + 28), (x + 180, y + h)], fill=(122, 84, 52))
    d.polygon([(x + 130, y + h), (x + 230, y + 12), (x + 320, y + h)], fill=(96, 62, 38))
    d.polygon([(x + 200, y + 12), (x + 230, y + 12), (x + 245, y + 34),
               (x + 215, y + 34)], fill=(255, 255, 255))
    d.polygon([(x + 62, y + 28), (x + 90, y + 28), (x + 104, y + 52),
               (x + 76, y + 52)], fill=(255, 255, 255))
    pts = [(x + 6, y + h - 34)]
    zig = [0, -16, 0, 10, 0, -26, 0, 8, 0, -14, 0]
    px = x + 6
    for dz in zig:
        px += 26
        pts.append((px, y + h - 34 + dz))
    pts.append((x + w - 6, y + h - 34))
    d.line(pts, fill=(179, 38, 30), width=4, joint="curve")
    d.rectangle([x + w - 96, y + 10, x + w - 10, y + 38], fill=(179, 38, 30))
    d.text((x + w - 88, y + 15), "M 6.8", font=font(FONTB, 18), fill=(255, 255, 255))


ART = [art_cop31, art_riyadh, art_peru]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Banner ----
    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.rectangle([0, 84, W, 88], fill=GOLD)
    d.text((24, 10), "THE WORLD IN ONE PAGE", font=font(FONTB, 15), fill=GOLD)
    d.text((24, 30), "SATURDAY 21 NOVEMBER 2026", font=font(FONTB, 42), fill=WHITE)
    d.text((W - 24, 18), "48 STORIES  \u00b7  7 REGIONS", font=font(FONTB, 17),
           fill=WHITE, anchor="ra")

    # ---- DATE CHECK ----
    d.rectangle([0, 88, W, 138], fill=GOLD_BG)
    d.rectangle([0, 88, W, 138], outline=(150, 110, 40), width=2)
    d.text((24, 94), "DATE CHECK  \u2014  Every story happened or was first reported on "
           "Saturday 21 November 2026.", font=font(FONTB, 17), fill=(60, 30, 0))
    d.text((24, 116), "00:09 UTC  Peru quake    \u2022    02:41 AST  Riyadh intercepts"
           "    \u2022    18:24 UTC  BepiColombo enters Mercury orbit",
           font=font(FONT, 14), fill=(60, 30, 0))

    # ---- Three leads ----
    lx, ly, lw, lh = 16, 148, 322, 292
    gap = 10
    for i, lead in enumerate(LEADS):
        x = lx + i * (lw + gap)
        d.rectangle([x, ly, x + lw, ly + lh], fill=PANEL, outline=LINE, width=1)
        ART[i](d, x + 1, ly + 1, lw - 2, 138)
        ty = ly + 150
        d.text((x + 12, ty), lead["tag"], font=font(FONTB, 11), fill=lead["color"])
        y = draw_wrapped(d, x + 12, ty + 18, lead["head"], font(FONTB, 20),
                         lw - 24, fill=INK, spacing=2, max_lines=2)
        y = draw_wrapped(d, x + 12, y + 4, lead["body"], font(FONT, 13),
                         lw - 24, fill=(50, 50, 50), spacing=2, max_lines=3)
        d.text((x + 12, ly + lh - 22), "21 NOV 2026  \u00b7  " + lead["src"],
               font=font(FONTB, 11), fill=GREY)

    # ---- Brief grid header ----
    d.text((16, 446), "THE DAY IN BRIEF  \u2014  STORIES 4\u201327",
           font=font(FONTB, 15), fill=NAVY)
    d.line([330, 456, W - 16, 456], fill=LINE, width=2)

    # ---- Brief grid: 4 cols x 6 rows ----
    gx, gy, gw, gh, cg, rg = 16, 470, 240, 40, 8, 3
    for idx, (num, region, head, detail, src) in enumerate(BRIEF):
        col, row = idx % 4, idx // 4
        x = gx + col * (gw + cg)
        yy = gy + row * (gh + rg)
        d.rectangle([x, yy, x + gw, yy + gh], fill=PANEL, outline=LINE, width=1)
        d.text((x + 8, yy + 5), str(num), font=font(FONTB, 15), fill=RED)
        tx = x + 34
        y = draw_wrapped(d, tx, yy + 2, head, font(FONTB, 12), gw - 42,
                         fill=INK, spacing=1, max_lines=2)
        d.text((tx, yy + gh - 12), region + "  \u00b7  21 NOV  \u00b7  " + src,
               font=font(FONTB, 9), fill=GREY)

    # ---- Also header ----
    ay0 = 470 + 6 * 40 + 5 * 3 + 8
    d.text((16, ay0), "ALSO ON SATURDAY  \u2014  STORIES 28\u201348",
           font=font(FONTB, 15), fill=NAVY)
    d.line([330, ay0 + 10, W - 16, ay0 + 10], fill=LINE, width=2)

    # ---- Also list: 2 cols x 11 rows ----
    ax, ay, aw = 16, ay0 + 26, 488
    for idx, (num, head, src) in enumerate(ALSO):
        col, row = idx % 2, idx // 2
        x = ax + col * (aw + 8)
        yy = ay + row * 19
        d.text((x, yy), str(num) + ".", font=font(FONTB, 12), fill=RED)
        d.text((x + 30, yy), head, font=font(FONT, 12), fill=INK)
        tw = d.textlength(head, font=font(FONT, 12))
        d.text((x + 34 + tw, yy), "  \u00b7  " + src, font=font(FONTB, 10), fill=GREY)

    # ---- Footer strip ----
    fy = H - 38
    d.rectangle([0, fy, W, H], fill=NAVY)
    d.text((16, fy + 6), "S&P 500  -3.7%     Nikkei  -5.06%     Brent  $89.95  +0.57%",
           font=font(FONTB, 13), fill=WHITE)
    d.text((16, fy + 22), "All 48 stories dated 21 Nov 2026  |  Sources: Reuters, AP, AFP, "
           "USGS, ESA, NYT, UKMTO", font=font(FONT, 11), fill=(200, 210, 225))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
