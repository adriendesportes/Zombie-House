"""
Génère les tiles du manoir hanté en pixel art procédural 32x32.
Style: dark cartoon, 3/4 top-down.

Usage: python scripts/generate_tiles.py
"""

from PIL import Image, ImageDraw
import random
import os

T = 32  # Tile size
OUTPUT_DIR = "public/assets/tilesets/tiles"
OUTPUT_GRID = "public/assets/tilesets/manor-tileset.png"

random.seed(42)

# Palette
P = {
    'wl': (168, 120, 72), 'wm': (140, 95, 55), 'wd': (100, 68, 38),
    'wdd': (72, 48, 28), 'wln': (55, 38, 20),
    'sl': (130, 130, 138), 'sm': (100, 100, 110), 'sd': (72, 72, 82),
    'sdd': (55, 55, 65), 'sln': (40, 40, 50),
    'bl': (155, 85, 60), 'bm': (130, 70, 48), 'bd': (105, 55, 38),
    'bdd': (80, 42, 28), 'mort': (75, 65, 60),
    'cr': (140, 30, 30), 'crd': (100, 20, 20), 'crb': (170, 50, 35),
    'dw': (130, 80, 45), 'dd': (90, 55, 30), 'df': (70, 45, 25),
    'dh': (180, 160, 60), 'gg': (40, 180, 120),
    'cf': (255, 200, 80), 'cg': (255, 160, 40),
    'ol': (30, 22, 18), 'sh': (20, 15, 12),
    'web': (200, 200, 210),
}


def nc(base, v=10):
    return tuple(max(0, min(255, c + random.randint(-v, v))) for c in base)


def bricks(draw, x, y, w, h, rh=5):
    for by in range(y, y + h, rh):
        row = (by - y) // rh
        off = (row % 2) * 8
        for bx in range(x - 8 + off, x + w + 8, 16):
            bx1 = max(x, bx)
            bx2 = min(x + w - 1, bx + 14)
            by2 = min(y + h - 1, by + rh - 2)
            if bx2 <= bx1: continue
            draw.rectangle([bx1, by, bx2, by2], fill=nc(P['bm'], 10))
            draw.line([(bx1, by), (bx2, by)], fill=nc(P['bl'], 6))
            draw.line([(bx1, by2), (bx2, by2)], fill=P['bd'])
        draw.line([(x, by + rh - 1), (x + w - 1, by + rh - 1)], fill=P['mort'])


def gen_floor_parquet_light():
    img = Image.new('RGBA', (T, T), P['wm'])
    d = ImageDraw.Draw(img)
    for py in range(0, T, 8):
        off = (py // 8 % 2) * 10
        for px in range(-10 + off, T, 16):
            d.rectangle([px, py, px+14, py+6], fill=nc(P['wl']))
            d.line([(px, py+7), (px+14, py+7)], fill=P['wln'])
            for gy in range(py+2, py+6, 2):
                d.line([(px+1, gy), (px+13, gy)], fill=nc(P['wm'], 6))
    return img


def gen_floor_parquet_dark():
    img = Image.new('RGBA', (T, T), P['wdd'])
    d = ImageDraw.Draw(img)
    for py in range(0, T, 8):
        off = (py // 8 % 2) * 10
        for px in range(-10 + off, T, 16):
            d.rectangle([px, py, px+14, py+6], fill=nc(P['wd']))
            d.line([(px, py+7), (px+14, py+7)], fill=P['wln'])
            for gy in range(py+2, py+6, 2):
                d.line([(px+1, gy), (px+13, gy)], fill=nc(P['wdd'], 6))
    return img


def gen_floor_stone_light():
    img = Image.new('RGBA', (T, T), P['sm'])
    d = ImageDraw.Draw(img)
    stones = [(0,0,15,10),(16,0,16,11),(0,11,10,10),(11,12,10,9),(22,12,10,9),(0,22,14,10),(15,22,17,10)]
    for sx, sy, sw, sh in stones:
        d.rectangle([sx+1,sy+1,sx+sw-2,sy+sh-2], fill=nc(P['sl'],8))
        d.rectangle([sx,sy,sx+sw-1,sy+sh-1], outline=P['sln'])
        d.line([(sx+1,sy+1),(sx+sw-2,sy+1)], fill=nc((145,145,152),6))
    return img


def gen_floor_stone_dark():
    img = Image.new('RGBA', (T, T), P['sdd'])
    d = ImageDraw.Draw(img)
    stones = [(0,0,15,10),(16,0,16,11),(0,11,10,10),(11,12,10,9),(22,12,10,9),(0,22,14,10),(15,22,17,10)]
    for sx, sy, sw, sh in stones:
        d.rectangle([sx+1,sy+1,sx+sw-2,sy+sh-2], fill=nc(P['sd'],6))
        d.rectangle([sx,sy,sx+sw-1,sy+sh-1], outline=P['sln'])
    return img


def gen_floor_cracked():
    img = gen_floor_stone_light()
    d = ImageDraw.Draw(img)
    d.line([(5,2),(8,8),(10,15),(9,22),(12,30)], fill=(40,40,48))
    d.line([(22,5),(20,12),(21,20),(25,28)], fill=(40,40,48))
    return img


def gen_floor_carpet():
    img = Image.new('RGBA', (T, T), P['cr'])
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,31,31], outline=P['crb'], width=2)
    d.rectangle([3,3,28,28], outline=P['crd'])
    for y in range(5,27,4):
        for x in range(5,27,4):
            if (x+y)%8==2: d.point((x,y), fill=nc(P['crd'],5))
    return img


def gen_wall_top():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,31,8], fill=P['sd'])
    d.line([(0,0),(31,0)], fill=P['ol'], width=2)
    bricks(d, 0, 10, 32, 22)
    d.line([(0,9),(31,9)], fill=P['ol'])
    d.line([(0,31),(31,31)], fill=P['ol'], width=2)
    d.line([(0,0),(0,31)], fill=P['ol'])
    d.line([(31,0),(31,31)], fill=P['ol'])
    return img


def gen_wall_bottom():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    bricks(d, 0, 0, 32, 26)
    d.rectangle([0,26,31,31], fill=P['sd'])
    d.line([(0,26),(31,26)], fill=P['ol'])
    d.line([(0,0),(31,0)], fill=P['ol'], width=2)
    d.line([(0,31),(31,31)], fill=P['ol'], width=2)
    d.line([(0,0),(0,31)], fill=P['ol'])
    d.line([(31,0),(31,31)], fill=P['ol'])
    return img


def gen_wall_left():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,8,31], fill=P['sd'])
    bricks(d, 10, 0, 22, 32)
    d.line([(9,0),(9,31)], fill=P['ol'])
    d.line([(0,0),(0,31)], fill=P['ol'], width=2)
    d.line([(31,0),(31,31)], fill=P['ol'])
    d.line([(0,0),(31,0)], fill=P['ol'])
    d.line([(0,31),(31,31)], fill=P['ol'])
    return img


def gen_wall_right():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    bricks(d, 0, 0, 22, 32)
    d.rectangle([23,0,31,31], fill=P['sd'])
    d.line([(22,0),(22,31)], fill=P['ol'])
    d.line([(31,0),(31,31)], fill=P['ol'], width=2)
    d.line([(0,0),(0,31)], fill=P['ol'])
    d.line([(0,0),(31,0)], fill=P['ol'])
    d.line([(0,31),(31,31)], fill=P['ol'])
    return img


def gen_corner(top, left):
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    bricks(d, 0, 0, 32, 32)
    if top:
        d.rectangle([0,0,31,8], fill=P['sd'])
        d.line([(0,0),(31,0)], fill=P['ol'], width=2)
        d.line([(0,9),(31,9)], fill=P['ol'])
    else:
        d.rectangle([0,23,31,31], fill=P['sd'])
        d.line([(0,31),(31,31)], fill=P['ol'], width=2)
        d.line([(0,22),(31,22)], fill=P['ol'])
    if left:
        vy1 = 10 if top else 0
        vy2 = 31 if not top else 22
        d.rectangle([0,vy1,8,vy2], fill=P['sd'])
        d.line([(0,0),(0,31)], fill=P['ol'], width=2)
        d.line([(9,vy1),(9,vy2)], fill=P['ol'])
    else:
        vy1 = 10 if top else 0
        vy2 = 31 if not top else 22
        d.rectangle([23,vy1,31,vy2], fill=P['sd'])
        d.line([(31,0),(31,31)], fill=P['ol'], width=2)
        d.line([(22,vy1),(22,vy2)], fill=P['ol'])
    d.rectangle([0,0,31,31], outline=P['ol'])
    return img


def gen_door_closed():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,31,31], fill=P['bdd'])
    bricks(d, 0, 0, 8, 32)
    bricks(d, 24, 0, 8, 32)
    d.rectangle([8,2,23,31], fill=P['dw'])
    for dy in range(5, 29, 7):
        d.line([(9,dy),(22,dy)], fill=P['dd'])
    d.ellipse([18,14,21,18], fill=P['dh'])
    d.rectangle([8,2,23,31], outline=P['ol'])
    d.rectangle([0,0,31,31], outline=P['ol'])
    return img


def gen_door_open():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    bricks(d, 0, 0, 8, 32)
    bricks(d, 24, 0, 8, 32)
    d.rectangle([8,0,23,31], fill=(15,12,10))
    for gy in range(8,24,3):
        gx = 12 + random.randint(-1,1)
        d.ellipse([gx,gy,gx+7,gy+4], fill=nc(P['gg'],20))
    d.polygon([(21,2),(23,2),(23,29),(19,28)], fill=P['dd'])
    d.line([(21,2),(21,28)], fill=P['ol'])
    d.line([(7,0),(7,31)], fill=P['ol'], width=2)
    d.line([(24,0),(24,31)], fill=P['ol'], width=2)
    d.rectangle([0,0,31,31], outline=P['ol'])
    return img


def gen_table():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse([5,20,27,30], fill=(20,15,12,80))
    for lx,ly in [(7,18),(22,18),(7,26),(22,26)]:
        d.rectangle([lx,ly,lx+2,ly+5], fill=P['wd'])
    d.rectangle([4,10,27,20], fill=P['wm'])
    d.rectangle([4,10,27,20], outline=P['ol'])
    d.rectangle([5,11,26,14], fill=P['wl'])
    for gy in range(13,19,2):
        d.line([(6,gy),(25,gy)], fill=P['wd'])
    return img


def gen_bookshelf():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([3,2,28,30], fill=P['wd'])
    d.rectangle([3,2,28,30], outline=P['ol'])
    for sy in [2,11,20]:
        d.rectangle([4,sy+1,27,sy+7], fill=(35,25,18))
        d.line([(4,sy+8),(27,sy+8)], fill=P['wm'])
        bx = 5
        while bx < 26:
            bw = random.randint(2,4)
            bh = random.randint(5,7)
            cols = [(140,40,40),(40,80,140),(60,120,60),(140,120,40),(100,40,120)]
            d.rectangle([bx,sy+8-bh,bx+bw,sy+7], fill=nc(random.choice(cols),12))
            bx += bw + 1
    return img


def gen_candelabra():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    for r in range(14,4,-2):
        a = max(0,30-r)
        d.ellipse([16-r,16-r,16+r,16+r], fill=(255,180,60,a))
    d.ellipse([11,26,21,30], fill=(60,55,50))
    d.rectangle([15,9,17,27], fill=(70,65,58))
    for ax,ay in [(9,12),(22,12),(12,10),(20,10)]:
        d.line([(16,14),(ax,ay)], fill=(70,65,58))
        d.rectangle([ax-1,ay-5,ax+1,ay], fill=(220,210,190))
        d.polygon([(ax,ay-7),(ax-2,ay-4),(ax+2,ay-4)], fill=P['cf'])
    return img


def gen_chair():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse([8,22,24,30], fill=(20,15,12,60))
    for lx,ly in [(9,20),(19,20),(9,26),(19,26)]:
        d.rectangle([lx,ly,lx+2,ly+4], fill=P['wd'])
    d.rectangle([7,17,21,22], fill=P['wm'])
    d.rectangle([7,17,21,22], outline=P['ol'])
    d.polygon([(8,17),(10,4),(13,5),(11,17)], fill=P['wd'], outline=P['ol'])
    d.polygon([(15,17),(18,6),(20,8),(17,17)], fill=P['wdd'], outline=P['ol'])
    return img


def gen_cobweb():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    wc = (200,200,210,140)
    strands = [(31,10),(25,20),(15,25),(10,31),(22,31),(31,22)]
    for sx,sy in strands:
        d.line([(0,0),(sx,sy)], fill=wc)
    for r in range(6,28,6):
        pts = []
        for sx,sy in strands:
            dist = (sx*sx+sy*sy)**0.5
            if dist > 0:
                pts.append((int(sx*r/dist), int(sy*r/dist)))
        for i in range(len(pts)-1):
            d.line([pts[i],pts[i+1]], fill=(200,200,210,80))
    return img


def gen_barrel():
    img = Image.new('RGBA', (T, T), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse([6,24,26,31], fill=(20,15,12,70))
    d.rounded_rectangle([7,6,25,28], radius=3, fill=P['wm'])
    d.rounded_rectangle([7,6,25,28], radius=3, outline=P['ol'])
    for px in range(9,24,4):
        d.line([(px,7),(px,27)], fill=P['wd'])
    for by in [10,17,24]:
        d.rectangle([6,by,26,by+1], fill=(100,100,110))
    d.ellipse([8,4,24,10], fill=P['wd'])
    d.ellipse([8,4,24,10], outline=P['ol'])
    d.ellipse([10,5,22,9], fill=P['wdd'])
    return img


GENERATORS = [
    ("floor-parquet-light", gen_floor_parquet_light),
    ("floor-parquet-dark", gen_floor_parquet_dark),
    ("floor-stone-light", gen_floor_stone_light),
    ("floor-stone-dark", gen_floor_stone_dark),
    ("floor-cracked-tiles", gen_floor_cracked),
    ("floor-carpet-red", gen_floor_carpet),
    ("wall-top", gen_wall_top),
    ("wall-bottom", gen_wall_bottom),
    ("wall-left", gen_wall_left),
    ("wall-right", gen_wall_right),
    ("wall-corner-tl", lambda: gen_corner(True, True)),
    ("wall-corner-tr", lambda: gen_corner(True, False)),
    ("wall-corner-bl", lambda: gen_corner(False, True)),
    ("wall-corner-br", lambda: gen_corner(False, False)),
    ("door-closed-front", gen_door_closed),
    ("door-open-front", gen_door_open),
    ("door-closed-side", gen_door_closed),
    ("door-open-side", gen_door_open),
    ("furniture-table", gen_table),
    ("furniture-bookshelf", gen_bookshelf),
    ("decor-candelabra", gen_candelabra),
    ("furniture-chair", gen_chair),
    ("decor-cobweb", gen_cobweb),
    ("furniture-barrel", gen_barrel),
]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_GRID), exist_ok=True)
    grid = Image.new('RGBA', (6*T, 4*T), (0,0,0,0))
    for i, (name, gen) in enumerate(GENERATORS):
        tile = gen()
        tile.save(os.path.join(OUTPUT_DIR, f"{name}.png"))
        grid.paste(tile, ((i%6)*T, (i//6)*T), tile)
        print(f"  [{i+1:2d}/24] {name}")
    grid.save(OUTPUT_GRID)
    print(f"\nGrille: {OUTPUT_GRID} ({grid.size[0]}x{grid.size[1]})")


if __name__ == "__main__":
    main()
