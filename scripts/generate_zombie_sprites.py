"""
Génère les sprite sheets du zombie normal (niveau 1).
Design: cerveau exposé, œil jaune/blanc, hoodie violet, fumée verte, sneakers.
8 directions (5 uniques + 3 flips): 0°, 45°, 90°, 135°, 180°.
Animations: idle (4f), walk (6f). Chaque frame: 128x128 px.

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


# ─────────────────────────────────────────────────
# Helpers communs
# ─────────────────────────────────────────────────

def draw_smoke(d, cx, cy, phase, count=4, color='smoke1'):
    """Fumée verte derrière le zombie."""
    for i in range(count):
        sx = cx - 20 + i * int(40 / count) + math.sin(phase + i * 1.5) * 5
        sy = cy + 38 + math.cos(phase + i) * 3
        alpha = int(60 + math.sin(phase + i * 2) * 20)
        smoke_r = 6 + math.sin(phase * 1.3 + i) * 2
        for r in range(int(smoke_r), 2, -1):
            a = int(alpha * (r / smoke_r))
            d.ellipse([sx - r, sy - r, sx + r, sy + r],
                      fill=Z[color] + (min(255, a),))


def draw_shadow(d, cx, cy):
    """Ombre au sol."""
    d.ellipse([cx - 18, cy + 42, cx + 18, cy + 50], fill=(0, 0, 0, 50))


def draw_shoe(d, fx, fy):
    """Une chaussure."""
    d.rounded_rectangle([fx - 8, fy - 2, fx + 8, fy + 5], radius=3,
                        fill=Z['shoe_sole'])
    d.rounded_rectangle([fx - 8, fy - 8, fx + 8, fy + 2], radius=4,
                        fill=Z['shoe'])
    d.rounded_rectangle([fx - 8, fy - 8, fx + 8, fy + 2], radius=4,
                        outline=Z['outline'])
    d.arc([fx - 5, fy - 6, fx + 5, fy + 0], 20, 160,
          fill=Z['shoe_swoosh'], width=2)


# ─────────────────────────────────────────────────
# 0° — Face (Sud) — regarde vers la caméra
# ─────────────────────────────────────────────────

def draw_zombie_0(d, cx, cy, phase=0, walk_offset=0, arm_angle=0, lean=0):
    """Zombie chibi de face (0° / Sud)."""
    cx += lean

    draw_smoke(d, cx, cy, phase)
    draw_shadow(d, cx, cy)

    # Chaussures
    foot_offset = math.sin(walk_offset) * 4 if walk_offset else 0
    for side in [-1, 1]:
        fx = cx + side * 10
        fy = cy + 42 + (foot_offset * side if walk_offset else 0)
        draw_shoe(d, fx, fy)

    # Pantalon
    for side in [-1, 1]:
        lx = cx + side * 8
        ly = cy + 22 + (foot_offset * side * 0.5 if walk_offset else 0)
        d.rounded_rectangle([lx - 6, ly, lx + 6, ly + 22], radius=3,
                            fill=Z['pants'])
        d.rounded_rectangle([lx - 6, ly, lx + 6, ly + 22], radius=3,
                            outline=Z['outline'])
        d.rectangle([lx - 3, ly + 12, lx + 2, ly + 15], fill=Z['skin_lo'])
        d.line([(lx - 4, ly + 10), (lx + 3, ly + 13)],
               fill=Z['pants_lo'], width=1)

    # Hoodie (corps)
    body_w, body_h = 28, 26
    bx1, by1 = cx - body_w // 2, cy - 2
    bx2, by2 = cx + body_w // 2, cy + 24
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill=Z['hoodie'])
    d.rounded_rectangle([bx1 + 3, by1 + 2, bx1 + 12, by1 + 10], radius=3,
                        fill=Z['hoodie_hi'])
    # Poche kangourou
    d.rounded_rectangle([cx - 10, cy + 10, cx + 10, cy + 20], radius=3,
                        fill=Z['hoodie_lo'])
    d.rounded_rectangle([cx - 10, cy + 10, cx + 10, cy + 20], radius=3,
                        outline=Z['hoodie_dk'])
    d.line([(cx - 2, cy + 12), (cx + 4, cy + 18)], fill=Z['bone'], width=2)
    d.ellipse([cx - 4, cy + 11, cx, cy + 14], fill=Z['bone'])
    d.ellipse([cx + 3, cy + 17, cx + 7, cy + 20], fill=Z['bone'])
    # Cordons
    d.line([(cx - 3, by1 + 4), (cx - 3, by1 + 12)], fill=Z['hoodie_dk'], width=1)
    d.line([(cx + 3, by1 + 4), (cx + 3, by1 + 12)], fill=Z['hoodie_dk'], width=1)
    # Étoile
    star_x, star_y = cx + 10, cy + 5
    d.polygon([(star_x, star_y - 3), (star_x + 1, star_y - 1),
               (star_x + 3, star_y - 1), (star_x + 2, star_y + 1),
               (star_x + 3, star_y + 3), (star_x, star_y + 2),
               (star_x - 3, star_y + 3), (star_x - 2, star_y + 1),
               (star_x - 3, star_y - 1), (star_x - 1, star_y - 1)],
              fill=Z['hoodie_hi'])
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6,
                        outline=Z['outline'], width=2)

    # Bras
    for side in [-1, 1]:
        arm_a = arm_angle * side
        ax = cx + side * 20
        ay = cy + 5
        d.rounded_rectangle([ax - 6, ay - 2, ax + 6, ay + 14], radius=3,
                            fill=Z['hoodie'])
        d.rounded_rectangle([ax - 6, ay - 2, ax + 6, ay + 14], radius=3,
                            outline=Z['outline'])
        hand_y = ay + 14 + abs(arm_a) * 0.15
        d.ellipse([ax - 5, hand_y, ax + 5, hand_y + 10], fill=Z['skin'])
        d.ellipse([ax - 5, hand_y, ax + 5, hand_y + 10], outline=Z['outline'])
        for fi in range(-1, 2):
            ffx = ax + fi * 3
            d.line([(ffx, hand_y + 9), (ffx + fi, hand_y + 14)],
                   fill=Z['skin_lo'], width=2)

    # Cou
    d.rectangle([cx - 5, cy - 8, cx + 5, cy + 2], fill=Z['skin'])

    # Tête
    head_r = 20
    hx, hy = cx, cy - 22
    d.ellipse([hx - head_r, hy - head_r + 2, hx + head_r, hy + head_r - 2],
              fill=Z['skin'])
    d.ellipse([hx + 8, hy + 2, hx + 13, hy + 7], fill=Z['skin_spots'])
    d.ellipse([hx - 12, hy + 5, hx - 8, hy + 9], fill=Z['skin_spots'])
    d.ellipse([hx - 5, hy - 12, hx - 1, hy - 8], fill=Z['skin_spots'])

    # Cheveux
    d.pieslice([hx - 22, hy - 22, hx + 5, hy + 2], 200, 350, fill=Z['hair'])
    for i in range(5):
        mx = hx - 15 + i * 5
        my = hy - 18
        d.polygon([(mx, my), (mx + 3, my - 8 - i * 2), (mx + 6, my)],
                  fill=Z['hair'])
    d.polygon([(hx - 10, hy - 16), (hx - 18, hy - 24), (hx - 5, hy - 16)],
              fill=Z['hair'])
    d.line([(hx - 12, hy - 16), (hx - 5, hy - 14)], fill=Z['hair_hi'], width=2)

    # Cerveau exposé
    brain_x, brain_y = hx + 6, hy - 14
    d.ellipse([brain_x - 10, brain_y - 6, brain_x + 10, brain_y + 8],
              fill=Z['brain'])
    d.arc([brain_x - 8, brain_y - 4, brain_x, brain_y + 6], 0, 180,
          fill=Z['brain_lo'], width=2)
    d.arc([brain_x - 2, brain_y - 5, brain_x + 8, brain_y + 5], 180, 360,
          fill=Z['brain_lo'], width=2)
    d.arc([brain_x - 6, brain_y - 2, brain_x + 4, brain_y + 4], 30, 210,
          fill=Z['brain_lo'], width=1)
    d.ellipse([brain_x - 4, brain_y - 4, brain_x + 2, brain_y],
              fill=Z['brain_hi'])
    d.ellipse([brain_x - 10, brain_y - 6, brain_x + 10, brain_y + 8],
              outline=Z['outline'], width=2)

    # Yeux
    eye_lx, eye_ly = hx - 8, hy - 2
    d.ellipse([eye_lx - 6, eye_ly - 5, eye_lx + 6, eye_ly + 5],
              fill=Z['eye_yellow'])
    d.ellipse([eye_lx - 2, eye_ly - 2, eye_lx + 2, eye_ly + 2],
              fill=Z['pupil'])
    d.ellipse([eye_lx - 6, eye_ly - 5, eye_lx + 6, eye_ly + 5],
              outline=Z['outline'], width=2)
    d.ellipse([eye_lx + 2, eye_ly - 3, eye_lx + 4, eye_ly - 1],
              fill=(255, 255, 240))

    eye_rx, eye_ry = hx + 8, hy - 3
    d.ellipse([eye_rx - 7, eye_ry - 6, eye_rx + 7, eye_ry + 6],
              fill=Z['eye_white'])
    d.ellipse([eye_rx - 2, eye_ry - 1, eye_rx + 3, eye_ry + 3],
              fill=Z['pupil'])
    d.ellipse([eye_rx - 7, eye_ry - 6, eye_rx + 7, eye_ry + 6],
              outline=Z['outline'], width=2)
    d.line([(eye_rx + 4, eye_ry - 3), (eye_rx + 6, eye_ry - 5)],
           fill=(200, 80, 80), width=1)
    d.line([(eye_rx - 4, eye_ry + 3), (eye_rx - 6, eye_ry + 4)],
           fill=(200, 80, 80), width=1)

    # Bouche
    mouth_y = hy + 8
    d.arc([hx - 8, mouth_y - 2, hx + 8, mouth_y + 8], 10, 170,
          fill=Z['outline'], width=2)
    d.pieslice([hx - 7, mouth_y, hx + 7, mouth_y + 7], 0, 180,
               fill=Z['mouth'])
    for tx in range(-5, 6, 4):
        d.polygon([(hx + tx, mouth_y + 1), (hx + tx + 2, mouth_y + 1),
                   (hx + tx + 1, mouth_y + 4)], fill=Z['teeth'])
    d.polygon([(hx + 5, mouth_y + 5), (hx + 7, mouth_y + 5),
               (hx + 6, mouth_y + 9)], fill=Z['teeth'])
    d.ellipse([hx - 2, mouth_y + 3, hx + 3, mouth_y + 7], fill=(190, 70, 65))

    # Oreilles
    for side in [-1, 1]:
        ex = hx + side * 19
        ey = hy + 2
        d.ellipse([ex - 4, ey - 5, ex + 4, ey + 5], fill=Z['skin_lo'])
        d.ellipse([ex - 4, ey - 5, ex + 4, ey + 5], outline=Z['outline'])

    # Outline tête
    d.ellipse([hx - head_r, hy - head_r + 2, hx + head_r, hy + head_r - 2],
              outline=Z['outline'], width=2)


# ─────────────────────────────────────────────────
# 45° — 3/4 face (Sud-Est) — tourné vers la droite
# ─────────────────────────────────────────────────

def draw_zombie_45(d, cx, cy, phase=0, walk_offset=0, arm_angle=0, lean=0):
    """Zombie chibi 3/4 face (45° / Sud-Est)."""
    cx += lean

    draw_smoke(d, cx, cy, phase)
    draw_shadow(d, cx, cy)

    # Chaussures — décalées en profondeur
    foot_offset = math.sin(walk_offset) * 4 if walk_offset else 0
    # Pied arrière (gauche, plus haut = plus loin)
    fx_back = cx - 6
    fy_back = cy + 40 + (-foot_offset if walk_offset else 0)
    draw_shoe(d, fx_back, fy_back)
    # Pied avant (droit, plus bas = plus proche)
    fx_front = cx + 8
    fy_front = cy + 44 + (foot_offset if walk_offset else 0)
    draw_shoe(d, fx_front, fy_front)

    # Pantalon — jambes décalées
    for side, lx_off, fy_off in [(-1, -5, -foot_offset * 0.5),
                                  (1, 7, foot_offset * 0.5)]:
        lx = cx + lx_off
        ly = cy + 22 + (fy_off if walk_offset else 0)
        d.rounded_rectangle([lx - 5, ly, lx + 5, ly + 20], radius=3,
                            fill=Z['pants'])
        d.rounded_rectangle([lx - 5, ly, lx + 5, ly + 20], radius=3,
                            outline=Z['outline'])
        d.rectangle([lx - 2, ly + 12, lx + 2, ly + 15], fill=Z['skin_lo'])

    # Hoodie corps — légèrement tourné (plus large côté droit)
    bx1, by1 = cx - 12, cy - 2
    bx2, by2 = cx + 16, cy + 24
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill=Z['hoodie'])
    # Highlight côté gauche (face éclairée)
    d.rounded_rectangle([bx1 + 2, by1 + 2, bx1 + 10, by1 + 10], radius=3,
                        fill=Z['hoodie_hi'])
    # Poche (décentrée vers la droite)
    d.rounded_rectangle([cx - 6, cy + 10, cx + 12, cy + 20], radius=3,
                        fill=Z['hoodie_lo'])
    d.rounded_rectangle([cx - 6, cy + 10, cx + 12, cy + 20], radius=3,
                        outline=Z['hoodie_dk'])
    # Os dans la poche
    d.line([(cx, cy + 12), (cx + 5, cy + 18)], fill=Z['bone'], width=2)
    d.ellipse([cx - 2, cy + 11, cx + 2, cy + 14], fill=Z['bone'])
    # Cordon (un seul visible, côté face)
    d.line([(cx, by1 + 4), (cx, by1 + 12)], fill=Z['hoodie_dk'], width=1)
    d.line([(cx + 5, by1 + 4), (cx + 5, by1 + 12)], fill=Z['hoodie_dk'], width=1)
    # Étoile
    star_x, star_y = cx + 11, cy + 5
    d.polygon([(star_x, star_y - 3), (star_x + 1, star_y - 1),
               (star_x + 3, star_y - 1), (star_x + 2, star_y + 1),
               (star_x + 3, star_y + 3), (star_x, star_y + 2),
               (star_x - 3, star_y + 3), (star_x - 2, star_y + 1),
               (star_x - 3, star_y - 1), (star_x - 1, star_y - 1)],
              fill=Z['hoodie_hi'])
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6,
                        outline=Z['outline'], width=2)

    # Bras arrière (gauche, derrière le corps)
    ax_b = cx - 18
    ay = cy + 5
    d.rounded_rectangle([ax_b - 5, ay, ax_b + 5, ay + 13], radius=3,
                        fill=Z['hoodie_lo'])
    d.rounded_rectangle([ax_b - 5, ay, ax_b + 5, ay + 13], radius=3,
                        outline=Z['outline'])
    hand_y_b = ay + 13
    d.ellipse([ax_b - 4, hand_y_b, ax_b + 4, hand_y_b + 9], fill=Z['skin_lo'])
    d.ellipse([ax_b - 4, hand_y_b, ax_b + 4, hand_y_b + 9], outline=Z['outline'])

    # Bras avant (droit, devant le corps)
    ax_f = cx + 20
    arm_a = arm_angle
    d.rounded_rectangle([ax_f - 6, ay - 2, ax_f + 6, ay + 14], radius=3,
                        fill=Z['hoodie'])
    d.rounded_rectangle([ax_f - 6, ay - 2, ax_f + 6, ay + 14], radius=3,
                        outline=Z['outline'])
    hand_y_f = ay + 14 + abs(arm_a) * 0.15
    d.ellipse([ax_f - 5, hand_y_f, ax_f + 5, hand_y_f + 10], fill=Z['skin'])
    d.ellipse([ax_f - 5, hand_y_f, ax_f + 5, hand_y_f + 10], outline=Z['outline'])
    for fi in range(-1, 2):
        ffx = ax_f + fi * 3
        d.line([(ffx, hand_y_f + 9), (ffx + fi, hand_y_f + 14)],
               fill=Z['skin_lo'], width=2)

    # Cou (légèrement décentré)
    d.rectangle([cx - 3, cy - 8, cx + 5, cy + 2], fill=Z['skin'])

    # Tête — tournée 3/4 vers la droite
    head_r = 20
    hx, hy = cx + 2, cy - 22
    d.ellipse([hx - head_r, hy - head_r + 2, hx + head_r, hy + head_r - 2],
              fill=Z['skin'])
    # Taches (visibles côté droit)
    d.ellipse([hx + 10, hy + 1, hx + 15, hy + 6], fill=Z['skin_spots'])
    d.ellipse([hx - 8, hy + 5, hx - 4, hy + 9], fill=Z['skin_spots'])

    # Cheveux — masse décalée vers l'arrière (gauche vu en 3/4)
    d.pieslice([hx - 24, hy - 22, hx - 2, hy + 2], 200, 350, fill=Z['hair'])
    for i in range(4):
        mx = hx - 18 + i * 5
        my = hy - 18
        d.polygon([(mx, my), (mx + 3, my - 7 - i * 2), (mx + 6, my)],
                  fill=Z['hair'])
    d.polygon([(hx - 12, hy - 16), (hx - 20, hy - 24), (hx - 7, hy - 16)],
              fill=Z['hair'])
    d.line([(hx - 14, hy - 16), (hx - 7, hy - 14)], fill=Z['hair_hi'], width=2)

    # Cerveau (visible côté droit, décalé)
    brain_x, brain_y = hx + 8, hy - 13
    d.ellipse([brain_x - 9, brain_y - 6, brain_x + 9, brain_y + 7],
              fill=Z['brain'])
    d.arc([brain_x - 7, brain_y - 4, brain_x + 1, brain_y + 5], 0, 180,
          fill=Z['brain_lo'], width=2)
    d.arc([brain_x - 1, brain_y - 5, brain_x + 7, brain_y + 5], 180, 360,
          fill=Z['brain_lo'], width=2)
    d.ellipse([brain_x - 3, brain_y - 4, brain_x + 2, brain_y],
              fill=Z['brain_hi'])
    d.ellipse([brain_x - 9, brain_y - 6, brain_x + 9, brain_y + 7],
              outline=Z['outline'], width=2)

    # Oreille gauche (visible, côté arrière)
    ex, ey = hx - 18, hy + 2
    d.ellipse([ex - 4, ey - 5, ex + 4, ey + 5], fill=Z['skin_lo'])
    d.ellipse([ex - 4, ey - 5, ex + 4, ey + 5], outline=Z['outline'])

    # Yeux — œil gauche (jaune) plus petit/loin, œil droit (blanc) plus gros/proche
    # Œil gauche (plus loin, plus petit)
    eye_lx, eye_ly = hx - 6, hy - 1
    d.ellipse([eye_lx - 4, eye_ly - 4, eye_lx + 4, eye_ly + 4],
              fill=Z['eye_yellow'])
    d.ellipse([eye_lx - 1, eye_ly - 1, eye_lx + 2, eye_ly + 2],
              fill=Z['pupil'])
    d.ellipse([eye_lx - 4, eye_ly - 4, eye_lx + 4, eye_ly + 4],
              outline=Z['outline'], width=2)

    # Œil droit (plus proche, plus gros, fou)
    eye_rx, eye_ry = hx + 10, hy - 2
    d.ellipse([eye_rx - 7, eye_ry - 6, eye_rx + 5, eye_ry + 6],
              fill=Z['eye_white'])
    d.ellipse([eye_rx - 1, eye_ry - 1, eye_rx + 3, eye_ry + 3],
              fill=Z['pupil'])
    d.ellipse([eye_rx - 7, eye_ry - 6, eye_rx + 5, eye_ry + 6],
              outline=Z['outline'], width=2)
    d.line([(eye_rx + 3, eye_ry - 3), (eye_rx + 5, eye_ry - 5)],
           fill=(200, 80, 80), width=1)

    # Bouche (3/4, décalée droite)
    mouth_x, mouth_y = hx + 3, hy + 8
    d.arc([mouth_x - 7, mouth_y - 2, mouth_x + 5, mouth_y + 7], 10, 170,
          fill=Z['outline'], width=2)
    d.pieslice([mouth_x - 6, mouth_y, mouth_x + 4, mouth_y + 6], 0, 180,
               fill=Z['mouth'])
    for tx in range(-4, 4, 3):
        d.polygon([(mouth_x + tx, mouth_y + 1), (mouth_x + tx + 2, mouth_y + 1),
                   (mouth_x + tx + 1, mouth_y + 4)], fill=Z['teeth'])
    # Dent qui dépasse
    d.polygon([(mouth_x + 3, mouth_y + 4), (mouth_x + 5, mouth_y + 4),
               (mouth_x + 4, mouth_y + 8)], fill=Z['teeth'])

    # Outline tête
    d.ellipse([hx - head_r, hy - head_r + 2, hx + head_r, hy + head_r - 2],
              outline=Z['outline'], width=2)


# ─────────────────────────────────────────────────
# 90° — Profil (Est) — regarde vers la droite
# ─────────────────────────────────────────────────

def draw_zombie_90(d, cx, cy, phase=0, walk_offset=0, arm_angle=0, lean=0):
    """Zombie chibi de profil droit (90° / Est)."""
    cx += lean

    draw_smoke(d, cx, cy, phase, count=3)
    draw_shadow(d, cx, cy)

    # Chaussures — une devant, une derrière
    foot_offset = math.sin(walk_offset) * 6 if walk_offset else 0
    # Pied arrière
    fx_b = cx - int(foot_offset * 0.5) if walk_offset else cx
    fy_b = cy + 42
    d.rounded_rectangle([fx_b - 7, fy_b - 2, fx_b + 7, fy_b + 5], radius=3,
                        fill=Z['shoe_sole'])
    d.rounded_rectangle([fx_b - 7, fy_b - 8, fx_b + 7, fy_b + 2], radius=4,
                        fill=Z['shoe'])
    d.rounded_rectangle([fx_b - 7, fy_b - 8, fx_b + 7, fy_b + 2], radius=4,
                        outline=Z['outline'])
    # Pied avant
    fx_f = cx + int(foot_offset * 0.5) if walk_offset else cx
    fy_f = cy + 42
    d.rounded_rectangle([fx_f - 7, fy_f - 2, fx_f + 7, fy_f + 5], radius=3,
                        fill=Z['shoe_sole'])
    d.rounded_rectangle([fx_f - 7, fy_f - 8, fx_f + 7, fy_f + 2], radius=4,
                        fill=Z['shoe'])
    d.rounded_rectangle([fx_f - 7, fy_f - 8, fx_f + 7, fy_f + 2], radius=4,
                        outline=Z['outline'])
    d.arc([fx_f - 4, fy_f - 6, fx_f + 4, fy_f + 0], 20, 160,
          fill=Z['shoe_swoosh'], width=2)

    # Pantalon (profil — deux jambes superposées)
    for lx_off, fy_off in [(-2, -foot_offset * 0.3), (2, foot_offset * 0.3)]:
        lx = cx + lx_off
        ly = cy + 22 + (fy_off if walk_offset else 0)
        d.rounded_rectangle([lx - 5, ly, lx + 5, ly + 22], radius=3,
                            fill=Z['pants'])
        d.rounded_rectangle([lx - 5, ly, lx + 5, ly + 22], radius=3,
                            outline=Z['outline'])
        d.rectangle([lx - 2, ly + 13, lx + 2, ly + 16], fill=Z['skin_lo'])

    # Hoodie corps (profil — plus étroit)
    bx1, by1 = cx - 11, cy - 2
    bx2, by2 = cx + 11, cy + 24
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill=Z['hoodie'])
    # Highlight
    d.rounded_rectangle([bx1 + 2, by1 + 2, bx1 + 8, by1 + 10], radius=3,
                        fill=Z['hoodie_hi'])
    # Pli latéral
    d.line([(cx, cy + 2), (cx, cy + 22)], fill=Z['hoodie_dk'], width=1)
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6,
                        outline=Z['outline'], width=2)

    # Bras arrière (derrière le corps)
    ax_b = cx - 6
    ay = cy + 5
    d.rounded_rectangle([ax_b - 5, ay, ax_b + 3, ay + 13], radius=3,
                        fill=Z['hoodie_lo'])
    d.rounded_rectangle([ax_b - 5, ay, ax_b + 3, ay + 13], radius=3,
                        outline=Z['outline'])
    hand_y_b = ay + 13
    d.ellipse([ax_b - 4, hand_y_b, ax_b + 3, hand_y_b + 8],
              fill=Z['skin_lo'])
    d.ellipse([ax_b - 4, hand_y_b, ax_b + 3, hand_y_b + 8],
              outline=Z['outline'])

    # Bras avant (devant le corps, tendu vers la droite)
    ax_f = cx + 6
    d.rounded_rectangle([ax_f - 3, ay - 2, ax_f + 5, ay + 14], radius=3,
                        fill=Z['hoodie'])
    d.rounded_rectangle([ax_f - 3, ay - 2, ax_f + 5, ay + 14], radius=3,
                        outline=Z['outline'])
    hand_y_f = ay + 14 + abs(arm_angle) * 0.15
    d.ellipse([ax_f - 4, hand_y_f, ax_f + 5, hand_y_f + 10],
              fill=Z['skin'])
    d.ellipse([ax_f - 4, hand_y_f, ax_f + 5, hand_y_f + 10],
              outline=Z['outline'])
    # Griffes
    for fi in range(3):
        ffx = ax_f - 2 + fi * 3
        d.line([(ffx, hand_y_f + 9), (ffx + 2, hand_y_f + 14)],
               fill=Z['skin_lo'], width=2)

    # Cou
    d.rectangle([cx - 3, cy - 8, cx + 4, cy + 2], fill=Z['skin'])

    # Tête (profil droit)
    head_r = 20
    hx, hy = cx + 3, cy - 22
    d.ellipse([hx - head_r, hy - head_r + 2, hx + head_r, hy + head_r - 2],
              fill=Z['skin'])
    # Taches de peau
    d.ellipse([hx + 8, hy + 3, hx + 14, hy + 8], fill=Z['skin_spots'])
    d.ellipse([hx + 2, hy + 8, hx + 7, hy + 12], fill=Z['skin_spots'])

    # Cheveux (de profil — masse à l'arrière)
    d.pieslice([hx - 22, hy - 20, hx - 2, hy + 5], 180, 360, fill=Z['hair'])
    for i in range(4):
        mx = hx - 20 + i * 5
        my = hy - 16
        d.polygon([(mx, my), (mx + 2, my - 8 - i), (mx + 4, my)],
                  fill=Z['hair'])
    d.polygon([(hx - 14, hy - 16), (hx - 22, hy - 22), (hx - 9, hy - 16)],
              fill=Z['hair'])
    d.line([(hx - 16, hy - 14), (hx - 8, hy - 12)], fill=Z['hair_hi'], width=2)

    # Cerveau (profil — plus visible sur le dessus)
    brain_x, brain_y = hx + 4, hy - 14
    d.ellipse([brain_x - 8, brain_y - 6, brain_x + 10, brain_y + 7],
              fill=Z['brain'])
    d.arc([brain_x - 6, brain_y - 4, brain_x + 2, brain_y + 5], 0, 180,
          fill=Z['brain_lo'], width=2)
    d.arc([brain_x, brain_y - 5, brain_x + 8, brain_y + 5], 180, 360,
          fill=Z['brain_lo'], width=2)
    d.ellipse([brain_x - 2, brain_y - 4, brain_x + 3, brain_y],
              fill=Z['brain_hi'])
    d.ellipse([brain_x - 8, brain_y - 6, brain_x + 10, brain_y + 7],
              outline=Z['outline'], width=2)

    # Oreille (une seule visible, côté gauche/arrière)
    # En profil droit, l'oreille gauche est derrière la tête
    # On peut en voir une petite partie
    ex, ey = hx - 16, hy + 2
    d.ellipse([ex - 3, ey - 4, ex + 3, ey + 4], fill=Z['skin_lo'])
    d.ellipse([ex - 3, ey - 4, ex + 3, ey + 4], outline=Z['outline'])

    # Œil (un seul visible — le droit, blanc/fou)
    eye_rx, eye_ry = hx + 10, hy - 2
    d.ellipse([eye_rx - 7, eye_ry - 6, eye_rx + 4, eye_ry + 6],
              fill=Z['eye_white'])
    d.ellipse([eye_rx - 2, eye_ry - 1, eye_rx + 2, eye_ry + 3],
              fill=Z['pupil'])
    d.ellipse([eye_rx - 7, eye_ry - 6, eye_rx + 4, eye_ry + 6],
              outline=Z['outline'], width=2)
    d.line([(eye_rx + 2, eye_ry - 3), (eye_rx + 4, eye_ry - 5)],
           fill=(200, 80, 80), width=1)

    # Bouche (profil — moitié visible)
    mouth_x, mouth_y = hx + 10, hy + 7
    d.arc([mouth_x - 8, mouth_y - 2, mouth_x + 4, mouth_y + 7], 10, 170,
          fill=Z['outline'], width=2)
    d.pieslice([mouth_x - 7, mouth_y, mouth_x + 3, mouth_y + 6], 0, 180,
               fill=Z['mouth'])
    # Dents
    for tx in range(-5, 2, 3):
        d.polygon([(mouth_x + tx, mouth_y + 1), (mouth_x + tx + 2, mouth_y + 1),
                   (mouth_x + tx + 1, mouth_y + 4)], fill=Z['teeth'])
    # Dent qui dépasse
    d.polygon([(mouth_x + 1, mouth_y + 4), (mouth_x + 3, mouth_y + 4),
               (mouth_x + 2, mouth_y + 8)], fill=Z['teeth'])

    # Nez (petit, visible de profil)
    d.polygon([(hx + 16, hy + 1), (hx + 20, hy + 3), (hx + 16, hy + 5)],
              fill=Z['skin_lo'])
    d.line([(hx + 16, hy + 1), (hx + 20, hy + 3), (hx + 16, hy + 5)],
           fill=Z['outline'], width=1)

    # Outline tête
    d.ellipse([hx - head_r, hy - head_r + 2, hx + head_r, hy + head_r - 2],
              outline=Z['outline'], width=2)


# ─────────────────────────────────────────────────
# 135° — 3/4 dos (Nord-Est) — dos tourné vers la droite
# ─────────────────────────────────────────────────

def draw_zombie_135(d, cx, cy, phase=0, walk_offset=0, arm_angle=0, lean=0):
    """Zombie chibi 3/4 dos (135° / Nord-Est)."""
    cx += lean

    draw_smoke(d, cx, cy, phase, count=3, color='smoke2')
    draw_shadow(d, cx, cy)

    # Chaussures
    foot_offset = math.sin(walk_offset) * 4 if walk_offset else 0
    fx_back = cx - 6
    fy_back = cy + 44 + (foot_offset if walk_offset else 0)
    draw_shoe(d, fx_back, fy_back)
    fx_front = cx + 8
    fy_front = cy + 40 + (-foot_offset if walk_offset else 0)
    draw_shoe(d, fx_front, fy_front)

    # Pantalon
    for lx_off, fy_off in [(-5, foot_offset * 0.5), (7, -foot_offset * 0.5)]:
        lx = cx + lx_off
        ly = cy + 22 + (fy_off if walk_offset else 0)
        d.rounded_rectangle([lx - 5, ly, lx + 5, ly + 20], radius=3,
                            fill=Z['pants'])
        d.rounded_rectangle([lx - 5, ly, lx + 5, ly + 20], radius=3,
                            outline=Z['outline'])
        d.rectangle([lx - 2, ly + 14, lx + 2, ly + 17], fill=Z['skin_lo'])

    # Hoodie corps (3/4 dos — on voit surtout le dos)
    bx1, by1 = cx - 14, cy - 2
    bx2, by2 = cx + 14, cy + 24
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill=Z['hoodie'])
    # Capuche tombante (visible de dos)
    d.rounded_rectangle([cx - 10, cy - 4, cx + 10, cy + 5], radius=5,
                        fill=Z['hoodie_lo'])
    d.rounded_rectangle([cx - 10, cy - 4, cx + 10, cy + 5], radius=5,
                        outline=Z['hoodie_dk'])
    # Pli central du dos
    d.line([(cx + 2, cy + 5), (cx + 2, cy + 22)], fill=Z['hoodie_dk'], width=1)
    # Côté du hoodie visible (le côté droit qu'on entrevoit)
    d.rounded_rectangle([bx2 - 6, by1 + 3, bx2, by2 - 3], radius=2,
                        fill=Z['hoodie_hi'])
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6,
                        outline=Z['outline'], width=2)

    # Bras avant (droit — côté visible, légèrement devant)
    ax_f = cx + 18
    ay = cy + 5
    d.rounded_rectangle([ax_f - 5, ay - 2, ax_f + 5, ay + 14], radius=3,
                        fill=Z['hoodie'])
    d.rounded_rectangle([ax_f - 5, ay - 2, ax_f + 5, ay + 14], radius=3,
                        outline=Z['outline'])
    hand_y = ay + 14
    d.ellipse([ax_f - 4, hand_y, ax_f + 4, hand_y + 9], fill=Z['skin'])
    d.ellipse([ax_f - 4, hand_y, ax_f + 4, hand_y + 9], outline=Z['outline'])
    for fi in range(-1, 2):
        ffx = ax_f + fi * 3
        d.line([(ffx, hand_y + 8), (ffx + fi, hand_y + 13)],
               fill=Z['skin_lo'], width=2)

    # Bras arrière (gauche — derrière)
    ax_b = cx - 18
    d.rounded_rectangle([ax_b - 5, ay, ax_b + 5, ay + 13], radius=3,
                        fill=Z['hoodie_lo'])
    d.rounded_rectangle([ax_b - 5, ay, ax_b + 5, ay + 13], radius=3,
                        outline=Z['outline'])
    hand_y_b = ay + 13
    d.ellipse([ax_b - 4, hand_y_b, ax_b + 4, hand_y_b + 9],
              fill=Z['skin_lo'])
    d.ellipse([ax_b - 4, hand_y_b, ax_b + 4, hand_y_b + 9],
              outline=Z['outline'])

    # Cou
    d.rectangle([cx - 3, cy - 8, cx + 5, cy + 2], fill=Z['skin_lo'])

    # Tête (3/4 dos — on voit surtout l'arrière)
    head_r = 20
    hx, hy = cx + 2, cy - 22
    d.ellipse([hx - head_r, hy - head_r + 2, hx + head_r, hy + head_r - 2],
              fill=Z['skin_lo'])

    # Cheveux (beaucoup visibles de dos)
    d.pieslice([hx - 22, hy - 22, hx + 2, hy + 5], 180, 360, fill=Z['hair'])
    for i in range(5):
        mx = hx - 20 + i * 5
        my = hy - 16
        d.polygon([(mx, my), (mx + 2, my - 7 - i), (mx + 5, my)],
                  fill=Z['hair'])
    d.polygon([(hx - 14, hy - 16), (hx - 22, hy - 24), (hx - 7, hy - 16)],
              fill=Z['hair'])
    d.line([(hx - 16, hy - 14), (hx - 8, hy - 12)], fill=Z['hair_hi'], width=2)

    # Cerveau (bien visible, décalé vers la droite)
    brain_x, brain_y = hx + 6, hy - 13
    d.ellipse([brain_x - 10, brain_y - 7, brain_x + 10, brain_y + 8],
              fill=Z['brain'])
    d.arc([brain_x - 8, brain_y - 5, brain_x, brain_y + 6], 0, 180,
          fill=Z['brain_lo'], width=2)
    d.arc([brain_x - 2, brain_y - 6, brain_x + 8, brain_y + 6], 180, 360,
          fill=Z['brain_lo'], width=2)
    d.arc([brain_x - 6, brain_y - 2, brain_x + 4, brain_y + 4], 30, 210,
          fill=Z['brain_lo'], width=1)
    d.ellipse([brain_x - 4, brain_y - 4, brain_x + 2, brain_y],
              fill=Z['brain_hi'])
    d.ellipse([brain_x - 10, brain_y - 7, brain_x + 10, brain_y + 8],
              outline=Z['outline'], width=2)

    # Oreille droite (visible côté droit)
    ex, ey = hx + 18, hy + 2
    d.ellipse([ex - 4, ey - 5, ex + 4, ey + 5], fill=Z['skin_lo'])
    d.ellipse([ex - 4, ey - 5, ex + 4, ey + 5], outline=Z['outline'])

    # Profil partiel — juste la joue et un bout d'œil visible côté droit
    # Petit bout de l'œil blanc (on entrevoit à peine)
    eye_rx, eye_ry = hx + 15, hy - 1
    d.ellipse([eye_rx - 4, eye_ry - 3, eye_rx + 2, eye_ry + 3],
              fill=Z['eye_white'])
    d.ellipse([eye_rx - 2, eye_ry - 1, eye_rx + 1, eye_ry + 2],
              fill=Z['pupil'])
    d.ellipse([eye_rx - 4, eye_ry - 3, eye_rx + 2, eye_ry + 3],
              outline=Z['outline'], width=1)

    # Outline tête
    d.ellipse([hx - head_r, hy - head_r + 2, hx + head_r, hy + head_r - 2],
              outline=Z['outline'], width=2)


# ─────────────────────────────────────────────────
# 180° — Dos (Nord) — regarde en s'éloignant de la caméra
# ─────────────────────────────────────────────────

def draw_zombie_180(d, cx, cy, phase=0, walk_offset=0):
    """Zombie chibi de dos (180° / Nord)."""
    # Fumée verte
    for i in range(3):
        sx = cx - 15 + i * 15 + math.sin(phase + i) * 4
        sy = cy + 38 + math.cos(phase + i) * 3
        for r in range(6, 2, -1):
            a = int(50 * (r / 6))
            d.ellipse([sx - r, sy - r, sx + r, sy + r],
                      fill=Z['smoke2'] + (a,))

    draw_shadow(d, cx, cy)

    # Chaussures
    fo = math.sin(walk_offset) * 4 if walk_offset else 0
    for side in [-1, 1]:
        fx = cx + side * 10
        fy = cy + 42 + fo * side
        d.rounded_rectangle([fx - 8, fy - 2, fx + 8, fy + 5], radius=3,
                            fill=Z['shoe_sole'])
        d.rounded_rectangle([fx - 8, fy - 8, fx + 8, fy + 2], radius=4,
                            fill=Z['shoe'])
        d.rounded_rectangle([fx - 8, fy - 8, fx + 8, fy + 2], radius=4,
                            outline=Z['outline'])

    # Pantalon
    for side in [-1, 1]:
        lx = cx + side * 8
        ly = cy + 22 + fo * side * 0.5
        d.rounded_rectangle([lx - 6, ly, lx + 6, ly + 22], radius=3,
                            fill=Z['pants'])
        d.rounded_rectangle([lx - 6, ly, lx + 6, ly + 22], radius=3,
                            outline=Z['outline'])
        d.rectangle([lx - 2, ly + 14, lx + 3, ly + 17], fill=Z['skin_lo'])

    # Hoodie corps (dos)
    bx1, by1 = cx - 14, cy - 2
    bx2, by2 = cx + 14, cy + 24
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill=Z['hoodie'])
    # Capuche tombante
    d.rounded_rectangle([cx - 12, cy - 4, cx + 12, cy + 6], radius=5,
                        fill=Z['hoodie_lo'])
    d.rounded_rectangle([cx - 12, cy - 4, cx + 12, cy + 6], radius=5,
                        outline=Z['hoodie_dk'])
    # Pli central
    d.line([(cx, cy + 6), (cx, cy + 22)], fill=Z['hoodie_dk'], width=1)
    d.rounded_rectangle([bx1, by1, bx2, by2], radius=6,
                        outline=Z['outline'], width=2)

    # Bras (dos)
    for side in [-1, 1]:
        ax = cx + side * 20
        ay = cy + 5
        d.rounded_rectangle([ax - 6, ay - 2, ax + 6, ay + 14], radius=3,
                            fill=Z['hoodie'])
        d.rounded_rectangle([ax - 6, ay - 2, ax + 6, ay + 14], radius=3,
                            outline=Z['outline'])
        d.ellipse([ax - 5, ay + 14, ax + 5, ay + 24], fill=Z['skin'])
        d.ellipse([ax - 5, ay + 14, ax + 5, ay + 24], outline=Z['outline'])

    # Cou
    d.rectangle([cx - 5, cy - 8, cx + 5, cy + 2], fill=Z['skin_lo'])

    # Tête (dos)
    head_r = 20
    hx, hy = cx, cy - 22
    d.ellipse([hx - head_r, hy - head_r + 2, hx + head_r, hy + head_r - 2],
              fill=Z['skin_lo'])

    # Cheveux (plus visibles de dos)
    d.pieslice([hx - 20, hy - 20, hx + 10, hy + 5], 180, 360, fill=Z['hair'])
    for i in range(6):
        mx = hx - 18 + i * 6
        my = hy - 16
        d.polygon([(mx, my), (mx + 2, my - 7 - i), (mx + 5, my)],
                  fill=Z['hair'])
    d.line([(hx - 15, hy - 14), (hx - 5, hy - 10)], fill=Z['hair_hi'], width=2)

    # Cerveau (bien visible de dos)
    bx, by = hx + 5, hy - 13
    d.ellipse([bx - 11, by - 7, bx + 11, by + 9], fill=Z['brain'])
    d.arc([bx - 9, by - 5, bx + 1, by + 7], 0, 180,
          fill=Z['brain_lo'], width=2)
    d.arc([bx - 3, by - 6, bx + 9, by + 6], 180, 360,
          fill=Z['brain_lo'], width=2)
    d.ellipse([bx - 5, by - 4, bx + 1, by], fill=Z['brain_hi'])
    d.ellipse([bx - 11, by - 7, bx + 11, by + 9],
              outline=Z['outline'], width=2)

    # Oreilles
    for side in [-1, 1]:
        ex, ey = hx + side * 19, hy + 2
        d.ellipse([ex - 4, ey - 5, ex + 4, ey + 5], fill=Z['skin_lo'])
        d.ellipse([ex - 4, ey - 5, ex + 4, ey + 5], outline=Z['outline'])

    d.ellipse([hx - head_r, hy - head_r + 2, hx + head_r, hy + head_r - 2],
              outline=Z['outline'], width=2)


# ─────────────────────────────────────────────────
# Génération des sprite sheets
# ─────────────────────────────────────────────────

def generate_sheet(draw_func, num_frames, filename, anim_params):
    """Génère un sprite sheet horizontal."""
    sheet = Image.new('RGBA', (F * num_frames, F), (0, 0, 0, 0))
    for i in range(num_frames):
        frame = Image.new('RGBA', (F, F), (0, 0, 0, 0))
        d = ImageDraw.Draw(frame)
        params = anim_params(i, num_frames)
        draw_func(d, F // 2, F // 2 + 8, **params)
        sheet.paste(frame, (i * F, 0))
    sheet.save(filename)
    print(f"  ✓ {filename} ({F * num_frames}x{F})")


def generate_flipped_sheet(src_filename, dst_filename):
    """Génère un sprite sheet flippé horizontalement (pour les directions gauche)."""
    src = Image.open(src_filename)
    flipped = src.transpose(Image.FLIP_LEFT_RIGHT)
    flipped.save(dst_filename)
    print(f"  ↔ {dst_filename} (flip de {os.path.basename(src_filename)})")


def idle_params(i, n):
    return {
        'phase': i * 1.5,
        'lean': math.sin(i * math.pi / 2) * 3,
        'arm_angle': math.sin(i * math.pi / 2) * 5,
    }


def walk_params(i, n):
    return {
        'phase': i * 1.0,
        'walk_offset': i * math.pi / 3,
        'lean': math.sin(i * math.pi / 3) * 4,
        'arm_angle': math.cos(i * math.pi / 3) * 8,
    }


def idle_params_back(i, n):
    return {'phase': i * 1.5}


def walk_params_back(i, n):
    return {
        'phase': i * 1.0,
        'walk_offset': i * math.pi / 3,
    }


def main():
    os.makedirs(OUTPUT, exist_ok=True)

    print("=== Zombie Normal — 8 directions ===\n")

    # --- 5 directions uniques ---
    directions = [
        ("0",   draw_zombie_0,   idle_params,      walk_params),
        ("45",  draw_zombie_45,  idle_params,      walk_params),
        ("90",  draw_zombie_90,  idle_params,      walk_params),
        ("135", draw_zombie_135, idle_params,      walk_params),
        ("180", draw_zombie_180, idle_params_back, walk_params_back),
    ]

    for angle, draw_func, idle_p, walk_p in directions:
        print(f"\n--- Direction {angle}° ---")
        generate_sheet(draw_func, 4,
                       os.path.join(OUTPUT, f"idle-{angle}.png"), idle_p)
        generate_sheet(draw_func, 6,
                       os.path.join(OUTPUT, f"walk-{angle}.png"), walk_p)

    # --- 3 directions miroir (flip horizontal) ---
    flips = [
        ("45", "315"),   # 315° = flip de 45°
        ("90", "270"),   # 270° = flip de 90°
        ("135", "225"),  # 225° = flip de 135°
    ]

    print("\n--- Directions miroir (flip horizontal) ---")
    for src_angle, dst_angle in flips:
        for anim in ["idle", "walk"]:
            src = os.path.join(OUTPUT, f"{anim}-{src_angle}.png")
            dst = os.path.join(OUTPUT, f"{anim}-{dst_angle}.png")
            generate_flipped_sheet(src, dst)

    # --- Rétrocompatibilité : copier aussi les anciens noms ---
    print("\n--- Copies rétrocompatibilité ---")
    compat = [
        ("idle-0.png", "idle-front.png"),
        ("walk-0.png", "walk-front.png"),
        ("idle-180.png", "idle-back.png"),
        ("walk-180.png", "walk-back.png"),
    ]
    for src_name, dst_name in compat:
        src = os.path.join(OUTPUT, src_name)
        dst = os.path.join(OUTPUT, dst_name)
        img = Image.open(src)
        img.save(dst)
        print(f"  = {dst} (copie de {src_name})")

    print("\n✅ Terminé ! 8 directions × 2 animations = 16 sprite sheets")


if __name__ == "__main__":
    main()
