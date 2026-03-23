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
    # Night grass — very dark green
    img = Image.new('RGBA', (T, T), (18, 42, 15))
    d = ImageDraw.Draw(img)
    # Base avec variation sombre
    for y in range(0, T, 4):
        for x in range(0, T, 4):
            h = hashF(x, y, 1)
            r, g, b = int(12 + h * 18), int(32 + h * 22), int(10 + h * 15)
            d.rectangle([x, y, x + 3, y + 3], fill=(r, g, b))
    # Taches legeres (moonlight)
    for i in range(8):
        cx = hash_xy(i, 0, 10) % (T - 20) + 10
        cy = hash_xy(i, 1, 10) % (T - 20) + 10
        r = 6 + hash_xy(i, 2, 10) % 10
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=nc((22, 50, 20), 6))
    # Brins d'herbe
    for i in range(40):
        x = hash_xy(i, 0, 20) % T
        y = hash_xy(i, 1, 20) % T
        h = 4 + hash_xy(i, 2, 20) % 8
        d.line([(x, y), (x + hash_xy(i, 3, 20) % 3 - 1, y - h)], fill=nc((15, 45, 12), 5), width=1)
    # Petits cailloux (dark)
    for i in range(6):
        cx = hash_xy(i, 0, 30) % (T - 10) + 5
        cy = hash_xy(i, 1, 30) % (T - 10) + 5
        d.ellipse([cx - 2, cy - 1, cx + 2, cy + 1], fill=nc((50, 48, 42), 8))
    # Pas de fleurs la nuit — champignons luminescents
    for i in range(2):
        if hashF(i, 0, 40) > 0.6:
            fx = hash_xy(i, 0, 41) % (T - 20) + 10
            fy = hash_xy(i, 1, 41) % (T - 20) + 10
            # Lueur verte
            d.ellipse([fx - 4, fy - 4, fx + 4, fy + 4], fill=(20, 60, 15, 40))
            colors = [(40, 180, 60), (50, 150, 80), (30, 120, 100)]
            col = colors[hash_xy(i, 2, 41) % 3]
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


def gen_ground_bathroom_tile():
    """White/gray ceramic tiles with grout lines, some cracked."""
    img = Image.new('RGBA', (T, T), (220, 220, 225))
    d = ImageDraw.Draw(img)
    tile_sz = T // 4
    for ty in range(0, T, tile_sz):
        for tx in range(0, T, tile_sz):
            h = hashF(tx, ty, 500)
            r = int(210 + h * 20)
            col = (r, r + 1, r + 3)
            d.rectangle([tx + 2, ty + 2, tx + tile_sz - 3, ty + tile_sz - 3], fill=col)
            # Highlight top-left
            d.line([(tx + 3, ty + 3), (tx + tile_sz - 4, ty + 3)], fill=(col[0] + 12, col[1] + 12, col[2] + 10), width=1)
            d.line([(tx + 3, ty + 3), (tx + 3, ty + tile_sz - 4)], fill=(col[0] + 8, col[1] + 8, col[2] + 6), width=1)
            # Shadow bottom-right
            d.line([(tx + tile_sz - 3, ty + 4), (tx + tile_sz - 3, ty + tile_sz - 3)], fill=(col[0] - 10, col[1] - 10, col[2] - 8), width=1)
            d.line([(tx + 4, ty + tile_sz - 3), (tx + tile_sz - 3, ty + tile_sz - 3)], fill=(col[0] - 8, col[1] - 8, col[2] - 6), width=1)
    # Grout lines
    for gy in range(0, T, tile_sz):
        d.line([(0, gy), (T, gy)], fill=(170, 168, 162), width=2)
        d.line([(0, gy + 1), (T, gy + 1)], fill=(185, 183, 178), width=1)
    for gx in range(0, T, tile_sz):
        d.line([(gx, 0), (gx, T)], fill=(170, 168, 162), width=2)
        d.line([(gx + 1, 0), (gx + 1, T)], fill=(185, 183, 178), width=1)
    # Cracks on some tiles
    for i in range(3):
        if hashF(i, 0, 510) > 0.4:
            cx = hash_xy(i, 1, 510) % (T - 20) + 10
            cy = hash_xy(i, 2, 510) % (T - 20) + 10
            d.line([(cx - 12, cy - 8), (cx, cy + 2), (cx + 8, cy + 10)], fill=(140, 138, 130, 150), width=1)
            d.line([(cx, cy + 2), (cx + 14, cy - 4)], fill=(150, 148, 142, 120), width=1)
    # Stains
    for i in range(2):
        sx = hash_xy(i, 0, 520) % (T - 20) + 10
        sy = hash_xy(i, 1, 520) % (T - 20) + 10
        d.ellipse([sx - 6, sy - 4, sx + 6, sy + 4], fill=(195, 190, 182, 60))
    return img


def gen_ground_worn_carpet():
    """Dark red/brown worn carpet with frayed edges."""
    img = Image.new('RGBA', (T, T), (105, 42, 38))
    d = ImageDraw.Draw(img)
    # Texture fibers
    for y in range(0, T, 3):
        for x in range(0, T, 3):
            h = hashF(x, y, 530)
            r = int(90 + h * 35)
            d.rectangle([x, y, x + 2, y + 2], fill=(r, int(r * 0.42), int(r * 0.38)))
    # Worn spots (lighter patches)
    for i in range(6):
        wx = hash_xy(i, 0, 540) % (T - 30) + 15
        wy = hash_xy(i, 1, 540) % (T - 30) + 15
        wr = 8 + hash_xy(i, 2, 540) % 12
        d.ellipse([wx - wr, wy - wr, wx + wr, wy + wr], fill=(120, 55, 48, 70))
    # Darker stains
    for i in range(3):
        sx = hash_xy(i, 0, 550) % (T - 20) + 10
        sy = hash_xy(i, 1, 550) % (T - 20) + 10
        d.ellipse([sx - 10, sy - 6, sx + 10, sy + 6], fill=(70, 28, 24, 80))
    # Frayed edges
    for i in range(20):
        ex = hash_xy(i, 0, 560) % T
        d.line([(ex, 0), (ex + hash_xy(i, 1, 560) % 4 - 2, 3 + hash_xy(i, 2, 560) % 5)],
               fill=(85, 35, 30, 100), width=1)
        d.line([(ex, T - 1), (ex + hash_xy(i, 3, 560) % 4 - 2, T - 4 - hash_xy(i, 4, 560) % 5)],
               fill=(85, 35, 30, 100), width=1)
    # Subtle pattern (diamond shapes)
    for py in range(16, T - 16, 32):
        for px in range(16, T - 16, 32):
            d.polygon([(px, py - 6), (px + 5, py), (px, py + 6), (px - 5, py)],
                      fill=(115, 48, 42, 50))
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


# ---- 5 variantes de pierre grise coherentes pour l'exterieur du manoir ----
# Palette commune : gris 70-110, joints 50-60, highlights 115-125

def gen_wall_exterior_stone_1():
    """Pierre taillee reguliere — blocs rectangulaires bien alignes."""
    img = Image.new('RGBA', (T, T), (82, 80, 78))
    d = ImageDraw.Draw(img)
    bh, bw = T // 4, T // 2
    for row in range(4):
        off = (row % 2) * (bw // 2)
        for col in range(-1, 3):
            x1 = col * bw + off
            y1 = row * bh
            x2, y2 = min(T, x1 + bw - 2), min(T, y1 + bh - 2)
            if x2 <= max(0, x1): continue
            x1 = max(0, x1)
            h = hashF(row, col, 600)
            r = int(78 + h * 18)
            d.rectangle([x1+1, y1+1, x2, y2], fill=(r, r-2, r-5))
            d.line([(x1+2, y1+2), (x2-1, y1+2)], fill=(r+12, r+10, r+8), width=1)
            d.line([(x1+2, y2-1), (x2-1, y2-1)], fill=(r-10, r-12, r-13), width=1)
    # Joints
    for row in range(1, 4):
        d.line([(0, row*bh), (T, row*bh)], fill=(52, 50, 48), width=2)
    for row in range(4):
        off = (row % 2) * (bw // 2)
        for col in range(3):
            x = col * bw + off
            if 0 < x < T:
                d.line([(x, row*bh), (x, (row+1)*bh)], fill=(52, 50, 48), width=2)
    for i in range(6):
        d.line([(0, T-1-i), (T, T-1-i)], fill=(0,0,0, 18-i*3))
    return img


def gen_wall_exterior_stone_2():
    """Pierre irreguliere — blocs de tailles variees."""
    img = Image.new('RGBA', (T, T), (78, 76, 74))
    d = ImageDraw.Draw(img)
    stones = [
        (0, 0, 0.55, 0.42), (0.57, 0, 0.43, 0.38),
        (0, 0.44, 0.38, 0.56), (0.40, 0.40, 0.32, 0.30),
        (0.74, 0.40, 0.26, 0.32), (0.40, 0.72, 0.60, 0.28),
        (0, 0.44, 0.38, 0.28), (0.40, 0.72, 0.28, 0.28),
        (0.70, 0.74, 0.30, 0.26),
    ]
    for si, (sx, sy, sw, sh) in enumerate(stones):
        x1, y1 = int(sx*T), int(sy*T)
        x2, y2 = min(T-1, int((sx+sw)*T)), min(T-1, int((sy+sh)*T))
        if x2 <= x1 or y2 <= y1: continue
        h = hashF(si, 0, 610)
        r = int(75 + h * 22)
        d.rectangle([x1+1, y1+1, x2-1, y2-1], fill=(r, r-1, r-4))
        d.line([(x1+2, y1+2), (x2-2, y1+2)], fill=(r+10, r+9, r+7), width=1)
        d.rectangle([x1, y1, x2, y2], outline=(50, 48, 45), width=2)
    for i in range(6):
        d.line([(0, T-1-i), (T, T-1-i)], fill=(0,0,0, 18-i*3))
    return img


def gen_wall_exterior_stone_3():
    """Pierre avec erosion — surface usee par le temps."""
    img = gen_wall_exterior_stone_1().convert('RGBA')
    overlay = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # Erosion : taches sombres subtiles
    for i in range(8):
        cx = hash_xy(i, 0, 620) % (T-16) + 8
        cy = hash_xy(i, 1, 620) % (T-16) + 8
        r = 4 + hash_xy(i, 2, 620) % 8
        v = hash_xy(i, 3, 620) % 12
        od.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(58+v, 56+v, 52+v, 60))
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)
    # Petites fissures
    d.line([(T//3, 8), (T//3+5, T//2)], fill=(58, 56, 52), width=1)
    d.line([(T*2//3, T//4), (T*2//3-3, T*3//4)], fill=(56, 54, 50), width=1)
    return img


def gen_wall_exterior_stone_4():
    """Pierre avec lichen — taches subtiles gris-vert sur surface grise."""
    img = gen_wall_exterior_stone_2().convert('RGBA')
    overlay = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(6):
        cx = hash_xy(i, 0, 630) % (T-20) + 10
        cy = hash_xy(i, 1, 630) % (T-20) + 10
        r = 4 + hash_xy(i, 2, 630) % 6
        h = hashF(i, 3, 630)
        # Lichen subtil gris-vert, pas blanc
        col = (int(82+h*15), int(85+h*15), int(72+h*10), int(40+h*30))
        od.ellipse([cx-r, cy-r//2, cx+r, cy+r//2], fill=col)
    return Image.alpha_composite(img, overlay)


def gen_wall_exterior_stone_5():
    """Pierre mouillee — plus sombre en bas, traces d'eau."""
    img = gen_wall_exterior_stone_1().convert('RGBA')
    # Darken bottom half by blending with a dark overlay
    from PIL import ImageEnhance
    overlay = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(T//2, T):
        alpha = int((y - T//2) / (T//2) * 50)
        od.line([(0, y), (T, y)], fill=(0, 0, 8, alpha))
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)
    # Traces de ruissellement vertical (dark streaks)
    for i in range(3):
        x = hash_xy(i, 0, 640) % (T-10) + 5
        for y in range(T//3, T-5, 3):
            x += hash_xy(i, y, 641) % 3 - 1
            x = max(2, min(T-3, x))
            streak = Image.new('RGBA', (T, T), (0, 0, 0, 0))
            sd = ImageDraw.Draw(streak)
            sd.rectangle([x, y, x+1, y+2], fill=(0, 0, 5, 35))
            img = Image.alpha_composite(img, streak)
    return img


def gen_wall_front_dark_stone():
    """Pierre sombre presque noire — mur de donjon."""
    img = Image.new('RGBA', (T, T), (42, 42, 48))
    d = ImageDraw.Draw(img)
    stones = [
        (0, 0, T * 0.52, T * 0.45), (T * 0.54, 0, T * 0.46, T * 0.50),
        (0, T * 0.48, T * 0.48, T * 0.52), (T * 0.50, T * 0.52, T * 0.50, T * 0.48),
    ]
    for si, (sx, sy, sw, sh) in enumerate(stones):
        sx, sy, sw, sh = int(sx), int(sy), int(sw), int(sh)
        h = hashF(si, 0, 280)
        r = int(35 + h * 18)
        col = (r, r + 1, r + 5)
        d.rectangle([sx + 2, sy + 2, sx + sw - 3, sy + sh - 3], fill=col)
        d.line([(sx + 3, sy + 3), (sx + sw - 4, sy + 3)], fill=(col[0] + 10, col[1] + 10, col[2] + 8), width=2)
        d.line([(sx + sw - 3, sy + 4), (sx + sw - 3, sy + sh - 3)], fill=(col[0] - 8, col[1] - 8, col[2] - 6), width=2)
    for sx, sy, sw, sh in stones:
        d.rectangle([int(sx), int(sy), int(sx + sw), int(sy + sh)], outline=(28, 28, 35), width=2)
    for i in range(8):
        d.line([(0, T - 1 - i), (T, T - 1 - i)], fill=(0, 0, 0, 20 - i * 2))
    return img


def gen_wall_front_cracked_brick():
    """Briques fissurees avec lezardes."""
    img = Image.new('RGBA', (T, T), (90, 60, 48))
    d = ImageDraw.Draw(img)
    draw_bricks(d, T, T, 120, 62, 40, (65, 52, 45))
    # Grosses fissures
    d.line([(T//4, 5), (T//3, T//2), (T//4+10, T-8)], fill=(35, 30, 25), width=3)
    d.line([(T//3, T//2), (T*2//3, T//2+15)], fill=(35, 30, 25), width=2)
    d.line([(T*3//4, 8), (T*2//3, T//3), (T*3//4-5, T*2//3)], fill=(38, 32, 28), width=2)
    # Morceaux manquants
    d.rectangle([T//3-5, T//2-3, T//3+8, T//2+5], fill=(45, 35, 30))
    for i in range(8):
        d.line([(0, T - 1 - i), (T, T - 1 - i)], fill=(0, 0, 0, 20 - i * 2))
    return img


def gen_wall_front_cobblestone():
    """Moellons irreguliers — pierres rondes de tailles variees."""
    img = Image.new('RGBA', (T, T), (75, 72, 68))
    d = ImageDraw.Draw(img)
    random.seed(777)
    for i in range(12):
        cx = hash_xy(i, 0, 350) % (T - 20) + 10
        cy = hash_xy(i, 1, 350) % (T - 16) + 8
        rx = 8 + hash_xy(i, 2, 350) % 12
        ry = 6 + hash_xy(i, 3, 350) % 10
        h = hashF(i, 4, 350)
        col = (int(68 + h * 30), int(65 + h * 28), int(60 + h * 25))
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col)
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=(50, 48, 42), width=2)
        d.ellipse([cx - rx + 3, cy - ry + 2, cx - rx + 8, cy - ry + 5], fill=(col[0] + 12, col[1] + 12, col[2] + 10))
    random.seed(42)
    for i in range(8):
        d.line([(0, T - 1 - i), (T, T - 1 - i)], fill=(0, 0, 0, 18 - i * 2))
    return img


def gen_wall_front_vine_stone():
    """Pierre avec lierre grimpant — mur exterieur envahi."""
    img = gen_wall_front_gray_stone()
    d = ImageDraw.Draw(img)
    # Tiges de lierre verticales
    for vine in range(3):
        vx = 15 + hash_xy(vine, 0, 360) % (T - 30)
        d.line([(vx, 0), (vx + hash_xy(vine, 1, 360) % 8 - 4, T)], fill=(30, 65, 25), width=3)
        d.line([(vx + 1, 0), (vx + hash_xy(vine, 1, 360) % 8 - 3, T)], fill=(35, 75, 28), width=2)
        # Feuilles le long de la tige
        for ly in range(8, T - 5, 12):
            lx = vx + hash_xy(vine, ly, 370) % 12 - 6
            side = 1 if hash_xy(vine, ly, 371) % 2 == 0 else -1
            lx1, lx2 = min(lx + side * 2, lx + side * 12), max(lx + side * 2, lx + side * 12)
            d.ellipse([lx1, ly - 4, lx2, ly + 4], fill=(40, 95 + hash_xy(vine, ly, 372) % 30, 30))
            lx3, lx4 = min(lx + side * 3, lx + side * 10), max(lx + side * 3, lx + side * 10)
            d.ellipse([lx3, ly - 3, lx4, ly + 2], fill=(45, 110 + hash_xy(vine, ly, 373) % 20, 35))
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


def draw_fallen_books(d, cx, cy):
    """3-4 books scattered on floor, various colors."""
    books = [
        (cx - 18, cy - 8, 16, 22, (140, 45, 38)),
        (cx + 4, cy - 12, 14, 20, (38, 65, 140)),
        (cx - 6, cy + 4, 18, 14, (45, 110, 52)),
        (cx + 10, cy + 2, 12, 18, (130, 95, 40)),
    ]
    for bx, by, bw, bh, col in books:
        # Book shadow
        d.rectangle([bx + 2, by + 2, bx + bw + 2, by + bh + 2], fill=(30, 25, 20, 60))
        # Book cover
        d.rectangle([bx, by, bx + bw, by + bh], fill=col)
        # Spine line
        d.line([(bx + 2, by), (bx + 2, by + bh)], fill=(col[0] - 25, col[1] - 20, col[2] - 18), width=2)
        # Page edge
        d.rectangle([bx + 3, by + 2, bx + bw - 2, by + bh - 2], fill=(225, 218, 195))
        d.rectangle([bx + 3, by + 2, bx + bw - 2, by + bh - 2], outline=(col[0] - 15, col[1] - 12, col[2] - 10), width=1)
    # One open book
    d.polygon([(cx - 4, cy - 2), (cx - 18, cy - 10), (cx - 18, cy + 6)], fill=(220, 212, 190))
    d.polygon([(cx - 4, cy - 2), (cx + 8, cy - 8), (cx + 8, cy + 8)], fill=(215, 208, 185))
    d.line([(cx - 4, cy - 2), (cx - 4, cy + 8)], fill=(80, 60, 40), width=1)


def draw_kitchen_utensils(d, cx, cy):
    """Knife, spoon, broken plate scattered."""
    # Broken plate
    d.pieslice([cx - 20, cy - 12, cx + 4, cy + 12], 0, 270, fill=(210, 205, 195))
    d.pieslice([cx - 20, cy - 12, cx + 4, cy + 12], 0, 270, outline=(150, 145, 135), width=2)
    d.pieslice([cx - 16, cy - 8, cx, cy + 8], 0, 270, fill=(225, 220, 212))
    # Plate shard nearby
    d.polygon([(cx + 8, cy - 6), (cx + 16, cy - 2), (cx + 10, cy + 4)], fill=(205, 200, 190))
    d.polygon([(cx + 8, cy - 6), (cx + 16, cy - 2), (cx + 10, cy + 4)], outline=(150, 145, 135), width=1)
    # Knife
    d.rectangle([cx + 12, cy + 6, cx + 14, cy + 22], fill=(110, 75, 45))  # handle
    d.polygon([(cx + 11, cy + 4), (cx + 15, cy + 4), (cx + 13, cy - 10)], fill=(180, 185, 192))  # blade
    d.line([(cx + 13, cy - 10), (cx + 13, cy + 4)], fill=(210, 215, 220), width=1)  # highlight
    # Spoon
    d.ellipse([cx - 10, cy + 10, cx - 2, cy + 18], fill=(170, 175, 182))
    d.ellipse([cx - 8, cy + 12, cx - 4, cy + 16], fill=(190, 195, 200))
    d.rectangle([cx - 7, cy + 18, cx - 5, cy + 30], fill=(160, 165, 172))


def draw_broken_toys(d, cx, cy):
    """Small doll, wooden blocks scattered."""
    # Wooden block 1
    d.rectangle([cx - 22, cy - 8, cx - 10, cy + 4], fill=(180, 140, 80))
    d.rectangle([cx - 22, cy - 8, cx - 10, cy + 4], outline=(120, 90, 50), width=2)
    d.text((cx - 19, cy - 6), "A", fill=(180, 50, 40))
    # Wooden block 2 (tilted)
    d.polygon([(cx + 8, cy - 12), (cx + 20, cy - 8), (cx + 16, cy + 4), (cx + 4, cy)],
              fill=(80, 140, 180))
    d.polygon([(cx + 8, cy - 12), (cx + 20, cy - 8), (cx + 16, cy + 4), (cx + 4, cy)],
              outline=(50, 90, 120), width=2)
    # Small doll body
    d.ellipse([cx - 6, cy + 6, cx + 2, cy + 14], fill=(220, 180, 160))  # head
    d.rectangle([cx - 5, cy + 14, cx + 1, cy + 26], fill=(180, 60, 70))  # dress
    d.line([(cx - 8, cy + 18), (cx - 5, cy + 16)], fill=(220, 180, 160), width=2)  # arm
    d.line([(cx + 1, cy + 16), (cx + 5, cy + 20)], fill=(220, 180, 160), width=2)  # arm
    # Eyes
    d.ellipse([cx - 4, cy + 8, cx - 2, cy + 10], fill=(30, 30, 30))
    d.ellipse([cx, cy + 8, cx + 2, cy + 10], fill=(30, 30, 30))
    # Broken arm detached
    d.line([(cx + 10, cy + 14), (cx + 18, cy + 18)], fill=(220, 180, 160), width=2)


def draw_broken_mirror(d, cx, cy):
    """Shards of glass reflective."""
    # Main large shard
    d.polygon([(cx - 16, cy - 18), (cx + 8, cy - 14), (cx + 12, cy + 4), (cx - 4, cy + 10), (cx - 18, cy - 2)],
              fill=(180, 195, 210, 140))
    d.polygon([(cx - 16, cy - 18), (cx + 8, cy - 14), (cx + 12, cy + 4), (cx - 4, cy + 10), (cx - 18, cy - 2)],
              outline=(140, 150, 165, 180), width=2)
    # Reflection highlight
    d.line([(cx - 10, cy - 12), (cx + 4, cy - 4)], fill=(240, 245, 255, 100), width=2)
    d.line([(cx - 8, cy - 6), (cx + 2, cy + 2)], fill=(230, 235, 245, 80), width=1)
    # Small shards
    shards = [
        [(cx + 14, cy - 8), (cx + 22, cy - 4), (cx + 18, cy + 2)],
        [(cx - 8, cy + 12), (cx + 2, cy + 14), (cx - 2, cy + 22)],
        [(cx + 6, cy + 8), (cx + 14, cy + 10), (cx + 10, cy + 18)],
        [(cx - 22, cy + 4), (cx - 14, cy + 2), (cx - 16, cy + 12)],
    ]
    for shard in shards:
        d.polygon(shard, fill=(175, 190, 205, 120))
        d.polygon(shard, outline=(130, 140, 155, 150), width=1)
    # Sparkle points
    for i in range(3):
        sx = cx - 10 + hash_xy(i, 0, 600) % 28
        sy = cy - 10 + hash_xy(i, 1, 600) % 24
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255, 140))


def draw_water_puddle(d, cx, cy):
    """Blue-gray water puddle (different from existing puddle)."""
    # Larger irregular shape
    d.ellipse([cx - 22, cy - 12, cx + 18, cy + 10], fill=(55, 80, 110, 90))
    d.ellipse([cx - 16, cy - 8, cx + 14, cy + 8], fill=(65, 95, 125, 80))
    d.ellipse([cx + 4, cy - 2, cx + 24, cy + 14], fill=(50, 75, 105, 70))
    # Ripples
    d.arc([cx - 10, cy - 5, cx + 6, cy + 5], 0, 360, fill=(90, 120, 150, 50), width=1)
    d.arc([cx - 6, cy - 3, cx + 2, cy + 3], 0, 360, fill=(100, 130, 160, 40), width=1)
    # Reflections
    d.ellipse([cx - 4, cy - 3, cx + 2, cy + 1], fill=(140, 165, 195, 50))
    d.ellipse([cx + 8, cy + 2, cx + 14, cy + 6], fill=(130, 155, 185, 40))
    # Edge darkening
    d.arc([cx - 22, cy - 12, cx + 18, cy + 10], 0, 360, fill=(35, 55, 80, 40), width=2)


# ==================== FURNITURE ====================

def gen_furniture_bed():
    """Top-down view of a broken bed with torn sheets (2x1 tile: 128x64)."""
    # Actually 256x128 at T scale for 2x1 tiles, but we use 128x64 concept
    # The atlas cell is 128 wide, so 2-tile = 256x128
    w, h = T * 2, T
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Shadow
    d.rounded_rectangle([6, 6, w - 4, h - 4], radius=4, fill=(0, 0, 0, 40))
    # Bed frame (dark wood)
    d.rounded_rectangle([2, 2, w - 6, h - 6], radius=6, fill=(85, 55, 32))
    d.rounded_rectangle([2, 2, w - 6, h - 6], radius=6, outline=(50, 32, 18), width=3)
    # Headboard (left side in top-down)
    d.rectangle([2, 2, 24, h - 6], fill=(70, 42, 24))
    d.rectangle([4, 4, 22, h - 8], fill=(90, 58, 35))
    d.rectangle([2, 2, 24, h - 6], outline=(45, 28, 15), width=2)
    # Mattress
    d.rectangle([26, 8, w - 12, h - 12], fill=(180, 170, 155))
    # Torn sheets (white with wrinkles)
    d.rectangle([30, 12, w - 40, h - 16], fill=(210, 205, 195))
    # Wrinkle lines
    for i in range(5):
        wy = 18 + i * (h - 40) // 5
        d.line([(40, wy), (w - 50, wy + hash_xy(i, 0, 700) % 6 - 3)],
               fill=(185, 180, 170), width=1)
    # Pillow
    d.rounded_rectangle([30, h // 2 - 18, 70, h // 2 + 18], radius=8, fill=(220, 215, 205))
    d.rounded_rectangle([30, h // 2 - 18, 70, h // 2 + 18], radius=8, outline=(190, 185, 175), width=2)
    # Blood stain on sheets
    d.ellipse([w // 2, h // 2 - 10, w // 2 + 28, h // 2 + 8], fill=(130, 30, 25, 100))
    # Torn edge
    for i in range(8):
        tx = w - 40 + hash_xy(i, 0, 710) % 20
        ty = 14 + hash_xy(i, 1, 710) % (h - 32)
        d.line([(w - 40, ty), (tx, ty + hash_xy(i, 2, 710) % 6 - 3)],
               fill=(200, 195, 185), width=1)
    return img


def gen_furniture_long_table():
    """Wooden table seen from above (2x1 tile)."""
    w, h = T * 2, T
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Shadow
    d.rounded_rectangle([6, 6, w - 2, h - 2], radius=3, fill=(0, 0, 0, 40))
    # Table surface
    base = (145, 105, 65)
    d.rounded_rectangle([2, 4, w - 6, h - 6], radius=4, fill=base)
    # Planks
    plank_h = (h - 12) // 4
    for py in range(6, h - 8, plank_h):
        ph = hashF(0, py, 720)
        col = (int(base[0] + ph * 18 - 8), int(base[1] + ph * 14 - 6), int(base[2] + ph * 10 - 4))
        d.rectangle([4, py, w - 8, py + plank_h - 2], fill=col)
        # Grain lines
        for gx in range(8, w - 12, 6):
            if hashF(gx, py, 730) > 0.55:
                d.line([(gx, py + 2), (gx + 4 + hash_xy(gx, py, 740) % 8, py + 2)],
                       fill=(col[0] - 12, col[1] - 10, col[2] - 8), width=1)
    # Edge highlight
    d.line([(4, 6), (w - 8, 6)], fill=(base[0] + 15, base[1] + 12, base[2] + 10), width=2)
    # Edge shadow
    d.line([(4, h - 8), (w - 8, h - 8)], fill=(base[0] - 20, base[1] - 18, base[2] - 14), width=2)
    # Outline
    d.rounded_rectangle([2, 4, w - 6, h - 6], radius=4, outline=(60, 40, 22), width=3)
    # Scratches
    for i in range(3):
        sx = 20 + hash_xy(i, 0, 750) % (w - 50)
        sy = 12 + hash_xy(i, 1, 750) % (h - 28)
        d.line([(sx, sy), (sx + 15 + hash_xy(i, 2, 750) % 20, sy + hash_xy(i, 3, 750) % 6 - 3)],
               fill=(base[0] - 15, base[1] - 12, base[2] - 10, 100), width=1)
    return img


def gen_furniture_bookshelf():
    """Bookshelf obstacle, tall look (1x1 tile)."""
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Shadow
    d.rectangle([4, 4, T - 2, T - 2], fill=(0, 0, 0, 40))
    # Frame
    frame_col = (72, 48, 28)
    d.rectangle([0, 0, T - 4, T - 4], fill=frame_col)
    d.rectangle([0, 0, T - 4, T - 4], outline=(42, 28, 15), width=3)
    # Shelves (4 rows)
    shelf_h = (T - 12) // 4
    for sy in range(4, T - 8, shelf_h):
        # Shelf plank
        d.rectangle([4, sy + shelf_h - 3, T - 8, sy + shelf_h], fill=(60, 38, 20))
        # Books on this shelf
        bx = 6
        while bx < T - 14:
            bw = 6 + hash_xy(bx, sy, 760) % 10
            bh = shelf_h - 8 + hash_xy(bx, sy, 770) % 6
            colors = [(140, 42, 35), (35, 55, 130), (42, 105, 48), (130, 95, 35),
                      (95, 35, 110), (35, 100, 110), (110, 55, 42)]
            col = colors[hash_xy(bx, sy, 790) % len(colors)]
            by = sy + shelf_h - 4 - bh
            d.rectangle([bx, by, bx + bw, sy + shelf_h - 4], fill=col)
            d.line([(bx + 1, by), (bx + 1, sy + shelf_h - 4)], fill=(col[0] + 15, col[1] + 12, col[2] + 10), width=1)
            bx += bw + 2
    # Top ornament line
    d.rectangle([0, 0, T - 4, 5], fill=(58, 38, 20))
    d.line([(1, 4), (T - 5, 4)], fill=(82, 58, 35), width=1)
    return img


def gen_furniture_bathtub():
    """White bathtub with dark water inside (2x1 tile)."""
    w, h = T * 2, T
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Shadow
    d.rounded_rectangle([6, 6, w - 2, h - 2], radius=12, fill=(0, 0, 0, 40))
    # Outer tub (white porcelain)
    d.rounded_rectangle([2, 2, w - 6, h - 6], radius=14, fill=(230, 228, 222))
    d.rounded_rectangle([2, 2, w - 6, h - 6], radius=14, outline=(160, 158, 150), width=3)
    # Rim highlight
    d.rounded_rectangle([4, 4, w - 8, h - 8], radius=12, outline=(245, 242, 238), width=2)
    # Inner tub
    d.rounded_rectangle([14, 14, w - 18, h - 18], radius=10, fill=(45, 50, 58))
    # Dark water inside
    d.rounded_rectangle([16, 16, w - 20, h - 20], radius=8, fill=(35, 42, 55))
    # Water surface details
    for i in range(4):
        rx = 30 + hash_xy(i, 0, 800) % (w - 70)
        ry = 24 + hash_xy(i, 1, 800) % (h - 50)
        d.ellipse([rx - 8, ry - 3, rx + 8, ry + 3], fill=(45, 55, 68, 80))
    # Reflection on water
    d.ellipse([w // 2 - 15, h // 2 - 8, w // 2 + 15, h // 2 + 4], fill=(60, 70, 85, 50))
    # Blood in water
    d.ellipse([w // 2 + 20, h // 2 - 4, w // 2 + 45, h // 2 + 8], fill=(80, 25, 22, 70))
    # Faucet
    d.rectangle([w - 30, h // 2 - 6, w - 20, h // 2 + 6], fill=(160, 162, 168))
    d.ellipse([w - 26, h // 2 - 10, w - 18, h // 2 - 4], fill=(170, 172, 178))
    # Claw feet visible at corners
    for fx, fy in [(8, 8), (8, h - 12), (w - 14, 8), (w - 14, h - 12)]:
        d.ellipse([fx, fy, fx + 6, fy + 6], fill=(160, 155, 145))
    return img


def gen_furniture_wardrobe():
    """Dark wooden wardrobe (1x1 tile, hides the boss)."""
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Shadow
    d.rectangle([4, 4, T - 1, T - 1], fill=(0, 0, 0, 45))
    # Main body
    base = (62, 42, 25)
    d.rectangle([0, 0, T - 4, T - 4], fill=base)
    # Two doors
    door_w = (T - 12) // 2
    for dx in [4, 6 + door_w]:
        d.rectangle([dx, 4, dx + door_w, T - 8], fill=(72, 50, 30))
        d.rectangle([dx, 4, dx + door_w, T - 8], outline=(45, 28, 15), width=2)
        # Panel inset
        d.rectangle([dx + 6, 10, dx + door_w - 6, T // 2 - 4], fill=(65, 44, 26))
        d.rectangle([dx + 6, T // 2 + 4, dx + door_w - 6, T - 14], fill=(65, 44, 26))
        # Handle
        hx = dx + door_w - 10
        hy = T // 2
        d.ellipse([hx - 3, hy - 3, hx + 3, hy + 3], fill=(140, 135, 100))
        d.ellipse([hx - 1, hy - 1, hx + 1, hy + 1], fill=(180, 175, 140))
    # Top molding
    d.rectangle([0, 0, T - 4, 5], fill=(52, 35, 20))
    d.line([(1, 4), (T - 5, 4)], fill=(78, 55, 35), width=1)
    # Bottom base
    d.rectangle([0, T - 8, T - 4, T - 4], fill=(52, 35, 20))
    # Outline
    d.rectangle([0, 0, T - 4, T - 4], outline=(35, 22, 12), width=3)
    # Mysterious glow from crack between doors
    d.line([(T // 2 - 1, 8), (T // 2 - 1, T - 10)], fill=(120, 180, 80, 60), width=2)
    return img


def gen_furniture_fireplace():
    """Stone fireplace/oven (1x1 tile)."""
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Shadow
    d.rectangle([4, 4, T - 1, T - 1], fill=(0, 0, 0, 40))
    # Stone body
    d.rectangle([0, 0, T - 4, T - 4], fill=(125, 118, 108))
    # Stone texture
    stones = [
        (2, 2, T // 2 - 4, T // 3 - 2), (T // 2 - 1, 2, T // 2 - 2, T // 3 - 2),
        (2, T // 3, T // 3, T // 3), (T // 3 + 2, T // 3, T // 3, T // 3),
        (T * 2 // 3 + 2, T // 3, T // 3 - 6, T // 3),
    ]
    for sx, sy, sw, sh in stones:
        h = hashF(sx, sy, 810)
        col = (int(115 + h * 22), int(108 + h * 20), int(98 + h * 18))
        d.rectangle([sx, sy, sx + sw, sy + sh], fill=col)
        d.rectangle([sx, sy, sx + sw, sy + sh], outline=(80, 75, 68), width=1)
    # Firebox opening (dark)
    fy = T // 2
    fh = T // 2 - 10
    d.rounded_rectangle([12, fy, T - 16, T - 8], radius=4, fill=(25, 20, 18))
    # Embers glow
    d.ellipse([T // 2 - 15, T - 22, T // 2 + 10, T - 12], fill=(120, 40, 20, 80))
    d.ellipse([T // 2 - 8, T - 18, T // 2 + 4, T - 14], fill=(180, 70, 25, 60))
    # Ash
    for i in range(5):
        ax = 16 + hash_xy(i, 0, 820) % (T - 40)
        ay = fy + 8 + hash_xy(i, 1, 820) % (fh - 10)
        d.ellipse([ax - 3, ay - 1, ax + 3, ay + 1], fill=(60, 55, 50, 80))
    # Top mantle
    d.rectangle([0, 0, T - 4, 8], fill=(108, 100, 90))
    d.line([(1, 7), (T - 5, 7)], fill=(135, 128, 118), width=1)
    # Outline
    d.rectangle([0, 0, T - 4, T - 4], outline=(50, 45, 38), width=3)
    return img


def gen_furniture_cradle():
    """Small broken baby cradle (1x1 tile)."""
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Shadow
    d.ellipse([10, T // 2 + 10, T - 10, T - 6], fill=(0, 0, 0, 35))
    # Rockers (bottom curved pieces)
    d.arc([8, T - 30, T - 12, T - 4], 0, 180, fill=(95, 65, 38), width=4)
    # Cradle body
    base = (120, 85, 52)
    d.rounded_rectangle([14, 16, T - 18, T - 16], radius=6, fill=base)
    d.rounded_rectangle([14, 16, T - 18, T - 16], radius=6, outline=(70, 48, 28), width=3)
    # Inner
    d.rounded_rectangle([20, 22, T - 24, T - 22], radius=4, fill=(160, 140, 115))
    # Small blanket
    d.rounded_rectangle([24, 30, T - 28, T - 26], radius=3, fill=(180, 175, 210))
    d.line([(28, 50), (T - 32, 48)], fill=(160, 155, 190), width=1)
    # Headboard (left side)
    d.rectangle([14, 14, 20, T - 16], fill=(100, 68, 38))
    d.rectangle([14, 8, 20, 16], fill=(90, 60, 32))
    # Footboard (right) - broken, tilted
    d.polygon([(T - 22, 18), (T - 16, 14), (T - 14, T - 18), (T - 20, T - 16)],
              fill=(100, 68, 38))
    # Crack in wood
    d.line([(T // 2, 18), (T // 2 + 6, T // 2), (T // 2 - 2, T - 22)],
           fill=(60, 40, 22, 150), width=2)
    return img


def gen_furniture_stairs_broken():
    """Escalier detruit vu de dessus — marches cassees, debris."""
    img = Image.new('RGBA', (T * 2, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w, h = T * 2, T
    # Base pierre
    d.rectangle([4, 4, w - 5, h - 5], fill=(72, 68, 62))
    # Marches (5 marches avec perspective)
    step_h = (h - 10) // 5
    for i in range(5):
        y = 5 + i * step_h
        # Marche de plus en plus large vers le bas (perspective)
        indent = (4 - i) * 6
        col_base = (85 + i * 8, 80 + i * 7, 72 + i * 6)
        # Marche intacte ou cassee
        if i == 1 or i == 3:
            # Marche cassee — trou noir + debris
            d.rectangle([indent + 4, y + 2, w - indent - 5, y + step_h - 2], fill=(25, 22, 18))
            # Debris
            for j in range(6):
                dx = indent + 10 + hash_xy(i, j, 700) % (w - indent * 2 - 25)
                dy = y + 3 + hash_xy(i, j + 1, 700) % (step_h - 6)
                sz = 3 + hash_xy(i, j + 2, 700) % 5
                d.rectangle([dx, dy, dx + sz, dy + sz - 1], fill=(col_base[0] - 10, col_base[1] - 8, col_base[2] - 6))
            # Fissure
            d.line([(indent + 15, y + step_h // 2), (w // 2, y + 3)], fill=(40, 35, 28), width=2)
        else:
            # Marche intacte
            d.rectangle([indent + 4, y + 1, w - indent - 5, y + step_h - 1], fill=col_base)
            # Highlight haut
            d.line([(indent + 5, y + 2), (w - indent - 6, y + 2)], fill=(col_base[0] + 15, col_base[1] + 13, col_base[2] + 10), width=1)
            # Ombre bas
            d.line([(indent + 5, y + step_h - 2), (w - indent - 6, y + step_h - 2)], fill=(col_base[0] - 12, col_base[1] - 10, col_base[2] - 8), width=1)
            # Usure
            if hash_xy(i, 10, 710) % 3 == 0:
                d.ellipse([indent + 20 + hash_xy(i, 11, 710) % 40, y + 4, indent + 30 + hash_xy(i, 11, 710) % 40, y + step_h - 4],
                          fill=(col_base[0] - 8, col_base[1] - 6, col_base[2] - 5, 100))
    # Rampe cassee gauche
    d.rectangle([2, 2, 8, h - 3], fill=(55, 38, 22))
    d.rectangle([2, 2, 8, h // 3], fill=(55, 38, 22))
    d.line([(5, h // 3), (5, h // 3 + 15)], fill=(45, 30, 18), width=2)  # cassee
    # Rampe droite (intacte)
    d.rectangle([w - 9, 2, w - 3, h - 3], fill=(60, 42, 25))
    d.rectangle([w - 9, 2, w - 3, h - 3], outline=(35, 25, 15), width=2)
    # Outline
    d.rectangle([2, 2, w - 3, h - 3], outline=(35, 28, 18), width=3)
    return img


def gen_furniture_chandelier():
    """Grand lustre suspendu vu de dessus — cercle dore avec bougies."""
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = T // 2, T // 2
    # Halo de lumiere chaud
    for r in range(55, 10, -2):
        a = max(0, 40 - r // 2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 180, 50, a))
    # Cercle principal (metal dore)
    d.ellipse([cx - 35, cy - 35, cx + 35, cy + 35], outline=(180, 150, 60), width=4)
    d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], outline=(140, 115, 45), width=2)
    # Cercle interieur
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], outline=(160, 130, 50), width=3)
    # Bras radiaux (8)
    for i in range(8):
        angle = i * math.pi / 4
        x1 = cx + int(math.cos(angle) * 18)
        y1 = cy + int(math.sin(angle) * 18)
        x2 = cx + int(math.cos(angle) * 33)
        y2 = cy + int(math.sin(angle) * 33)
        d.line([(x1, y1), (x2, y2)], fill=(170, 140, 55), width=3)
        # Bougie au bout
        bx, by = cx + int(math.cos(angle) * 36), cy + int(math.sin(angle) * 36)
        d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(220, 210, 185))
        d.ellipse([bx - 5, by - 5, bx + 5, by + 5], outline=(160, 130, 50), width=1)
        # Flamme
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(255, 210, 80))
        d.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=(255, 250, 200))
    # Centre decoratif
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(160, 130, 50))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(190, 160, 70))
    # Chaines (4 lignes vers le centre)
    for i in range(4):
        angle = i * math.pi / 2 + math.pi / 4
        x1 = cx + int(math.cos(angle) * 6)
        y1 = cy + int(math.sin(angle) * 6)
        d.line([(cx, cy), (x1, y1)], fill=(120, 100, 40), width=2)
    # Outline
    d.ellipse([cx - 35, cy - 35, cx + 35, cy + 35], outline=(80, 65, 25), width=2)
    return img


def gen_furniture_grand_door():
    """Grande porte d'entree massive du manoir — vue de dessus/face."""
    img = Image.new('RGBA', (T * 2, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w, h = T * 2, T
    # Cadre en pierre
    d.rectangle([0, 0, w - 1, h - 1], fill=(85, 75, 65))
    d.rectangle([3, 3, w - 4, h - 4], fill=(95, 85, 72))
    # Piliers lateraux
    d.rectangle([0, 0, 18, h - 1], fill=(105, 92, 78))
    d.rectangle([w - 19, 0, w - 1, h - 1], fill=(105, 92, 78))
    d.line([(2, 0), (2, h)], fill=(120, 108, 92), width=2)
    d.line([(w - 3, 0), (w - 3, h)], fill=(120, 108, 92), width=2)
    d.rectangle([0, 0, 18, h - 1], outline=(50, 40, 30), width=2)
    d.rectangle([w - 19, 0, w - 1, h - 1], outline=(50, 40, 30), width=2)
    # Porte gauche
    d.rectangle([20, 4, w // 2 - 3, h - 5], fill=(110, 72, 38))
    for py in range(8, h - 8, 14):
        d.line([(22, py), (w // 2 - 5, py)], fill=(88, 55, 28), width=1)
    # Panneau decoratif
    d.rectangle([30, 15, w // 2 - 12, h // 2 - 5], outline=(90, 58, 30), width=2)
    d.rectangle([30, h // 2 + 5, w // 2 - 12, h - 18], outline=(90, 58, 30), width=2)
    # Porte droite
    d.rectangle([w // 2 + 2, 4, w - 21, h - 5], fill=(110, 72, 38))
    for py in range(8, h - 8, 14):
        d.line([(w // 2 + 4, py), (w - 23, py)], fill=(88, 55, 28), width=1)
    d.rectangle([w // 2 + 12, 15, w - 31, h // 2 - 5], outline=(90, 58, 30), width=2)
    d.rectangle([w // 2 + 12, h // 2 + 5, w - 31, h - 18], outline=(90, 58, 30), width=2)
    # Poignees (anneaux dores)
    for px in [w // 2 - 10, w // 2 + 10]:
        d.ellipse([px - 6, h // 2 - 6, px + 6, h // 2 + 6], outline=(200, 180, 70), width=3)
        d.ellipse([px - 2, h // 2 - 8, px + 2, h // 2 - 4], fill=(200, 180, 70))
    # Arche au-dessus (decorative)
    d.arc([25, -20, w - 26, 25], 0, 180, fill=(85, 70, 55), width=4)
    # Ligne de separation
    d.line([(w // 2, 4), (w // 2, h - 5)], fill=(50, 35, 22), width=3)
    # Outline general
    d.rectangle([0, 0, w - 1, h - 1], outline=(35, 28, 20), width=3)
    # Clous decoratifs
    for py in [12, h - 13]:
        for px in [25, w - 26]:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(140, 130, 60))
    return img


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


def gen_bush_thorny():
    """Buisson epineux sombre."""
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = T // 2, T // 2 + 10
    d.ellipse([cx - 28, cy + 12, cx + 28, cy + 22], fill=(0, 0, 0, 40))
    d.ellipse([cx - 28, cy - 15, cx + 28, cy + 15], fill=(22, 55, 18))
    d.ellipse([cx - 18, cy - 18, cx + 8, cy - 2], fill=(28, 68, 22))
    # Epines
    for i in range(8):
        angle = i * math.pi / 4
        sx = cx + int(math.cos(angle) * 26)
        sy = cy + int(math.sin(angle) * 13)
        ex = cx + int(math.cos(angle) * 35)
        ey = cy + int(math.sin(angle) * 18)
        d.line([(sx, sy), (ex, ey)], fill=(35, 25, 15), width=2)
    d.ellipse([cx - 28, cy - 15, cx + 28, cy + 15], outline=(15, 38, 12), width=2)
    return img


def gen_bush_fern():
    """Fougere basse."""
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = T // 2, T // 2 + 15
    d.ellipse([cx - 20, cy + 8, cx + 20, cy + 16], fill=(0, 0, 0, 35))
    # Fronds
    for i in range(6):
        angle = -math.pi/2 + (i - 2.5) * 0.5
        for j in range(8, 32, 4):
            fx = cx + int(math.cos(angle) * j)
            fy = cy - int(abs(math.sin(angle)) * j * 0.4) + 5
            sz = max(2, 6 - j // 8)
            d.ellipse([fx - sz, fy - sz//2, fx + sz, fy + sz//2], fill=(20, 60 + j, 15))
    return img


def gen_bush_dead():
    """Buisson mort / sec."""
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = T // 2, T // 2 + 10
    d.ellipse([cx - 22, cy + 10, cx + 22, cy + 18], fill=(0, 0, 0, 35))
    # Branches seches
    for i in range(10):
        angle = i * math.pi / 5 + 0.3
        length = 15 + hash_xy(i, 0, 500) % 18
        sx, sy = cx, cy
        ex = cx + int(math.cos(angle) * length)
        ey = cy + int(math.sin(angle) * length * 0.5) - 8
        d.line([(sx, sy), (ex, ey)], fill=(55, 38, 22), width=2)
        # Petites branches
        if hash_xy(i, 1, 500) % 3 == 0:
            bx = (sx + ex) // 2
            by = (sy + ey) // 2
            d.line([(bx, by), (bx + hash_xy(i, 2, 500) % 10 - 5, by - 8)], fill=(48, 32, 18), width=1)
    # Quelques feuilles mortes
    for i in range(4):
        lx = cx - 15 + hash_xy(i, 0, 510) % 30
        ly = cy + hash_xy(i, 1, 510) % 10
        d.ellipse([lx - 3, ly - 2, lx + 3, ly + 2], fill=(85, 55, 20, 120))
    return img


def gen_tree_pine():
    """Sapin sombre — forme triangulaire, vert fonce."""
    S = T * 2  # bigger than a tile
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = S // 2, S // 2 + 10
    # Ombre au sol
    d.ellipse([cx - 35, cy + 40, cx + 35, cy + 55], fill=(0, 0, 0, 50))
    # Tronc
    d.rectangle([cx - 6, cy + 10, cx + 6, cy + 45], fill=(65, 42, 25))
    d.rectangle([cx - 6, cy + 10, cx + 6, cy + 45], outline=(40, 25, 15), width=2)
    # 3 etages de feuillage (triangles empiles)
    layers = [
        (cy + 15, 42, (25, 82, 28)),   # bas, large
        (cy - 5, 35, (30, 95, 32)),    # milieu
        (cy - 22, 26, (35, 108, 38)),  # haut
    ]
    for ly, w, col in layers:
        d.polygon([(cx, ly - 30), (cx - w, ly + 10), (cx + w, ly + 10)], fill=col)
        d.polygon([(cx, ly - 30), (cx - w, ly + 10), (cx + w, ly + 10)], outline=(18, 55, 15), width=2)
        # Neige/givre sur les branches
        d.line([(cx - w + 8, ly + 8), (cx - w + 18, ly + 2)], fill=(180, 195, 180, 80), width=2)
    # Pointe
    d.polygon([(cx, cy - 65), (cx - 8, cy - 45), (cx + 8, cy - 45)], fill=(38, 115, 42))
    return img


def gen_tree_oak():
    """Chene — tronc epais, couronne ronde et touffue."""
    S = T * 2
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = S // 2, S // 2 + 15
    # Ombre
    d.ellipse([cx - 40, cy + 35, cx + 40, cy + 52], fill=(0, 0, 0, 45))
    # Tronc (epais, noueux)
    d.rectangle([cx - 10, cy - 5, cx + 10, cy + 42], fill=(72, 48, 28))
    d.rectangle([cx - 10, cy - 5, cx + 10, cy + 42], outline=(45, 28, 15), width=2)
    # Branches visibles
    d.line([(cx - 8, cy + 5), (cx - 25, cy - 15)], fill=(65, 42, 22), width=4)
    d.line([(cx + 8, cy + 5), (cx + 28, cy - 12)], fill=(65, 42, 22), width=4)
    d.line([(cx - 5, cy), (cx - 18, cy - 28)], fill=(60, 38, 20), width=3)
    # Couronne (plusieurs cercles qui se chevauchent)
    for ox, oy, r, col in [
        (-18, -25, 22, (35, 100, 30)),
        (15, -28, 20, (32, 92, 28)),
        (0, -38, 24, (38, 108, 35)),
        (-10, -42, 18, (42, 118, 38)),
        (12, -40, 16, (40, 112, 36)),
        (-25, -18, 15, (30, 88, 25)),
        (25, -20, 14, (33, 95, 28)),
    ]:
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r], fill=col)
    # Outline de la couronne
    d.ellipse([cx - 42, cy - 58, cx + 42, cy - 5], outline=(18, 55, 15), width=3)
    # Highlights
    d.ellipse([cx - 12, cy - 50, cx + 5, cy - 38], fill=(48, 128, 42, 150))
    return img


def gen_tree_spooky():
    """Arbre mort effrayant — branches tordues, pas de feuilles, silhouette sombre."""
    S = T * 2
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = S // 2, S // 2 + 15
    # Ombre
    d.ellipse([cx - 30, cy + 38, cx + 30, cy + 50], fill=(0, 0, 0, 40))
    # Tronc tordu
    trunk_col = (42, 30, 18)
    d.polygon([(cx - 12, cy + 42), (cx + 12, cy + 42), (cx + 8, cy - 20), (cx - 8, cy - 20)],
              fill=trunk_col)
    d.polygon([(cx - 12, cy + 42), (cx + 12, cy + 42), (cx + 8, cy - 20), (cx - 8, cy - 20)],
              outline=(30, 20, 10), width=2)
    # Trou dans le tronc (visage effrayant)
    d.ellipse([cx - 5, cy + 8, cx + 5, cy + 18], fill=(15, 10, 5))
    d.ellipse([cx - 3, cy + 10, cx - 1, cy + 13], fill=(60, 180, 60, 80))  # oeil gauche luisant
    d.ellipse([cx + 1, cy + 10, cx + 3, cy + 13], fill=(60, 180, 60, 80))  # oeil droit
    # Branches mortes tordues (nombreuses)
    branches = [
        [(cx, cy - 20), (cx - 30, cy - 45), (cx - 45, cy - 55)],
        [(cx, cy - 20), (cx + 25, cy - 48), (cx + 42, cy - 62)],
        [(cx - 30, cy - 45), (cx - 38, cy - 35), (cx - 50, cy - 38)],
        [(cx + 25, cy - 48), (cx + 35, cy - 38)],
        [(cx, cy - 18), (cx - 15, cy - 55), (cx - 8, cy - 68)],
        [(cx, cy - 18), (cx + 12, cy - 58), (cx + 18, cy - 70)],
        [(cx - 45, cy - 55), (cx - 52, cy - 48)],
        [(cx + 42, cy - 62), (cx + 50, cy - 55)],
        [(cx - 8, cy - 68), (cx - 18, cy - 72)],
        [(cx + 18, cy - 70), (cx + 25, cy - 68)],
    ]
    for branch in branches:
        d.line(branch, fill=trunk_col, width=3)
    # Branches plus fines
    thin_branches = [
        [(cx - 38, cy - 35), (cx - 48, cy - 30)],
        [(cx + 35, cy - 38), (cx + 45, cy - 32)],
        [(cx - 52, cy - 48), (cx - 58, cy - 42)],
        [(cx + 50, cy - 55), (cx + 55, cy - 48)],
    ]
    for b in thin_branches:
        d.line(b, fill=(35, 25, 15), width=2)
    # Outline tronc
    d.line([(cx - 12, cy + 42), (cx - 8, cy - 20)], fill=(30, 20, 10), width=2)
    d.line([(cx + 12, cy + 42), (cx + 8, cy - 20)], fill=(30, 20, 10), width=2)
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

    print("Generating ground atlas (9 tiles)...")
    grounds = [
        gen_ground_grass(), gen_ground_stone(), gen_ground_dirt(),
        gen_ground_gravel(), gen_ground_wood(), gen_ground_carpet(),
        gen_ground_water(), gen_ground_bathroom_tile(), gen_ground_worn_carpet(),
    ]
    make_atlas(grounds).save(os.path.join(OUTPUT, "ground-atlas.png"))
    print(f"  ground-atlas.png ({len(grounds)} tiles, {T}x{T} each)")

    print("Generating wall front atlas (9 variants)...")
    wall_fronts = [
        gen_wall_front_red_brick(), gen_wall_front_gray_stone(),
        gen_wall_front_wood(), gen_wall_front_gray_brick(),
        gen_wall_front_mossy(),
        gen_wall_front_dark_stone(), gen_wall_front_cracked_brick(),
        gen_wall_front_cobblestone(), gen_wall_front_vine_stone(),
    ]
    make_atlas(wall_fronts).save(os.path.join(OUTPUT, "wall-front-atlas.png"))
    print(f"  wall-front-atlas.png ({len(wall_fronts)} variants)")

    print("Generating wall top atlas (9 variants)...")
    top_colors = [
        (135, 115, 100), (110, 112, 120), (105, 82, 65), (100, 102, 108), (125, 108, 95),
        (55, 55, 62), (120, 100, 88), (82, 80, 75), (100, 108, 98),
    ]
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

    print("Generating decoration atlas (15 types)...")
    decos = [
        gen_deco(draw_bones), gen_deco(draw_skull), gen_deco(draw_crack),
        gen_deco(draw_web), gen_deco(draw_blood), gen_deco(draw_pebbles),
        gen_deco(draw_grass_tuft), gen_deco(draw_mushroom), gen_deco(draw_torch),
        gen_deco(draw_puddle),
        gen_deco(draw_fallen_books), gen_deco(draw_kitchen_utensils),
        gen_deco(draw_broken_toys), gen_deco(draw_broken_mirror),
        gen_deco(draw_water_puddle),
    ]
    make_atlas(decos).save(os.path.join(OUTPUT, "deco-atlas.png"))
    print(f"  deco-atlas.png ({len(decos)} types)")

    print("Generating furniture atlas (7 items)...")
    furniture = [
        gen_furniture_bed(),         # 0: 2x1 (256x128)
        gen_furniture_long_table(),  # 1: 2x1 (256x128)
        gen_furniture_bookshelf(),   # 2: 1x1 (128x128)
        gen_furniture_bathtub(),     # 3: 2x1 (256x128)
        gen_furniture_wardrobe(),    # 4: 1x1 (128x128)
        gen_furniture_fireplace(),   # 5: 1x1 (128x128)
        gen_furniture_cradle(),      # 6: 1x1 (128x128)
        gen_furniture_chandelier(),  # 7: 1x1 (128x128)
        gen_furniture_grand_door(),  # 8: 2x1 (256x128)
        gen_furniture_stairs_broken(), # 9: 2x1 (256x128)
    ]
    # Custom atlas: each item gets its own row, max width = 256
    max_w = max(f.size[0] for f in furniture)
    total_h = sum(f.size[1] for f in furniture)
    furn_atlas = Image.new('RGBA', (max_w, total_h), (0, 0, 0, 0))
    y_off = 0
    for f in furniture:
        furn_atlas.paste(f, (0, y_off), f)
        y_off += f.size[1]
    furn_atlas.save(os.path.join(OUTPUT, "furniture-atlas.png"))
    print(f"  furniture-atlas.png ({len(furniture)} items, {max_w}x{total_h})")

    # Also save individual furniture PNGs for easier sprite loading
    furn_names = ['bed', 'long_table', 'bookshelf', 'bathtub', 'wardrobe', 'fireplace', 'cradle', 'chandelier', 'grand_door', 'stairs_broken']
    for name, fimg in zip(furn_names, furniture):
        fimg.save(os.path.join(OUTPUT, f"furniture-{name}.png"))
        print(f"  furniture-{name}.png ({fimg.size[0]}x{fimg.size[1]})")

    print("Generating exterior stone atlas (5 variants)...")
    ext_stones = [
        gen_wall_exterior_stone_1(), gen_wall_exterior_stone_2(),
        gen_wall_exterior_stone_3(), gen_wall_exterior_stone_4(),
        gen_wall_exterior_stone_5(),
    ]
    make_atlas(ext_stones).save(os.path.join(OUTPUT, "wall-exterior-atlas.png"))
    ext_tops = [gen_wall_top((88, 86, 82), i+20) for i in range(5)]
    make_atlas(ext_tops).save(os.path.join(OUTPUT, "wall-exterior-top-atlas.png"))
    print(f"  wall-exterior-atlas.png + wall-exterior-top-atlas.png (5 variants)")

    print("Generating bush...")
    gen_bush().save(os.path.join(OUTPUT, "bush.png"))
    print("  bush.png")

    print("Generating trees...")
    gen_tree_pine().save(os.path.join(OUTPUT, "tree-pine.png"))
    gen_tree_oak().save(os.path.join(OUTPUT, "tree-oak.png"))
    gen_tree_spooky().save(os.path.join(OUTPUT, "tree-spooky.png"))
    gen_bush_thorny().save(os.path.join(OUTPUT, "bush-thorny.png"))
    gen_bush_fern().save(os.path.join(OUTPUT, "bush-fern.png"))
    gen_bush_dead().save(os.path.join(OUTPUT, "bush-dead.png"))
    print("  tree-pine/oak/spooky.png, bush-thorny/fern/dead.png")

    print("\nDone!")


if __name__ == "__main__":
    main()
