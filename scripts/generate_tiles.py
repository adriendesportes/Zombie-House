"""
Génère les tiles du manoir hanté — style Brawl Stars.
Grille carrée 32x32, vue 3/4 top-down.
Les murs ont une hauteur visible (face avant + dessus).
Les sols sont plats, vus de dessus.

Usage: python scripts/generate_tiles.py
"""

from PIL import Image, ImageDraw, ImageFilter
import random
import os

T = 32        # Tile size (square)
WALL_H = 18   # Hauteur visible de la face avant des murs
OUTPUT_DIR = "public/assets/tilesets/tiles"

random.seed(42)

# Palette Brawl Stars manoir hanté — couleurs douces, saturées
P = {
    # Sols
    'wood1': (155, 110, 68), 'wood1_hi': (175, 130, 82), 'wood1_lo': (125, 85, 50),
    'wood2': (115, 78, 45), 'wood2_hi': (138, 98, 60), 'wood2_lo': (90, 58, 32),
    'stone1': (120, 118, 125), 'stone1_hi': (140, 138, 145), 'stone1_lo': (95, 93, 102),
    'stone2': (82, 80, 92), 'stone2_hi': (100, 98, 110), 'stone2_lo': (62, 60, 72),
    'carpet': (145, 32, 32), 'carpet_hi': (168, 48, 42), 'carpet_lo': (112, 22, 22),
    'carpet_bord': (175, 60, 45),
    # Murs
    'wall_top': (115, 98, 88),       # face dessus (éclairée)
    'wall_top_hi': (135, 118, 105),
    'wall_front': (72, 52, 42),      # face avant (sombre)
    'brick': (142, 78, 52),
    'brick_hi': (165, 95, 68),
    'brick_lo': (112, 60, 38),
    'mortar': (65, 52, 48),
    # Porte
    'door': (135, 88, 48), 'door_hi': (158, 108, 62), 'door_lo': (98, 62, 32),
    'handle': (205, 185, 72),
    'glow': (55, 175, 115),
    # Meubles
    'wood': (138, 92, 52), 'wood_hi': (162, 112, 68), 'wood_lo': (105, 68, 38),
    'wood_dk': (70, 45, 25),
    # FX
    'candle': (255, 215, 95), 'candle_hi': (255, 248, 195),
    'outline': (35, 25, 18),
    'shadow': (0, 0, 0),
    'web': (195, 195, 208),
}


def nc(base, v=8):
    return tuple(max(0, min(255, c + random.randint(-v, v))) for c in base)


# ==================== SOLS (32x32, plats, vus de dessus) ====================

def gen_floor_wood(base, hi, lo):
    img = Image.new('RGBA', (T, T), base)
    d = ImageDraw.Draw(img)
    # Planches horizontales
    for py in range(0, T, 8):
        off = (py // 8 % 2) * 12
        for px in range(-12 + off, T, 20):
            c = nc(base, 5)
            d.rectangle([px, py, px+18, py+6], fill=c)
            d.line([(px, py+7), (px+18, py+7)], fill=lo)
            d.line([(px+1, py), (px+18, py)], fill=hi)
            # Grain
            for g in range(py+2, py+6, 2):
                d.line([(px+2, g), (px+16, g)], fill=nc(lo, 4))
    # Petits détails
    for _ in range(2):
        x, y = random.randint(2, T-3), random.randint(2, T-3)
        d.point((x, y), fill=nc(lo, 3))
    return img


def gen_floor_stone(base, hi, lo):
    img = Image.new('RGBA', (T, T), base)
    d = ImageDraw.Draw(img)
    stones = [(0,0,16,10),(17,0,15,11),(0,11,11,10),(12,12,10,9),(23,12,9,9),(0,22,15,10),(16,22,16,10)]
    for sx, sy, sw, sh in stones:
        c = nc(base, 6)
        d.rectangle([sx+1, sy+1, sx+sw-2, sy+sh-2], fill=c)
        d.rectangle([sx, sy, sx+sw-1, sy+sh-1], outline=lo)
        d.line([(sx+1, sy+1), (sx+sw-2, sy+1)], fill=hi)
        d.line([(sx+1, sy+1), (sx+1, sy+sh-2)], fill=nc(hi, 3))
    return img


def gen_floor_parquet_light(): return gen_floor_wood(P['wood1'], P['wood1_hi'], P['wood1_lo'])
def gen_floor_parquet_dark(): return gen_floor_wood(P['wood2'], P['wood2_hi'], P['wood2_lo'])
def gen_floor_stone_light(): return gen_floor_stone(P['stone1'], P['stone1_hi'], P['stone1_lo'])
def gen_floor_stone_dark(): return gen_floor_stone(P['stone2'], P['stone2_hi'], P['stone2_lo'])

def gen_floor_cracked():
    img = gen_floor_stone(P['stone1'], P['stone1_hi'], P['stone1_lo'])
    d = ImageDraw.Draw(img)
    d.line([(8,3),(12,10),(10,18),(14,28)], fill=(55,55,62), width=1)
    d.line([(22,5),(19,14),(22,22)], fill=(55,55,62), width=1)
    return img

def gen_floor_carpet():
    img = Image.new('RGBA', (T, T), P['carpet'])
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,T-1,T-1], outline=P['carpet_bord'], width=2)
    d.rectangle([3,3,T-4,T-4], outline=P['carpet_lo'])
    for y in range(5,T-5,5):
        for x in range(5,T-5,5):
            if (x+y)%10<5: d.rectangle([x,y,x+2,y+2], fill=P['carpet_hi'])
    return img


# ==================== MURS (32x(32+WALL_H)) ====================
# Les murs font 32px de large mais (32+WALL_H) de haut.
# La partie basse (WALL_H px) = face avant visible.
# La partie haute (32 px) = face du dessus.
# En jeu, le mur est placé de façon à ce que la face dessus couvre la tile,
# et la face avant dépasse vers le bas (sur la tile en dessous visuellement).

def draw_bricks(d, x, y, w, h):
    rh = 5
    for by in range(y, y+h, rh):
        row = (by - y) // rh
        off = (row % 2) * 8
        for bx in range(x - 8 + off, x + w + 8, 15):
            bx1 = max(x, bx)
            bx2 = min(x + w - 1, bx + 13)
            by2 = min(y + h - 1, by + rh - 2)
            if bx2 <= bx1: continue
            c = nc(P['brick'], 6)
            d.rectangle([bx1, by, bx2, by2], fill=c)
            d.line([(bx1, by), (bx2, by)], fill=P['brick_hi'])
            d.line([(bx1, by2), (bx2, by2)], fill=P['brick_lo'])
        if by + rh - 1 < y + h:
            d.line([(x, by+rh-1), (x+w-1, by+rh-1)], fill=P['mortar'])


def gen_wall():
    """Mur complet: face dessus (32x32) + face avant (32xWALL_H)."""
    img = Image.new('RGBA', (T, T + WALL_H), (0,0,0,0))
    d = ImageDraw.Draw(img)

    # Face du dessus (partie haute de l'image)
    d.rectangle([0, 0, T-1, T-1], fill=P['wall_top'])
    # Texture subtile
    for x in range(2, T-2, 5):
        for y in range(2, T-2, 5):
            d.point((x + random.randint(-1,1), y + random.randint(-1,1)), fill=nc(P['wall_top_hi'], 4))
    d.rectangle([0, 0, T-1, T-1], outline=P['outline'])

    # Face avant (partie basse = la hauteur visible)
    front_y = T
    draw_bricks(d, 0, front_y, T, WALL_H)
    # Ombre dégradée en bas de la face
    for i in range(4):
        alpha = 60 - i * 15
        d.line([(0, front_y + WALL_H - 1 - i), (T-1, front_y + WALL_H - 1 - i)],
               fill=(0, 0, 0, max(0, alpha)))
    d.rectangle([0, front_y, T-1, front_y + WALL_H - 1], outline=P['outline'])

    return img


def gen_wall_half():
    """Demi-mur (moins haut)."""
    h = WALL_H // 2
    img = Image.new('RGBA', (T, T + h), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, T-1, T-1], fill=P['wall_top'])
    d.rectangle([0, 0, T-1, T-1], outline=P['outline'])
    draw_bricks(d, 0, T, T, h)
    d.rectangle([0, T, T-1, T + h - 1], outline=P['outline'])
    return img


def gen_door_closed():
    img = Image.new('RGBA', (T, T + WALL_H), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # Dessus
    d.rectangle([0, 0, T-1, T-1], fill=P['wall_top'])
    d.rectangle([0, 0, T-1, T-1], outline=P['outline'])
    # Face avant = porte
    fy = T
    d.rectangle([0, fy, T-1, fy+WALL_H-1], fill=P['door'])
    # Planches
    for dy in range(fy+3, fy+WALL_H-2, 4):
        d.line([(2, dy), (T-3, dy)], fill=P['door_lo'])
    # Highlight haut
    d.rectangle([2, fy+1, T-3, fy+2], fill=P['door_hi'])
    # Arche
    d.arc([4, fy-2, T-5, fy+8], 180, 0, fill=P['door_lo'], width=2)
    # Poignée
    d.ellipse([T//2+4, fy+WALL_H//2-2, T//2+8, fy+WALL_H//2+2], fill=P['handle'], outline=P['outline'])
    d.rectangle([0, fy, T-1, fy+WALL_H-1], outline=P['outline'])
    return img


def gen_door_open():
    img = Image.new('RGBA', (T, T + WALL_H), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, T-1, T-1], fill=P['wall_top'])
    d.rectangle([0, 0, T-1, T-1], outline=P['outline'])
    fy = T
    # Ouverture sombre
    d.rectangle([0, fy, T-1, fy+WALL_H-1], fill=(15, 12, 10))
    # Lueur verte
    for i in range(5):
        r = 7 - i
        a = 25 + i * 12
        cx, cy = T//2, fy + WALL_H//2
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(45, 130+a//2, 75+a//3, a))
    d.rectangle([0, fy, T-1, fy+WALL_H-1], outline=P['outline'])
    return img


# ==================== SHADOW ====================

def gen_shadow():
    """Ombre projetée par un mur sur la tile en dessous."""
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    for y in range(min(10, T)):
        alpha = int(70 * (1 - y / 10))
        d.line([(0, y), (T-1, y)], fill=(0, 0, 0, max(0, alpha)))
    return img


# ==================== MEUBLES ====================

def gen_table():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # Ombre
    d.ellipse([4, 20, T-4, T-2], fill=(0,0,0,35))
    # Pieds
    for lx, ly in [(6,17),(T-9,17),(6,T-6),(T-9,T-6)]:
        d.rectangle([lx, ly, lx+2, ly+5], fill=P['wood_lo'])
    # Plateau
    d.rectangle([3, 10, T-4, 19], fill=P['wood'])
    d.rectangle([3, 10, T-4, 12], fill=P['wood_hi'])  # highlight
    d.rectangle([3, 19, T-4, 21], fill=P['wood_lo'])   # face avant
    d.rectangle([3, 10, T-4, 21], outline=P['outline'])
    # Grain
    for g in range(13, 18, 2):
        d.line([(5, g), (T-6, g)], fill=P['wood_lo'])
    return img


def gen_bookshelf():
    img = Image.new('RGBA', (T, T + 8), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # Corps
    h = T + 4
    d.rectangle([2, 0, T-3, h-1], fill=P['wood_lo'])
    d.rectangle([2, 0, T-3, 2], fill=P['wood_hi'])  # dessus
    d.rectangle([2, 0, T-3, h-1], outline=P['outline'])
    # Étagères + livres
    for sy in [3, 12, 21]:
        d.rectangle([3, sy, T-4, sy+7], fill=(32, 24, 16))
        d.line([(3, sy+8), (T-4, sy+8)], fill=P['wood'])
        bx = 4
        while bx < T-5:
            bw = random.randint(2, 4)
            bh = random.randint(4, 6)
            cols = [(140,38,38),(38,75,140),(55,115,55),(140,115,38),(95,38,115),(38,95,95)]
            d.rectangle([bx, sy+8-bh, bx+bw, sy+7], fill=nc(random.choice(cols), 10))
            bx += bw + 1
    return img


def gen_candelabra():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # Halo
    for r in range(14, 4, -1):
        a = max(0, 30 - r * 2)
        d.ellipse([T//2-r, T//2-r, T//2+r, T//2+r], fill=(255, 175, 55, a))
    # Base
    d.ellipse([T//2-5, T-8, T//2+5, T-3], fill=(58, 50, 44), outline=P['outline'])
    # Tige
    d.rectangle([T//2-1, 10, T//2+1, T-5], fill=(68, 60, 52))
    # Bras + flammes
    for ax, ay in [(T//2-10, 12), (T//2+10, 12), (T//2-5, 9), (T//2+5, 9)]:
        d.line([(T//2, 14), (ax, ay)], fill=(68, 60, 52))
        d.rectangle([ax-1, ay-4, ax+1, ay], fill=(218, 208, 188))
        d.polygon([(ax, ay-7), (ax-2, ay-3), (ax+2, ay-3)], fill=P['candle'])
        d.point((ax, ay-6), fill=P['candle_hi'])
    return img


def gen_chair():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse([7, 22, T-7, T-2], fill=(0,0,0,30))
    for lx, ly in [(8, 18), (T-11, 18), (8, T-6), (T-11, T-6)]:
        d.rectangle([lx, ly, lx+2, ly+4], fill=P['wood_lo'])
    d.rectangle([6, 14, T-7, 20], fill=P['wood'])
    d.rectangle([6, 14, T-7, 20], outline=P['outline'])
    d.polygon([(7, 14), (9, 3), (12, 4), (10, 14)], fill=P['wood_lo'], outline=P['outline'])
    d.polygon([(T-12, 14), (T-9, 5), (T-6, 7), (T-8, 14)], fill=P['wood_dk'], outline=P['outline'])
    return img


def gen_cobweb():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    wc = P['web'] + (130,)
    strands = [(T-1,8),(T-5,16),(T//2,T//2+4),(8,T-1),(T-4,T-1),(T-1,T//2)]
    for sx, sy in strands:
        d.line([(0,0),(sx,sy)], fill=wc)
    for r in range(5, T-4, 5):
        pts = []
        for sx, sy in strands:
            dist = max(1, (sx*sx+sy*sy)**0.5)
            pts.append((int(sx*r/dist), int(sy*r/dist)))
        for i in range(len(pts)-1):
            d.line([pts[i], pts[i+1]], fill=P['web']+(70,))
    return img


def gen_barrel():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse([6, T-8, T-6, T-2], fill=(0,0,0,30))
    d.rounded_rectangle([7, 5, T-7, T-5], radius=3, fill=P['wood'])
    d.rounded_rectangle([7, 5, T-7, T-5], radius=3, outline=P['outline'])
    for px in range(10, T-8, 4):
        d.line([(px, 6), (px, T-6)], fill=P['wood_lo'])
    for by in [9, 16, 23]:
        d.rectangle([6, by, T-6, by+1], fill=(102, 102, 112))
    d.ellipse([8, 3, T-8, 9], fill=P['wood_lo'], outline=P['outline'])
    d.ellipse([10, 4, T-10, 8], fill=P['wood_dk'])
    return img


# ==================== ASSEMBLAGE ====================

GENERATORS = [
    ("floor-parquet-light", gen_floor_parquet_light),
    ("floor-parquet-dark", gen_floor_parquet_dark),
    ("floor-stone-light", gen_floor_stone_light),
    ("floor-stone-dark", gen_floor_stone_dark),
    ("floor-cracked", gen_floor_cracked),
    ("floor-carpet", gen_floor_carpet),
    ("wall", gen_wall),
    ("wall-half", gen_wall_half),
    ("door-closed", gen_door_closed),
    ("door-open", gen_door_open),
    ("shadow", gen_shadow),
    ("table", gen_table),
    ("bookshelf", gen_bookshelf),
    ("candelabra", gen_candelabra),
    ("chair", gen_chair),
    ("cobweb", gen_cobweb),
    ("barrel", gen_barrel),
]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for i, (name, gen) in enumerate(GENERATORS):
        tile = gen()
        tile.save(os.path.join(OUTPUT_DIR, f"{name}.png"))
        print(f"  [{i+1:2d}/{len(GENERATORS)}] {name} ({tile.size[0]}x{tile.size[1]})")
    print("Terminé !")


if __name__ == "__main__":
    main()
