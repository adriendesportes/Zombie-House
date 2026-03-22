"""
Découpe le tileset v2 : détecte les 4 lignes de sprites,
puis divise chaque ligne en 6 colonnes égales.

Usage: python scripts/slice_tileset_v2.py
"""

from PIL import Image
import numpy as np
from scipy import ndimage
import os

INPUT = "Design/Tilesets/manor-tileset-v2-raw.png"
OUTPUT_DIR = "public/assets/tilesets/tiles"
OUTPUT_GRID = "public/assets/tilesets/manor-tileset.png"

TILE_SIZE = 64
GRID_COLS = 6
GRID_ROWS = 4

TILE_NAMES = [
    "floor-parquet-light", "floor-parquet-dark", "floor-stone-light",
    "floor-stone-dark", "floor-cracked-tiles", "floor-carpet-red",
    "wall-top", "wall-bottom", "wall-left",
    "wall-right", "wall-corner-tl", "wall-corner-tr",
    "wall-corner-bl", "wall-corner-br", "door-closed-front",
    "door-open-front", "door-closed-side", "door-open-side",
    "furniture-table", "furniture-table-2", "furniture-bookshelf",
    "decor-candelabra", "furniture-chair", "decor-cobweb",
]


def find_row_boundaries(mask):
    """Trouve les limites Y de chaque ligne en projetant horizontalement."""
    row_sums = mask.sum(axis=1)
    threshold = mask.shape[1] * 0.02  # 2% de la largeur

    in_row = False
    rows = []
    start = 0
    for y in range(len(row_sums)):
        if row_sums[y] > threshold and not in_row:
            start = y
            in_row = True
        elif row_sums[y] <= threshold and in_row:
            rows.append((start, y))
            in_row = False
    if in_row:
        rows.append((start, len(row_sums)))

    # Split rows that are too tall (likely 2 rows merged)
    avg_h = sum(y2 - y1 for y1, y2 in rows) / len(rows) if rows else 200
    final = []
    for y1, y2 in rows:
        h = y2 - y1
        if h > avg_h * 1.5:
            # Find the best split point (row with least content)
            mid_zone = row_sums[y1:y2]
            search_start = len(mid_zone) // 3
            search_end = len(mid_zone) * 2 // 3
            best = search_start + mid_zone[search_start:search_end].argmin()
            split_y = y1 + best
            final.append((y1, split_y))
            final.append((split_y, y2))
        else:
            final.append((y1, y2))

    return final


def find_content_bounds(mask):
    """Trouve les limites X du contenu global."""
    col_sums = mask.sum(axis=0)
    threshold = mask.shape[0] * 0.01

    x_start = 0
    for x in range(len(col_sums)):
        if col_sums[x] > threshold:
            x_start = x
            break

    x_end = len(col_sums)
    for x in range(len(col_sums) - 1, -1, -1):
        if col_sums[x] > threshold:
            x_end = x + 1
            break

    return x_start, x_end


def main():
    img = Image.open(INPUT).convert("RGBA")
    arr = np.array(img)
    print(f"Image: {img.size[0]}x{img.size[1]}")

    # Supprimer le fond blanc
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    is_white = (r > 240) & (g > 240) & (b > 240)
    arr[is_white, 3] = 0
    clean_img = Image.fromarray(arr)

    mask = arr[:, :, 3] > 0

    # Trouver les limites des lignes
    row_bounds = find_row_boundaries(mask)
    print(f"Lignes détectées: {len(row_bounds)}")
    for i, (y1, y2) in enumerate(row_bounds):
        print(f"  Ligne {i+1}: y={y1}→{y2} (h={y2-y1})")

    # Trouver les limites X du contenu
    x_start, x_end = find_content_bounds(mask)
    content_w = x_end - x_start
    col_w = content_w / GRID_COLS
    print(f"Contenu X: {x_start}→{x_end} (w={content_w}), col_w={col_w:.0f}")

    # Découper
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_GRID), exist_ok=True)

    grid = Image.new("RGBA", (GRID_COLS * TILE_SIZE, GRID_ROWS * TILE_SIZE), (0, 0, 0, 0))

    idx = 0
    for row_i, (y1, y2) in enumerate(row_bounds[:GRID_ROWS]):
        for col_i in range(GRID_COLS):
            if idx >= len(TILE_NAMES):
                break
            name = TILE_NAMES[idx]

            cx1 = int(x_start + col_i * col_w)
            cx2 = int(x_start + (col_i + 1) * col_w)

            crop = clean_img.crop((cx1, y1, cx2, y2))
            crop = crop.resize((TILE_SIZE, TILE_SIZE), Image.LANCZOS)

            tile_path = os.path.join(OUTPUT_DIR, f"{name}.png")
            crop.save(tile_path)
            print(f"  [{idx+1:2d}/24] {name} ({cx2-cx1}x{y2-y1} → {TILE_SIZE}x{TILE_SIZE})")

            grid.paste(crop, (col_i * TILE_SIZE, row_i * TILE_SIZE))
            idx += 1

    grid.save(OUTPUT_GRID)
    print(f"\nGrille: {OUTPUT_GRID}")
    print("Terminé !")


if __name__ == "__main__":
    main()
