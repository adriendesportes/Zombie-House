"""
Découpe automatique du tileset raw en tiles individuels 64x64 px.
1. Supprime le fond damier gris (le rend transparent)
2. Détecte les sprites par composantes connexes
3. Découpe, redimensionne en 64x64, assemble une grille

Usage: python scripts/slice_tileset.py
"""

from PIL import Image
import numpy as np
from scipy import ndimage
import os

INPUT = "Design/Tilesets/manor-tileset-raw.png"
OUTPUT_DIR = "public/assets/tilesets/tiles"
OUTPUT_GRID = "public/assets/tilesets/manor-tileset.png"
OUTPUT_CLEAN = "Design/Tilesets/manor-tileset-clean.png"

TILE_SIZE = 64
GRID_COLS = 6
GRID_ROWS = 4

TILE_NAMES = [
    # Row 1 — Sols
    "floor-parquet-light", "floor-parquet-dark", "floor-stone-light",
    "floor-stone-dark", "floor-cracked-tiles", "floor-carpet-red",
    # Row 2 — Murs
    "wall-north", "wall-south", "wall-east",
    "wall-west", "wall-corner-ne", "wall-corner-nw",
    # Row 3 — Coins + Portes
    "wall-corner-se", "wall-corner-sw", "door-closed-ns",
    "door-open-ns", "door-closed-ew", "door-open-ew",
    # Row 4 — Meubles / Décors
    "furniture-table", "furniture-bookshelf", "decor-candelabra",
    "furniture-chair", "decor-cobweb", "furniture-barrel",
]


def remove_checkerboard_bg(arr):
    """
    Le fond damier est composé de gris neutres (R≈G≈B, range 70-130).
    On détecte ces pixels et les rend transparents.
    """
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    # Écart max entre canaux RGB (faible = gris neutre)
    rgb_stack = np.stack([r, g, b], axis=-1).astype(np.int16)
    max_diff = rgb_stack.max(axis=-1) - rgb_stack.min(axis=-1)

    # Luminosité moyenne
    lum = rgb_stack.mean(axis=-1)

    # Le fond damier : gris neutre (diff < 8) dans la plage 65-130
    is_bg = (max_diff < 10) & (lum > 60) & (lum < 135)

    # Érosion pour ne pas manger les bords des sprites
    is_bg = ndimage.binary_erosion(is_bg, iterations=1)
    # Puis dilatation pour bien couvrir
    is_bg = ndimage.binary_dilation(is_bg, iterations=2)

    new_arr = arr.copy()
    new_arr[is_bg, 3] = 0  # Rendre transparent
    return new_arr


def find_sprites(mask, min_size=50):
    """Trouve les bounding boxes des zones non-transparentes."""
    struct = ndimage.generate_binary_structure(2, 2)
    # Petite dilatation pour fusionner les pixels proches d'un même sprite
    dilated = ndimage.binary_dilation(mask, structure=struct, iterations=1)
    labeled, num_features = ndimage.label(dilated, structure=struct)

    bboxes = []
    for i in range(1, num_features + 1):
        ys, xs = np.where(labeled == i)
        x_min, x_max = int(xs.min()), int(xs.max())
        y_min, y_max = int(ys.min()), int(ys.max())
        w = x_max - x_min
        h = y_max - y_min
        if w >= min_size and h >= min_size:
            bboxes.append((x_min, y_min, x_max + 1, y_max + 1))

    # Trier par lignes puis colonnes
    bboxes.sort(key=lambda b: (b[1], b[0]))
    rows = []
    current_row = [bboxes[0]]
    for bbox in bboxes[1:]:
        current_center_y = sum(b[1] + b[3] for b in current_row) / (2 * len(current_row))
        bbox_center_y = (bbox[1] + bbox[3]) / 2
        if abs(bbox_center_y - current_center_y) < 180:
            current_row.append(bbox)
        else:
            rows.append(sorted(current_row, key=lambda b: b[0]))
            current_row = [bbox]
    rows.append(sorted(current_row, key=lambda b: b[0]))

    sorted_bboxes = []
    for row in rows:
        sorted_bboxes.extend(row)

    # Post-traitement : couper les blobs trop hauts (>600px) en deux moitiés
    final = []
    for (x1, y1, x2, y2) in sorted_bboxes:
        h = y2 - y1
        if h > 600:
            mid_y = (y1 + y2) // 2
            final.append((x1, y1, x2, mid_y))
            final.append((x1, mid_y, x2, y2))
        else:
            final.append((x1, y1, x2, y2))

    # Re-trier par lignes après la coupe
    final.sort(key=lambda b: (b[1], b[0]))
    rows2 = []
    current_row2 = [final[0]]
    for bbox in final[1:]:
        current_center_y = sum(b[1] + b[3] for b in current_row2) / (2 * len(current_row2))
        bbox_center_y = (bbox[1] + bbox[3]) / 2
        if abs(bbox_center_y - current_center_y) < 180:
            current_row2.append(bbox)
        else:
            rows2.append(sorted(current_row2, key=lambda b: b[0]))
            current_row2 = [bbox]
    rows2.append(sorted(current_row2, key=lambda b: b[0]))

    final_sorted = []
    for row in rows2:
        final_sorted.extend(row)

    return final_sorted, rows2


def main():
    img = Image.open(INPUT).convert("RGBA")
    arr = np.array(img)
    print(f"Image source: {arr.shape[1]}x{arr.shape[0]}")

    # Étape 1 : supprimer le fond damier
    print("Suppression du fond damier...")
    clean_arr = remove_checkerboard_bg(arr)
    clean_img = Image.fromarray(clean_arr)
    os.makedirs(os.path.dirname(OUTPUT_CLEAN), exist_ok=True)
    clean_img.save(OUTPUT_CLEAN)
    print(f"Image nettoyée: {OUTPUT_CLEAN}")

    # Stats
    transparent_pct = (clean_arr[:, :, 3] == 0).sum() / clean_arr[:, :, 3].size * 100
    print(f"Pixels rendus transparents: {transparent_pct:.1f}%")

    # Étape 2 : détecter les sprites
    print("\nDétection des sprites...")
    mask = clean_arr[:, :, 3] > 0
    bboxes, rows = find_sprites(mask)

    print(f"Sprites détectés: {len(bboxes)} (attendus: {len(TILE_NAMES)})")
    for ri, row in enumerate(rows):
        print(f"  Ligne {ri + 1}: {len(row)} sprites")
        for x1, y1, x2, y2 in row:
            print(f"    ({x1},{y1})→({x2},{y2})  {x2-x1}x{y2-y1}")

    # Étape 3 : découper et assembler
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_GRID), exist_ok=True)

    grid = Image.new("RGBA", (GRID_COLS * TILE_SIZE, GRID_ROWS * TILE_SIZE), (0, 0, 0, 0))

    count = min(len(bboxes), len(TILE_NAMES))
    for i in range(count):
        name = TILE_NAMES[i]
        x1, y1, x2, y2 = bboxes[i]

        crop = clean_img.crop((x1, y1, x2, y2))

        # Trim edges transparents
        bbox = crop.getbbox()
        if bbox:
            crop = crop.crop(bbox)

        # Resize proportionnel max 64x64
        crop.thumbnail((TILE_SIZE, TILE_SIZE), Image.LANCZOS)

        # Centrer sur canvas 64x64
        tile = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
        ox = (TILE_SIZE - crop.width) // 2
        oy = (TILE_SIZE - crop.height) // 2
        tile.paste(crop, (ox, oy))

        tile_path = os.path.join(OUTPUT_DIR, f"{name}.png")
        tile.save(tile_path)
        print(f"  [{i+1:2d}/{count}] {name} ({x2-x1}x{y2-y1} → {TILE_SIZE}x{TILE_SIZE})")

        col = i % GRID_COLS
        row = i // GRID_COLS
        grid.paste(tile, (col * TILE_SIZE, row * TILE_SIZE))

    grid.save(OUTPUT_GRID)
    print(f"\nGrille: {OUTPUT_GRID} ({grid.size[0]}x{grid.size[1]})")
    print("Terminé !")


if __name__ == "__main__":
    main()
