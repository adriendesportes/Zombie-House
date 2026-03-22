"""
Génère les sprite sheets du zombie normal (niveau 1).
Design: cerveau exposé, œil jaune/blanc, hoodie violet, fumée verte, sneakers.
4 directions: front, back. Animations: idle (4f), walk (6f).
Chaque frame: 128x128 px.

Usage: python scripts/generate_zombie_sprites.py
"""

from PIL import Image, ImageDraw
import math
import os

F = 128  # Frame size
OUTPUT = "public/assets/sprites/enemies/zombie-normal"

# Palette zombie
Z = {
    'skin': (142, 165, 90),
    'skin_hi': (160, 182, 105),
    'skin_lo': (115, 138, 68),
    'skin_spots': (100, 120, 55),
    'brain': (210, 140, 150),
    'brain_hi': (230, 165, 172),
    'brain_lo': (180, 110, 125),
    'hair': (55, 40, 50),
    'hair_hi': (75, 55, 68),
    'eye_yellow': (230, 200, 40),
    'eye_white': (235, 235, 240),
    'pupil': (25, 20, 15),
    'mouth': (120, 35, 30),
    'teeth': (220, 215, 195),
    'hoodie': (82, 65, 95),
    'hoodie_hi': (100, 82, 115),
    'hoodie_lo': (62, 48, 75),
    'hoodie_dk': (48, 35, 58),
    'pants': (55, 52, 58),
    'pants_lo': (40, 38, 44),
    'shoe': (50, 45, 52),
    'shoe_sole': (180, 178, 170),
    'shoe_swoosh': (160, 160, 165),
    'bone': (220, 215, 195),
    'smoke1': (160, 220, 60),
    'smoke2': (120, 200, 40),
    'outline': (30, 25, 20),
}


def draw_zombie_front(d, cx, cy, phase=0, walk_offset=0, arm_angle=0, lean=0):
    """Dessine un zombie chibi de face."""
    cx += lean

    # === Fumée verte (derrière) ===
    for i in range(4):
        sx = cx - 20 + i * 12 + math.sin(phase + i * 1.5) * 5
        sy = cy + 38 + math.cos(phase + i) * 3
        alpha = int(60 + math.sin(phase + i * 2) * 20)
        smoke_r = 6 + math.sin(phase * 1.3 + i) * 2
        for r in range(int(smoke_r), 2, -1):
            a = int(alpha * (r / smoke_r))
            d.ellipse([sx-r, sy-r, sx+r, sy+r],
                      fill=Z['smoke1'] + (min(255, a),))

    # === Ombre au sol ===
    d.ellipse([cx-18, cy+42, cx+18, cy+50],
              fill=(0, 0, 0, 50))

    # === Chaussures ===
    foot_offset = math.sin(walk_offset) * 4 if walk_offset else 0
    for side in [-1, 1]:
        fx = cx + side * 10
        fy = cy + 42 + (foot_offset * side if walk_offset else 0)
        # Semelle
        d.rounded_rectangle([fx-8, fy-2, fx+8, fy+5], radius=3,
                            fill=Z['shoe_sole'])
        # Shoe body
        d.rounded_rectangle([fx-8, fy-8, fx+8, fy+2], radius=4,
                            fill=Z['shoe'])
        d.rounded_rectangle([fx-8, fy-8, fx+8, fy+2], radius=4,
                            outline=Z['outline'])
        # Swoosh
        d.arc([fx-5, fy-6, fx+5, fy+0], 20, 160,
              fill=Z['shoe_swoosh'], width=2)

    # === Pantalon ===
    for side in [-1, 1]:
        lx = cx + side * 8
        ly = cy + 22 + (foot_offset * side * 0.5 if walk_offset else 0)
        d.rounded_rectangle([lx-6, ly, lx+6, ly+22], radius=3,
                            fill=Z['pants'])
        d.rounded_rectangle([lx-6, ly, lx+6, ly+22], radius=3,
                            outline=Z['outline'])
        # Trous/déchirures
        d.rectangle([lx-3, ly+12, lx+2, ly+15],
                    fill=Z['skin_lo'])
        d.line([(lx-4, ly+10), (lx+3, ly+13)],
               fill=Z['pants_lo'], width=1)

    # === Hoodie (corps) ===
    body_w, body_h = 28, 26
    bx1, by1 = cx - body_w//2, cy - 2
    bx2, by2 = cx + body_w//2, cy + 24
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6,
                        fill=Z['hoodie'])
    # Highlight
    d.rounded_rectangle([bx1+3, by1+2, bx1+12, by1+10], radius=3,
                        fill=Z['hoodie_hi'])
    # Poche kangourou
    d.rounded_rectangle([cx-10, cy+10, cx+10, cy+20], radius=3,
                        fill=Z['hoodie_lo'])
    d.rounded_rectangle([cx-10, cy+10, cx+10, cy+20], radius=3,
                        outline=Z['hoodie_dk'])
    # Os dans la poche
    d.line([(cx-2, cy+12), (cx+4, cy+18)], fill=Z['bone'], width=2)
    d.ellipse([cx-4, cy+11, cx, cy+14], fill=Z['bone'])
    d.ellipse([cx+3, cy+17, cx+7, cy+20], fill=Z['bone'])
    # Cordon
    d.line([(cx-3, by1+4), (cx-3, by1+12)], fill=Z['hoodie_dk'], width=1)
    d.line([(cx+3, by1+4), (cx+3, by1+12)], fill=Z['hoodie_dk'], width=1)
    # Étoile décorative sur hoodie
    star_x, star_y = cx + 10, cy + 5
    d.polygon([(star_x, star_y-3), (star_x+1, star_y-1), (star_x+3, star_y-1),
               (star_x+2, star_y+1), (star_x+3, star_y+3), (star_x, star_y+2),
               (star_x-3, star_y+3), (star_x-2, star_y+1), (star_x-3, star_y-1),
               (star_x-1, star_y-1)], fill=Z['hoodie_hi'])
    # Outline corps
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6,
                        outline=Z['outline'], width=2)

    # === Bras ===
    for side in [-1, 1]:
        arm_a = arm_angle * side
        ax = cx + side * 20
        ay = cy + 5
        # Manche hoodie
        d.rounded_rectangle([ax-6, ay-2, ax+6, ay+14], radius=3,
                            fill=Z['hoodie'])
        d.rounded_rectangle([ax-6, ay-2, ax+6, ay+14], radius=3,
                            outline=Z['outline'])
        # Main zombie
        hand_y = ay + 14 + abs(arm_a) * 0.15
        d.ellipse([ax-5, hand_y, ax+5, hand_y+10],
                  fill=Z['skin'])
        d.ellipse([ax-5, hand_y, ax+5, hand_y+10],
                  outline=Z['outline'])
        # Doigts griffus
        for fi in range(-1, 2):
            fx = ax + fi * 3
            d.line([(fx, hand_y+9), (fx + fi, hand_y+14)],
                   fill=Z['skin_lo'], width=2)

    # === Cou ===
    d.rectangle([cx-5, cy-8, cx+5, cy+2], fill=Z['skin'])

    # === Tête ===
    head_r = 20
    hx, hy = cx, cy - 22
    # Tête forme ovale
    d.ellipse([hx-head_r, hy-head_r+2, hx+head_r, hy+head_r-2],
              fill=Z['skin'])
    # Taches de peau
    d.ellipse([hx+8, hy+2, hx+13, hy+7], fill=Z['skin_spots'])
    d.ellipse([hx-12, hy+5, hx-8, hy+9], fill=Z['skin_spots'])
    d.ellipse([hx-5, hy-12, hx-1, hy-8], fill=Z['skin_spots'])

    # === Cheveux (côté gauche + mèches) ===
    # Masse de cheveux
    d.pieslice([hx-22, hy-22, hx+5, hy+2], 200, 350,
               fill=Z['hair'])
    # Mèches individuelles
    for i in range(5):
        mx = hx - 15 + i * 5
        my = hy - 18
        d.polygon([(mx, my), (mx + 3, my - 8 - i*2), (mx + 6, my)],
                  fill=Z['hair'])
    d.polygon([(hx-10, hy-16), (hx-18, hy-24), (hx-5, hy-16)],
              fill=Z['hair'])
    # Highlight cheveux
    d.line([(hx-12, hy-16), (hx-5, hy-14)],
           fill=Z['hair_hi'], width=2)

    # === Cerveau exposé ===
    brain_x, brain_y = hx + 6, hy - 14
    d.ellipse([brain_x-10, brain_y-6, brain_x+10, brain_y+8],
              fill=Z['brain'])
    # Circonvolutions
    d.arc([brain_x-8, brain_y-4, brain_x, brain_y+6], 0, 180,
          fill=Z['brain_lo'], width=2)
    d.arc([brain_x-2, brain_y-5, brain_x+8, brain_y+5], 180, 360,
          fill=Z['brain_lo'], width=2)
    d.arc([brain_x-6, brain_y-2, brain_x+4, brain_y+4], 30, 210,
          fill=Z['brain_lo'], width=1)
    # Highlight
    d.ellipse([brain_x-4, brain_y-4, brain_x+2, brain_y], fill=Z['brain_hi'])
    # Outline cerveau
    d.ellipse([brain_x-10, brain_y-6, brain_x+10, brain_y+8],
              outline=Z['outline'], width=2)

    # === Yeux ===
    # Œil gauche (jaune)
    eye_lx, eye_ly = hx - 8, hy - 2
    d.ellipse([eye_lx-6, eye_ly-5, eye_lx+6, eye_ly+5],
              fill=Z['eye_yellow'])
    d.ellipse([eye_lx-2, eye_ly-2, eye_lx+2, eye_ly+2],
              fill=Z['pupil'])
    d.ellipse([eye_lx-6, eye_ly-5, eye_lx+6, eye_ly+5],
              outline=Z['outline'], width=2)
    # Reflet
    d.ellipse([eye_lx+2, eye_ly-3, eye_lx+4, eye_ly-1],
              fill=(255, 255, 240))

    # Œil droit (blanc, plus gros, fou)
    eye_rx, eye_ry = hx + 8, hy - 3
    d.ellipse([eye_rx-7, eye_ry-6, eye_rx+7, eye_ry+6],
              fill=Z['eye_white'])
    d.ellipse([eye_rx-2, eye_ry-1, eye_rx+3, eye_ry+3],
              fill=Z['pupil'])
    d.ellipse([eye_rx-7, eye_ry-6, eye_rx+7, eye_ry+6],
              outline=Z['outline'], width=2)
    # Veines
    d.line([(eye_rx+4, eye_ry-3), (eye_rx+6, eye_ry-5)],
           fill=(200, 80, 80), width=1)
    d.line([(eye_rx-4, eye_ry+3), (eye_rx-6, eye_ry+4)],
           fill=(200, 80, 80), width=1)

    # === Bouche ===
    mouth_y = hy + 8
    d.arc([hx-8, mouth_y-2, hx+8, mouth_y+8], 10, 170,
          fill=Z['outline'], width=2)
    # Intérieur bouche
    d.pieslice([hx-7, mouth_y, hx+7, mouth_y+7], 0, 180,
               fill=Z['mouth'])
    # Dents
    for tx in range(-5, 6, 4):
        d.polygon([(hx+tx, mouth_y+1), (hx+tx+2, mouth_y+1), (hx+tx+1, mouth_y+4)],
                  fill=Z['teeth'])
    # Dent qui dépasse
    d.polygon([(hx+5, mouth_y+5), (hx+7, mouth_y+5), (hx+6, mouth_y+9)],
              fill=Z['teeth'])
    # Langue
    d.ellipse([hx-2, mouth_y+3, hx+3, mouth_y+7],
              fill=(190, 70, 65))

    # === Oreilles ===
    for side in [-1, 1]:
        ex = hx + side * 19
        ey = hy + 2
        d.ellipse([ex-4, ey-5, ex+4, ey+5],
                  fill=Z['skin_lo'])
        d.ellipse([ex-4, ey-5, ex+4, ey+5],
                  outline=Z['outline'])

    # === Outline tête ===
    d.ellipse([hx-head_r, hy-head_r+2, hx+head_r, hy+head_r-2],
              outline=Z['outline'], width=2)


def draw_zombie_back(d, cx, cy, phase=0, walk_offset=0):
    """Dessine un zombie chibi de dos."""
    # === Fumée verte ===
    for i in range(3):
        sx = cx - 15 + i * 15 + math.sin(phase + i) * 4
        sy = cy + 38 + math.cos(phase + i) * 3
        for r in range(6, 2, -1):
            a = int(50 * (r / 6))
            d.ellipse([sx-r, sy-r, sx+r, sy+r],
                      fill=Z['smoke2'] + (a,))

    # Ombre
    d.ellipse([cx-18, cy+42, cx+18, cy+50], fill=(0,0,0,50))

    # Chaussures
    fo = math.sin(walk_offset) * 4 if walk_offset else 0
    for side in [-1, 1]:
        fx = cx + side * 10
        fy = cy + 42 + fo * side
        d.rounded_rectangle([fx-8, fy-2, fx+8, fy+5], radius=3, fill=Z['shoe_sole'])
        d.rounded_rectangle([fx-8, fy-8, fx+8, fy+2], radius=4, fill=Z['shoe'])
        d.rounded_rectangle([fx-8, fy-8, fx+8, fy+2], radius=4, outline=Z['outline'])

    # Pantalon
    for side in [-1, 1]:
        lx = cx + side * 8
        ly = cy + 22 + fo * side * 0.5
        d.rounded_rectangle([lx-6, ly, lx+6, ly+22], radius=3, fill=Z['pants'])
        d.rounded_rectangle([lx-6, ly, lx+6, ly+22], radius=3, outline=Z['outline'])
        d.rectangle([lx-2, ly+14, lx+3, ly+17], fill=Z['skin_lo'])

    # Hoodie corps (dos)
    bx1, by1 = cx - 14, cy - 2
    bx2, by2 = cx + 14, cy + 24
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill=Z['hoodie'])
    # Capuche tombante
    d.rounded_rectangle([cx-12, cy-4, cx+12, cy+6], radius=5, fill=Z['hoodie_lo'])
    d.rounded_rectangle([cx-12, cy-4, cx+12, cy+6], radius=5, outline=Z['hoodie_dk'])
    # Pli central
    d.line([(cx, cy+6), (cx, cy+22)], fill=Z['hoodie_dk'], width=1)
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6, outline=Z['outline'], width=2)

    # Bras (dos)
    for side in [-1, 1]:
        ax = cx + side * 20
        ay = cy + 5
        d.rounded_rectangle([ax-6, ay-2, ax+6, ay+14], radius=3, fill=Z['hoodie'])
        d.rounded_rectangle([ax-6, ay-2, ax+6, ay+14], radius=3, outline=Z['outline'])
        d.ellipse([ax-5, ay+14, ax+5, ay+24], fill=Z['skin'])
        d.ellipse([ax-5, ay+14, ax+5, ay+24], outline=Z['outline'])

    # Cou
    d.rectangle([cx-5, cy-8, cx+5, cy+2], fill=Z['skin_lo'])

    # Tête (dos) — on voit le cerveau et les cheveux
    head_r = 20
    hx, hy = cx, cy - 22
    d.ellipse([hx-head_r, hy-head_r+2, hx+head_r, hy+head_r-2], fill=Z['skin_lo'])

    # Cheveux (plus visibles de dos)
    d.pieslice([hx-20, hy-20, hx+10, hy+5], 180, 360, fill=Z['hair'])
    for i in range(6):
        mx = hx - 18 + i * 6
        my = hy - 16
        d.polygon([(mx, my), (mx+2, my-7-i), (mx+5, my)], fill=Z['hair'])
    d.line([(hx-15, hy-14), (hx-5, hy-10)], fill=Z['hair_hi'], width=2)

    # Cerveau (bien visible de dos)
    bx, by = hx + 5, hy - 13
    d.ellipse([bx-11, by-7, bx+11, by+9], fill=Z['brain'])
    d.arc([bx-9, by-5, bx+1, by+7], 0, 180, fill=Z['brain_lo'], width=2)
    d.arc([bx-3, by-6, bx+9, by+6], 180, 360, fill=Z['brain_lo'], width=2)
    d.ellipse([bx-5, by-4, bx+1, by], fill=Z['brain_hi'])
    d.ellipse([bx-11, by-7, bx+11, by+9], outline=Z['outline'], width=2)

    # Oreilles
    for side in [-1, 1]:
        ex, ey = hx + side * 19, hy + 2
        d.ellipse([ex-4, ey-5, ex+4, ey+5], fill=Z['skin_lo'])
        d.ellipse([ex-4, ey-5, ex+4, ey+5], outline=Z['outline'])

    d.ellipse([hx-head_r, hy-head_r+2, hx+head_r, hy+head_r-2],
              outline=Z['outline'], width=2)


def generate_sheet(draw_func, num_frames, filename, anim_params):
    """Génère un sprite sheet."""
    sheet = Image.new('RGBA', (F * num_frames, F), (0, 0, 0, 0))
    for i in range(num_frames):
        frame = Image.new('RGBA', (F, F), (0, 0, 0, 0))
        d = ImageDraw.Draw(frame)
        params = anim_params(i, num_frames)
        draw_func(d, F//2, F//2 + 8, **params)
        sheet.paste(frame, (i * F, 0))
    sheet.save(filename)
    print(f"  {filename} ({F * num_frames}x{F})")


def main():
    os.makedirs(OUTPUT, exist_ok=True)

    # Idle front (4 frames) — léger balancement
    generate_sheet(draw_zombie_front, 4,
        os.path.join(OUTPUT, "idle-front.png"),
        lambda i, n: {
            'phase': i * 1.5,
            'lean': math.sin(i * math.pi / 2) * 3,
            'arm_angle': math.sin(i * math.pi / 2) * 5,
        })

    # Walk front (6 frames) — marche titubante
    generate_sheet(draw_zombie_front, 6,
        os.path.join(OUTPUT, "walk-front.png"),
        lambda i, n: {
            'phase': i * 1.0,
            'walk_offset': i * math.pi / 3,
            'lean': math.sin(i * math.pi / 3) * 4,
            'arm_angle': math.cos(i * math.pi / 3) * 8,
        })

    # Idle back (4 frames)
    generate_sheet(draw_zombie_back, 4,
        os.path.join(OUTPUT, "idle-back.png"),
        lambda i, n: {
            'phase': i * 1.5,
        })

    # Walk back (6 frames)
    generate_sheet(draw_zombie_back, 6,
        os.path.join(OUTPUT, "walk-back.png"),
        lambda i, n: {
            'phase': i * 1.0,
            'walk_offset': i * math.pi / 3,
        })

    print("Terminé !")


if __name__ == "__main__":
    main()
