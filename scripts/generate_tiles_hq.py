"""
Génère les tilesets haute qualité (128x128) pour Zombie House.
Produit des atlas PNG regroupant toutes les variantes.

Outputs:
  public/assets/tilesets/ground-atlas.png    (7 tiles: herbe, pierre, terre, gravier, bois, tapis, eau)
  public/assets/tilesets/wall-front-atlas.png (5 variantes de face avant mur)
  public/assets/tilesets/wall-top-atlas.png   (5 variantes de face dessus mur)
  public/assets/tilesets/wall-dest-atlas.png  (3 variantes murs destructibles)
  public/assets/tilesets/door-atlas.png       (3 variantes de portes)
  public/assets/tilesets/deco-atlas.png       (10 décorations)
  public/assets/tilesets/bush.png             (buisson individuel)

Usage: python scripts/generate_tiles_hq.py
"""

from PIL import Image, ImageDraw, ImageFilter
import random
import os
import math

T = 128  # Tile size HQ
OUTPUT = "public/assets/tilesets"

random.seed(42)


def nc(base, v=12):
    return tuple(max(0, min(255, c + random.randint(-v, v))) for c in base)


def hash_xy(x, y, s=0):
    h = (x * 374761393 + y * 668265263 + s * 1274126177) ^ 0x5bd1e995
    h = (h ^ (h >> 15)) * 0x27d4eb2d & 0xFFFFFFFF
    return (h ^ (h >> 13)) & 0xFFFFFFFF


def hashF(x, y, s=0):
    return hash_xy(x, y, s) / 4294967296


# ==================== GROUND TILES ====================

def gen_ground_grass():
    img = Image.new('RGBA', (T, T), (72, 148, 55))
    d = ImageDraw.Draw(img)
    # Base avec variation
    for y in range(0, T, 4):
        for x in range(0, T, 4):
            h = hashF(x, y, 1)
            r, g, b = int(55 + h * 30), int(130 + h * 35), int(38 + h * 25)
            d.rectangle([x, y, x + 3, y + 3], fill=(r, g, b))
    # Taches plus claires
    for i in range(12):
        cx = hash_xy(i, 0, 10) % (T - 20) + 10
        cy = hash_xy(i, 1, 10) % (T - 20) + 10
        r = 8 + hash_xy(i, 2, 10) % 12
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=nc((65, 155, 48), 10))
    # Brins d'herbe
    for i in range(40):
        x = hash_xy(i, 0, 20) % T
        y = hash_xy(i, 1, 20) % T
        h = 4 + hash_xy(i, 2, 20) % 8
        d.line([(x, y), (x + hash_xy(i, 3, 20) % 3 - 1, y - h)], fill=nc((50, 120, 35), 8), width=1)
    # Petits cailloux
    for i in range(6):
        cx = hash_xy(i, 0, 30) % (T - 10) + 5
        cy = hash_xy(i, 1, 30) % (T - 10) + 5
        d.ellipse([cx - 2, cy - 1, cx + 2, cy + 1], fill=nc((120, 115, 100), 10))
    # Fleur occasionnelle
    for i in range(3):
        if hashF(i, 0, 40) > 0.5:
            fx = hash_xy(i, 0, 41) % (T - 20) + 10
            fy = hash_xy(i, 1, 41) % (T - 20) + 10
            colors = [(230, 210, 60), (210, 80, 120), (200, 100, 200), (100, 180, 220)]
            col = colors[hash_xy(i, 2, 41) % 4]
            d.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=col)
            d.ellipse([fx - 1, fy - 1, fx + 1, fy + 1], fill=(240, 240, 120))
    return img


def gen_ground_stone():
    img = Image.new('RGBA', (T, T), (105, 105, 115))
    d = ImageDraw.Draw(img)
    # Grosses pierres irrégulières
    stones = [
        (0, 0, T * 0.55, T * 0.45), (T * 0.57, 0, T * 0.43, T * 0.50),
        (0, T * 0.48, T * 0.42, T * 0.52), (T * 0.44, T * 0.52, T * 0.30, T * 0.48),
        (T * 0.76, T * 0.52, T * 0.24, T * 0.48),
    ]
    for si, (sx, sy, sw, sh) in enumerate(stones):
        sx, sy, sw, sh = int(sx), int(sy), int(sw), int(sh)
        h = hashF(si, 0, 50)
        r = int(92 + h * 30)
        col = (r, r + 2, r + 8)
        d.rectangle([sx + 2, sy + 2, sx + sw - 3, sy + sh - 3], fill=col)
        # Highlight haut-gauche
        d.line([(sx + 3, sy + 3), (sx + sw - 4, sy + 3)], fill=(col[0] + 20, col[1] + 20, col[2] + 18), width=2)
        d.line([(sx + 3, sy + 3), (sx + 3, sy + sh - 4)], fill=(col[0] + 15, col[1] + 15, col[2] + 13), width=2)
        # Ombre bas-droite
        d.line([(sx + sw - 3, sy + 4), (sx + sw - 3, sy + sh - 3)], fill=(col[0] - 15, col[1] - 15, col[2] - 12), width=2)
        d.line([(sx + 4, sy + sh - 3), (sx + sw - 3, sy + sh - 3)], fill=(col[0] - 12, col[1] - 12, col[2] - 10), width=2)
    # Joints
    d.line([(0, int(T * 0.47)), (T, int(T * 0.50))], fill=(65, 65, 75), width=2)
    d.line([(int(T * 0.56), 0), (int(T * 0.54), T)], fill=(65, 65, 75), width=2)
    d.line([(int(T * 0.43), int(T * 0.50)), (int(T * 0.44), T)], fill=(65, 65, 75), width=2)
    d.line([(int(T * 0.75), int(T * 0.50)), (int(T * 0.76), T)], fill=(65, 65, 75), width=2)
    # Mousse
    for i in range(4):
        mx = hash_xy(i, 0, 60) % (T - 16) + 8
        my = hash_xy(i, 1, 60) % (T - 16) + 8
        d.ellipse([mx - 5, my - 3, mx + 5, my + 3], fill=(60, 100, 45, 80))
    return img


def gen_ground_dirt():
    img = Image.new('RGBA', (T, T), (115, 82, 52))
    d = ImageDraw.Draw(img)
    # Texture granuleuse
    for y in range(0, T, 3):
        for x in range(0, T, 3):
            h = hashF(x, y, 2)
            r = int(105 + h * 30)
            d.rectangle([x, y, x + 2, y + 2], fill=(r, int(r * 0.72), int(r * 0.48)))
    # Cailloux
    for i in range(10):
        cx = hash_xy(i, 0, 70) % (T - 10) + 5
        cy = hash_xy(i, 1, 70) % (T - 10) + 5
        r = 2 + hash_xy(i, 2, 70) % 4
        h = hashF(i, 3, 70)
        d.ellipse([cx - r, cy - r + 1, cx + r, cy + r - 1], fill=nc((140, 130, 110), 15))
    # Racines
    for i in range(3):
        sx = hash_xy(i, 0, 80) % T
        sy = hash_xy(i, 1, 80) % T
        ex = sx + hash_xy(i, 2, 80) % 30 - 15
        ey = sy + hash_xy(i, 3, 80) % 20 + 5
        d.line([(sx, sy), (ex, ey)], fill=(85, 60, 35), width=2)
    return img


def gen_ground_gravel():
    img = Image.new('RGBA', (T, T), (155, 142, 125))
    d = ImageDraw.Draw(img)
    # Base
    for y in range(0, T, 4):
        for x in range(0, T, 4):
            h = hashF(x, y, 3)
            r = int(140 + h * 30)
            d.rectangle([x, y, x + 3, y + 3], fill=(r, int(r * 0.92), int(r * 0.82)))
    # Cailloux variés
    for i in range(30):
        cx = hash_xy(i, 0, 90) % (T - 6) + 3
        cy = hash_xy(i, 1, 90) % (T - 6) + 3
        r = 2 + hash_xy(i, 2, 90) % 5
        h = hashF(i, 3, 90)
        col = (int(110 + h * 60), int(100 + h * 55), int(85 + h * 45))
        d.ellipse([cx - r, cy - r + 1, cx + r, cy + r - 1], fill=col)
        d.ellipse([cx - r + 1, cy - r + 1, cx - r + 2, cy - r + 2], fill=(col[0] + 20, col[1] + 20, col[2] + 18))
    return img


def gen_ground_wood():
    img = Image.new('RGBA', (T, T), (125, 88, 52))
    d = ImageDraw.Draw(img)
    plank_h = T // 5
    for py in range(0, T, plank_h):
        h = hashF(0, py, 4)
        base = (int(115 + h * 25), int(80 + h * 20), int(45 + h * 15))
        d.rectangle([0, py, T - 1, py + plank_h - 2], fill=base)
        # Grain
        for gy in range(py + 3, py + plank_h - 3, 4):
            for gx in range(0, T, 2):
                gh = hashF(gx, gy, 5)
                if gh > 0.6:
                    d.line([(gx, gy), (gx + 3 + int(gh * 4), gy)],
                           fill=(base[0] - 12, base[1] - 10, base[2] - 8), width=1)
        # Highlight haut
        d.line([(0, py), (T, py)], fill=(base[0] + 15, base[1] + 12, base[2] + 10), width=1)
        # Joint bas
        d.line([(0, py + plank_h - 1), (T, py + plank_h - 1)], fill=(base[0] - 25, base[1] - 20, base[2] - 15), width=2)
        # Noeud de bois
        if h > 0.7:
            kx = hash_xy(0, py, 100) % (T - 20) + 10
            ky = py + plank_h // 2
            d.ellipse([kx - 6, ky - 4, kx + 6, ky + 4], fill=(base[0] - 20, base[1] - 18, base[2] - 12))
            d.ellipse([kx - 3, ky - 2, kx + 3, ky + 2], fill=(base[0] - 30, base[1] - 25, base[2] - 18))
    return img


def gen_ground_carpet():
    img = Image.new('RGBA', (T, T), (150, 35, 35))
    d = ImageDraw.Draw(img)
    # Bordure ornée
    d.rectangle([0, 0, T - 1, T - 1], outline=(180, 60, 50), width=6)
    d.rectangle([8, 8, T - 9, T - 9], outline=(120, 25, 25), width=2)
    d.rectangle([12, 12, T - 13, T - 13], outline=(170, 55, 45), width=1)
    # Motif central
    cx, cy = T // 2, T // 2
    for r in range(28, 8, -8):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(170, 50, 40, 120), width=2)
    # Motifs en losange
    for i in range(4):
        angle = i * math.pi / 2
        px = cx + int(math.cos(angle) * 30)
        py = cy + int(math.sin(angle) * 30)
        d.polygon([(px, py - 8), (px + 6, py), (px, py + 8), (px - 6, py)],
                  fill=(170, 50, 40))
    # Usure subtile
    for i in range(5):
        ux = hash_xy(i, 0, 110) % (T - 30) + 15
        uy = hash_xy(i, 1, 110) % (T - 30) + 15
        d.ellipse([ux - 8, uy - 5, ux + 8, uy + 5], fill=(140, 30, 30, 60))
    return img


def gen_ground_water():
    img = Image.new('RGBA', (T, T), (35, 115, 185))
    d = ImageDraw.Draw(img)
    # Base dégradée
    for y in range(T):
        h = y / T
        r, g, b = int(30 + h * 10), int(105 + h * 15), int(175 + h * 15)
        d.line([(0, y), (T, y)], fill=(r, g, b))
    # Vagues
    for wave in range(5):
        wy = 15 + wave * 22
        points = []
        for x in range(0, T + 4, 4):
            y = wy + int(math.sin(x * 0.08 + wave * 1.5) * 4)
            points.append((x, y))
        if len(points) > 1:
            d.line(points, fill=(255, 255, 255, 50), width=2)
    # Reflets
    for i in range(6):
        rx = hash_xy(i, 0, 120) % (T - 20) + 10
        ry = hash_xy(i, 1, 120) % (T - 20) + 10
        d.ellipse([rx - 4, ry - 2, rx + 4, ry + 2], fill=(255, 255, 255, 40))
    # Bord sombre
    d.rectangle([0, 0, T - 1, T - 1], outline=(20, 60, 100, 120), width=2)
    return img


# ==================== WALL FRONTS ====================

def draw_bricks(d, w, h, base_r, base_g, base_b, mortar, brick_h=16, brick_w=30):
    """Dessine des briques détaillées sur une surface w×h."""
    for by in range(0, h, brick_h):
        row = by // brick_h
        off = (row % 2) * int(brick_w * 0.6)
        for bx in range(-brick_w + off, w, brick_w + 3):
            x1, x2 = max(0, bx), min(w, bx + brick_w)
            y2 = min(h, by + brick_h - 2)
            if x2 <= x1:
                continue
            bh = hashF(row, bx // brick_w, 200)
            br = int(base_r + bh * 35 - 15)
            bg = int(base_g + bh * 22 - 10)
            bb = int(base_b + bh * 18 - 8)
            d.rectangle([x1, by + 1, x2, y2], fill=(br, bg, bb))
            # Highlight
            d.line([(x1 + 1, by + 2), (x2 - 1, by + 2)], fill=(br + 18, bg + 15, bb + 12), width=1)
            # Shadow
            d.line([(x1 + 1, y2), (x2 - 1, y2)], fill=(br - 15, bg - 12, bb - 10), width=1)
            # Texture
            if bh > 0.65:
                tx = x1 + 3 + hash_xy(row, bx, 210) % (max(1, x2 - x1 - 8))
                d.rectangle([tx, by + 4, tx + 4, by + 6], fill=(br - 10, bg - 8, bb - 6))
        # Mortier
        d.line([(0, by), (w, by)], fill=mortar, width=2)
    # Mortier vertical
    for by in range(0, h, brick_h):
        row = by // brick_h
        off = (row % 2) * int(brick_w * 0.6)
        for bx in range(off, w, brick_w + 3):
            if 0 < bx < w:
                d.line([(bx, by), (bx, min(h, by + brick_h))], fill=mortar, width=1)


def gen_wall_front_red_brick():
    img = Image.new('RGBA', (T, T), (90, 60, 48))
    d = ImageDraw.Draw(img)
    draw_bricks(d, T, T, 135, 68, 42, (70, 58, 48))
    # Ombre dégradée en bas
    for i in range(10):
        d.line([(0, T - 1 - i), (T, T - 1 - i)], fill=(0, 0, 0, 25 - i * 2))
    return img


def gen_wall_front_gray_stone():
    img = Image.new('RGBA', (T, T), (82, 82, 92))
    d = ImageDraw.Draw(img)
    # Grosses pierres
    stones = [
        (0, 0, T * 0.58, T * 0.48), (T * 0.60, 0, T * 0.40, T * 0.52),
        (0, T * 0.50, T * 0.45, T * 0.50), (T * 0.47, T * 0.54, T * 0.53, T * 0.46),
    ]
    for si, (sx, sy, sw, sh) in enumerate(stones):
        sx, sy, sw, sh = int(sx), int(sy), int(sw), int(sh)
        h = hashF(si, 0, 220)
        r = int(82 + h * 28)
        col = (r, r + 2, r + 10)
        d.rectangle([sx + 2, sy + 2, sx + sw - 3, sy + sh - 3], fill=col)
        d.line([(sx + 3, sy + 3), (sx + sw - 4, sy + 3)], fill=(col[0] + 15, col[1] + 15, col[2] + 12), width=2)
        d.line([(sx + sw - 3, sy + 4), (sx + sw - 3, sy + sh - 3)], fill=(col[0] - 12, col[1] - 12, col[2] - 10), width=2)
        d.line([(sx + 4, sy + sh - 3), (sx + sw - 3, sy + sh - 3)], fill=(col[0] - 10, col[1] - 10, col[2] - 8), width=2)
    for sx, sy, sw, sh in stones:
        sx, sy, sw, sh = int(sx), int(sy), int(sw), int(sh)
        d.rectangle([sx, sy, sx + sw, sy + sh], outline=(55, 55, 65), width=2)
    for i in range(8):
        d.line([(0, T - 1 - i), (T, T - 1 - i)], fill=(0, 0, 0, 20 - i * 2))
    return img


def gen_wall_front_wood():
    img = Image.new('RGBA', (T, T), (88, 62, 38))
    d = ImageDraw.Draw(img)
    plank_w = T // 6
    for px in range(0, T, plank_w):
        h = hashF(px, 0, 230)
        base = (int(82 + h * 30), int(58 + h * 22), int(35 + h * 18))
        d.rectangle([px + 1, 0, px + plank_w - 1, T - 1], fill=base)
        # Grain vertical
        for gy in range(2, T - 2, 5):
            gx = px + 3 + hash_xy(px, gy, 240) % max(1, plank_w - 6)
            d.line([(gx, gy), (gx, gy + 3)], fill=(base[0] - 10, base[1] - 8, base[2] - 6))
        # Highlight gauche
        d.line([(px + 1, 0), (px + 1, T)], fill=(base[0] + 12, base[1] + 10, base[2] + 8), width=1)
        # Clou
        if h > 0.5:
            ny = hash_xy(px, 0, 250) % (T - 20) + 10
            d.ellipse([px + plank_w // 2 - 2, ny - 2, px + plank_w // 2 + 2, ny + 2], fill=(80, 80, 88))
    # Joints
    for px in range(plank_w, T, plank_w):
        d.line([(px, 0), (px, T)], fill=(45, 30, 18), width=2)
    for i in range(8):
        d.line([(0, T - 1 - i), (T, T - 1 - i)], fill=(0, 0, 0, 20 - i * 2))
    return img


def gen_wall_front_gray_brick():
    img = Image.new('RGBA', (T, T), (80, 82, 90))
    d = ImageDraw.Draw(img)
    draw_bricks(d, T, T, 95, 95, 105, (60, 62, 68))
    for i in range(8):
        d.line([(0, T - 1 - i), (T, T - 1 - i)], fill=(0, 0, 0, 20 - i * 2))
    return img


def gen_wall_front_mossy():
    img = gen_wall_front_red_brick()
    d = ImageDraw.Draw(img)
    # Mousse par-dessus
    for i in range(15):
        mx = hash_xy(i, 0, 260) % T
        my = hash_xy(i, 1, 260) % T
        r = 6 + hash_xy(i, 2, 260) % 10
        a = 80 + hash_xy(i, 3, 260) % 80
        d.ellipse([mx - r, my - r, mx + r, my + r], fill=(55, 130 + hash_xy(i, 4, 260) % 30, 40, a))
    # Feuilles de lierre
    for i in range(8):
        lx = hash_xy(i, 0, 270) % T
        ly = hash_xy(i, 1, 270) % T
        d.ellipse([lx - 4, ly - 6, lx + 4, ly + 6], fill=(60, 140, 45, 120))
        d.line([(lx, ly - 6), (lx, ly + 6)], fill=(45, 100, 32, 100), width=1)
    return img


# ==================== WALL TOPS ====================

def gen_wall_top(base_col, variant=0):
    img = Image.new('RGBA', (T, T), base_col)
    d = ImageDraw.Draw(img)
    # Texture subtile
    for i in range(20):
        x = hash_xy(i, variant, 300) % (T - 8) + 4
        y = hash_xy(i, variant + 1, 300) % (T - 8) + 4
        h = hashF(i, variant, 310)
        w = 4 + hash_xy(i, variant, 320) % 6
        ht = 3 + hash_xy(i, variant, 330) % 4
        col = (base_col[0] + int((h - 0.5) * 20), base_col[1] + int((h - 0.5) * 18), base_col[2] + int((h - 0.5) * 15))
        col = tuple(max(0, min(255, c)) for c in col)
        d.rectangle([x, y, x + w, y + ht], fill=col)
    # Highlight haut
    d.line([(2, 2), (T - 3, 2)], fill=(base_col[0] + 20, base_col[1] + 18, base_col[2] + 15), width=2)
    d.line([(2, 2), (2, T - 3)], fill=(base_col[0] + 15, base_col[1] + 13, base_col[2] + 10), width=2)
    # Ombre bas-droite
    d.line([(T - 3, 3), (T - 3, T - 3)], fill=(base_col[0] - 12, base_col[1] - 10, base_col[2] - 8), width=2)
    d.line([(3, T - 3), (T - 3, T - 3)], fill=(base_col[0] - 10, base_col[1] - 8, base_col[2] - 6), width=2)
    return img


# ==================== DESTRUCTIBLE WALLS ====================

def gen_dest_crate():
    img = Image.new('RGBA', (T, T + T // 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    h = T // 3  # face avant height
    # Face dessus
    base = (172, 148, 112)
    d.rectangle([0, 0, T - 1, T - 1], fill=base)
    # Planches horizontales + verticales
    for py in range(0, T, T // 4):
        d.line([(0, py), (T, py)], fill=(base[0] - 25, base[1] - 22, base[2] - 18), width=2)
    for px in range(0, T, T // 3):
        d.line([(px, 0), (px, T)], fill=(base[0] - 25, base[1] - 22, base[2] - 18), width=2)
    # Croix
    d.line([(8, 8), (T - 8, T - 8)], fill=(base[0] - 40, base[1] - 35, base[2] - 28), width=3)
    d.line([(T - 8, 8), (8, T - 8)], fill=(base[0] - 40, base[1] - 35, base[2] - 28), width=3)
    # Clous
    for nx, ny in [(10, 10), (T - 10, 10), (10, T - 10), (T - 10, T - 10)]:
        d.ellipse([nx - 3, ny - 3, nx + 3, ny + 3], fill=(100, 100, 108))
    # Face avant
    front = (base[0] - 30, base[1] - 28, base[2] - 22)
    d.rectangle([0, T, T - 1, T + h - 1], fill=front)
    for px in range(0, T, T // 3):
        d.line([(px, T), (px, T + h)], fill=(front[0] - 15, front[1] - 12, front[2] - 10), width=2)
    d.rectangle([0, 0, T - 1, T + h - 1], outline=(35, 25, 18), width=3)
    return img


def gen_dest_barrel():
    img = Image.new('RGBA', (T, T + T // 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    h = T // 3
    base = (145, 105, 68)
    # Face dessus (cercle)
    d.ellipse([4, 4, T - 4, T - 4], fill=base)
    d.ellipse([12, 12, T - 12, T - 12], fill=(base[0] - 20, base[1] - 18, base[2] - 12))
    # Cerclages sur dessus
    d.ellipse([8, 8, T - 8, T - 8], outline=(80, 78, 72), width=3)
    d.ellipse([20, 20, T - 20, T - 20], outline=(80, 78, 72), width=2)
    # Planches radiales
    for a in range(0, 360, 30):
        rad = math.radians(a)
        cx, cy = T // 2, T // 2
        d.line([(cx + int(math.cos(rad) * 8), cy + int(math.sin(rad) * 8)),
                (cx + int(math.cos(rad) * (T // 2 - 6)), cy + int(math.sin(rad) * (T // 2 - 6)))],
               fill=(base[0] - 22, base[1] - 18, base[2] - 12), width=1)
    # Face avant
    d.rectangle([6, T, T - 6, T + h - 1], fill=(base[0] - 25, base[1] - 20, base[2] - 15))
    d.rectangle([6, T + 5, T - 6, T + 8], fill=(82, 80, 75))
    d.rectangle([6, T + h - 10, T - 6, T + h - 7], fill=(82, 80, 75))
    d.rectangle([6, T, T - 6, T + h - 1], outline=(35, 25, 18), width=2)
    d.ellipse([4, 4, T - 4, T - 4], outline=(35, 25, 18), width=2)
    return img


def gen_dest_stones():
    img = Image.new('RGBA', (T, T + T // 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    h = T // 3
    base = (138, 132, 122)
    d.rectangle([0, 0, T - 1, T - 1], fill=base)
    # Pierres irrégulières
    stones = [
        (4, 4, T // 2 - 5, T // 2 - 5), (T // 2 + 2, 6, T // 2 - 6, T // 2 - 8),
        (6, T // 2 + 2, T // 2 - 8, T // 2 - 6), (T // 2, T // 2 + 4, T // 2 - 4, T // 2 - 8),
    ]
    for si, (sx, sy, sw, sh) in enumerate(stones):
        h2 = hashF(si, 0, 280)
        col = (int(125 + h2 * 28), int(120 + h2 * 25), int(110 + h2 * 22))
        d.rectangle([sx, sy, sx + sw, sy + sh], fill=col)
        d.rectangle([sx, sy, sx + sw, sy + sh], outline=(80, 75, 68), width=2)
    # Fissures
    d.line([(T // 2 - 3, 5), (T // 2 + 5, T - 5)], fill=(70, 65, 58, 150), width=2)
    d.line([(8, T // 2), (T - 8, T // 2 + 5)], fill=(70, 65, 58, 150), width=2)
    # Face avant
    d.rectangle([0, T, T - 1, T + h - 1], fill=(base[0] - 22, base[1] - 20, base[2] - 18))
    d.line([(0, T + h // 2), (T, T + h // 2 + 2)], fill=(80, 75, 68), width=2)
    d.rectangle([0, 0, T - 1, T + h - 1], outline=(35, 25, 18), width=3)
    return img


# ==================== DOORS ====================

def gen_door_arch():
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Sol dalles
    d.rectangle([0, 0, T - 1, T - 1], fill=(68, 62, 55))
    d.rectangle([4, 4, T // 2 - 2, T // 2 - 2], fill=(75, 68, 60))
    d.rectangle([T // 2 + 2, T // 2 + 2, T - 4, T - 4], fill=(75, 68, 60))
    d.rectangle([T // 2 + 2, 4, T - 4, T // 2 - 2], fill=(72, 65, 58))
    d.rectangle([4, T // 2 + 2, T // 2 - 2, T - 4], fill=(72, 65, 58))
    # Piliers
    d.rectangle([0, 0, 10, T - 1], fill=(105, 92, 78))
    d.rectangle([T - 10, 0, T - 1, T - 1], fill=(105, 92, 78))
    d.line([(1, 0), (1, T)], fill=(120, 108, 92), width=2)
    d.line([(T - 2, 0), (T - 2, T)], fill=(120, 108, 92), width=2)
    d.rectangle([0, 0, 10, T - 1], outline=(40, 32, 25), width=2)
    d.rectangle([T - 10, 0, T - 1, T - 1], outline=(40, 32, 25), width=2)
    return img


def gen_door_wood():
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, T - 1, T - 1], fill=(92, 68, 42))
    # Planches
    for py in range(0, T, T // 5):
        d.line([(0, py), (T, py)], fill=(72, 52, 30), width=2)
    # Seuil haut/bas
    d.rectangle([0, 0, T - 1, 6], fill=(115, 88, 58))
    d.rectangle([0, T - 7, T - 1, T - 1], fill=(115, 88, 58))
    d.line([(0, 3), (T, 3)], fill=(85, 62, 38), width=1)
    d.line([(0, T - 4), (T, T - 4)], fill=(85, 62, 38), width=1)
    d.rectangle([0, 0, T - 1, T - 1], outline=(40, 28, 18), width=2)
    return img


def gen_door_grate():
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, T - 1, T - 1], fill=(32, 30, 25))
    # Barreaux verticaux
    for bx in range(10, T - 5, 14):
        d.line([(bx, 4), (bx, T - 4)], fill=(105, 108, 115), width=3)
    # Barres horizontales
    for by in [T // 3, T * 2 // 3]:
        d.line([(4, by), (T - 4, by)], fill=(90, 92, 100), width=2)
    # Rivets
    for bx in range(10, T - 5, 14):
        for by in [T // 3, T * 2 // 3]:
            d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(130, 132, 140))
            d.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=(90, 92, 100))
    d.rectangle([0, 0, T - 1, T - 1], outline=(25, 22, 18), width=2)
    return img


# ==================== DECORATIONS ====================

def gen_deco(draw_func):
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    draw_func(d, T // 2, T // 2)
    return img


def draw_bones(d, cx, cy):
    d.line([(cx - 18, cy - 6), (cx + 18, cy + 6)], fill=(215, 208, 192), width=4)
    d.line([(cx - 12, cy + 12), (cx + 14, cy - 10)], fill=(215, 208, 192), width=4)
    for ex, ey in [(cx - 18, cy - 6), (cx + 18, cy + 6), (cx - 12, cy + 12), (cx + 14, cy - 10)]:
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(220, 212, 198))


def draw_skull(d, cx, cy):
    d.ellipse([cx - 14, cy - 12, cx + 14, cy + 10], fill=(225, 218, 200))
    d.ellipse([cx - 14, cy - 12, cx + 14, cy + 10], outline=(40, 32, 25), width=2)
    d.ellipse([cx - 7, cy - 5, cx - 2, cy + 1], fill=(35, 28, 22))
    d.ellipse([cx + 2, cy - 5, cx + 7, cy + 1], fill=(35, 28, 22))
    d.polygon([(cx - 1, cy + 4), (cx + 1, cy + 4), (cx, cy + 8)], fill=(35, 28, 22))
    d.line([(cx - 5, cy + 10), (cx + 5, cy + 10)], fill=(35, 28, 22), width=2)
    for tx in range(-3, 5, 3):
        d.line([(cx + tx, cy + 9), (cx + tx, cy + 12)], fill=(35, 28, 22), width=1)


def draw_crack(d, cx, cy):
    d.line([(cx - 20, cy - 12), (cx - 5, cy), (cx - 10, cy + 18)], fill=(0, 0, 0, 100), width=2)
    d.line([(cx - 5, cy), (cx + 15, cy + 8)], fill=(0, 0, 0, 80), width=2)
    d.line([(cx + 5, cy - 15), (cx + 2, cy + 5)], fill=(0, 0, 0, 60), width=1)


def draw_web(d, cx, cy):
    strands = [(cx + 40, cy - 30), (cx + 30, cy + 10), (cx + 10, cy + 35),
               (cx - 20, cy + 40), (cx + 35, cy + 35), (cx + 40, cy + 15)]
    for sx, sy in strands:
        d.line([(cx - T // 2 + 5, cy - T // 2 + 5), (sx, sy)], fill=(200, 200, 212, 110), width=1)
    for r in range(12, 50, 10):
        pts = []
        for sx, sy in strands:
            dx, dy = sx - (cx - T // 2 + 5), sy - (cy - T // 2 + 5)
            dist = max(1, math.hypot(dx, dy))
            pts.append((int(cx - T // 2 + 5 + dx * r / dist), int(cy - T // 2 + 5 + dy * r / dist)))
        for i in range(len(pts) - 1):
            d.line([pts[i], pts[i + 1]], fill=(200, 200, 212, 70), width=1)


def draw_blood(d, cx, cy):
    d.ellipse([cx - 18, cy - 10, cx + 18, cy + 10], fill=(120, 22, 18, 140))
    d.ellipse([cx + 8, cy + 5, cx + 22, cy + 14], fill=(105, 18, 14, 110))
    d.ellipse([cx - 12, cy - 5, cx - 2, cy + 2], fill=(130, 25, 20, 100))


def draw_pebbles(d, cx, cy):
    for i in range(8):
        px = cx - 20 + hash_xy(i, 0, 400) % 40
        py = cy - 15 + hash_xy(i, 1, 400) % 30
        r = 3 + hash_xy(i, 2, 400) % 5
        h = hashF(i, 3, 400)
        col = (int(115 + h * 50), int(108 + h * 45), int(92 + h * 38))
        d.ellipse([px - r, py - r + 1, px + r, py + r - 1], fill=col)


def draw_grass_tuft(d, cx, cy):
    for i in range(8):
        bx = cx - 12 + i * 3
        bh = 10 + hash_xy(0, i, 410) % 12
        d.line([(bx, cy + 8), (bx + hash_xy(1, i, 410) % 4 - 2, cy + 8 - bh)],
               fill=nc((42, 135, 30), 8), width=2)


def draw_mushroom(d, cx, cy):
    d.rectangle([cx - 3, cy, cx + 3, cy + 12], fill=(140, 95, 50))
    d.pieslice([cx - 12, cy - 10, cx + 12, cy + 4], 180, 0, fill=(200, 60, 45))
    d.ellipse([cx - 5, cy - 6, cx - 1, cy - 2], fill=(240, 225, 160))
    d.ellipse([cx + 3, cy - 4, cx + 7, cy], fill=(240, 225, 160))
    d.pieslice([cx - 12, cy - 10, cx + 12, cy + 4], 180, 0, outline=(35, 25, 18), width=2)


def draw_torch(d, cx, cy):
    # Halo
    for r in range(35, 8, -2):
        a = max(0, 35 - r)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 180, 55, a))
    # Support
    d.rectangle([cx - 4, cy - 8, cx + 4, cy + 18], fill=(75, 62, 48))
    d.rectangle([cx - 4, cy - 8, cx + 4, cy + 18], outline=(40, 32, 25), width=2)
    # Flamme
    d.polygon([(cx, cy - 22), (cx - 8, cy - 6), (cx + 8, cy - 6)], fill=(255, 200, 60))
    d.polygon([(cx, cy - 18), (cx - 5, cy - 6), (cx + 5, cy - 6)], fill=(255, 240, 150))
    d.ellipse([cx - 3, cy - 14, cx + 3, cy - 8], fill=(255, 255, 200))


def draw_puddle(d, cx, cy):
    d.ellipse([cx - 16, cy - 8, cx + 16, cy + 8], fill=(35, 90, 140, 100))
    d.ellipse([cx - 10, cy - 4, cx + 10, cy + 4], fill=(45, 105, 155, 80))
    d.ellipse([cx - 3, cy - 2, cx + 5, cy + 1], fill=(255, 255, 255, 40))


# ==================== BUSH ====================

def gen_bush():
    img = Image.new('RGBA', (T + 20, T + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = (T + 20) // 2, (T + 20) // 2
    # Ombre
    d.ellipse([cx - 28, cy + 20, cx + 28, cy + 34], fill=(0, 0, 0, 45))
    # Corps principal
    d.ellipse([cx - 30, cy - 20, cx + 30, cy + 22], fill=(48, 168, 40))
    # Highlight
    d.ellipse([cx - 18, cy - 22, cx + 10, cy - 2], fill=(72, 210, 62))
    d.ellipse([cx - 10, cy - 25, cx + 2, cy - 10], fill=(88, 228, 78))
    # Outline
    d.ellipse([cx - 30, cy - 20, cx + 30, cy + 22], outline=(25, 75, 18), width=3)
    return img


# ==================== ASSEMBLY ====================

def make_atlas(tiles, cols=None):
    if cols is None:
        cols = len(tiles)
    rows = (len(tiles) + cols - 1) // cols
    # Find max height
    max_h = max(t.size[1] for t in tiles)
    w = tiles[0].size[0]
    atlas = Image.new('RGBA', (cols * w, rows * max_h), (0, 0, 0, 0))
    for i, tile in enumerate(tiles):
        c = i % cols
        r = i // cols
        # Align to bottom of cell
        y_off = max_h - tile.size[1]
        atlas.paste(tile, (c * w, r * max_h + y_off), tile)
    return atlas


def main():
    os.makedirs(OUTPUT, exist_ok=True)

    print("Generating ground atlas (7 tiles)...")
    grounds = [
        gen_ground_grass(), gen_ground_stone(), gen_ground_dirt(),
        gen_ground_gravel(), gen_ground_wood(), gen_ground_carpet(),
        gen_ground_water(),
    ]
    make_atlas(grounds).save(os.path.join(OUTPUT, "ground-atlas.png"))
    print(f"  ground-atlas.png ({len(grounds)} tiles, {T}x{T} each)")

    print("Generating wall front atlas (5 variants)...")
    wall_fronts = [
        gen_wall_front_red_brick(), gen_wall_front_gray_stone(),
        gen_wall_front_wood(), gen_wall_front_gray_brick(),
        gen_wall_front_mossy(),
    ]
    make_atlas(wall_fronts).save(os.path.join(OUTPUT, "wall-front-atlas.png"))
    print(f"  wall-front-atlas.png ({len(wall_fronts)} variants)")

    print("Generating wall top atlas (5 variants)...")
    top_colors = [(135, 115, 100), (110, 112, 120), (105, 82, 65), (100, 102, 108), (125, 108, 95)]
    wall_tops = [gen_wall_top(c, i) for i, c in enumerate(top_colors)]
    make_atlas(wall_tops).save(os.path.join(OUTPUT, "wall-top-atlas.png"))
    print(f"  wall-top-atlas.png ({len(wall_tops)} variants)")

    print("Generating destructible wall atlas (3 variants)...")
    dests = [gen_dest_crate(), gen_dest_barrel(), gen_dest_stones()]
    make_atlas(dests).save(os.path.join(OUTPUT, "wall-dest-atlas.png"))
    print(f"  wall-dest-atlas.png ({len(dests)} variants)")

    print("Generating door atlas (3 variants)...")
    doors = [gen_door_arch(), gen_door_wood(), gen_door_grate()]
    make_atlas(doors).save(os.path.join(OUTPUT, "door-atlas.png"))
    print(f"  door-atlas.png ({len(doors)} variants)")

    print("Generating decoration atlas (10 types)...")
    decos = [
        gen_deco(draw_bones), gen_deco(draw_skull), gen_deco(draw_crack),
        gen_deco(draw_web), gen_deco(draw_blood), gen_deco(draw_pebbles),
        gen_deco(draw_grass_tuft), gen_deco(draw_mushroom), gen_deco(draw_torch),
        gen_deco(draw_puddle),
    ]
    make_atlas(decos).save(os.path.join(OUTPUT, "deco-atlas.png"))
    print(f"  deco-atlas.png ({len(decos)} types)")

    print("Generating bush...")
    gen_bush().save(os.path.join(OUTPUT, "bush.png"))
    print("  bush.png")

    print("\nDone!")


if __name__ == "__main__":
    main()
