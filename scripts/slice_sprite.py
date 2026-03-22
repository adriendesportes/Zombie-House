"""
Découpe un sprite sheet raw en frames individuels et crée un sprite sheet propre.
Supprime le fond blanc/gris, détecte les frames, redimensionne en 128x128.

Usage: python scripts/slice_sprite.py <input> <output_dir> <sheet_name> <frame_size> [<num_expected>]
Example: python scripts/slice_sprite.py Design/Personnages/sprites/angel-monster-idle-raw.png public/assets/sprites/heroes/angel-monster idle 128 4
"""

from PIL import Image
import numpy as np
from scipy import ndimage
import os
import sys


def remove_background(arr, threshold=15):
    """Supprime le fond blanc/gris en le rendant transparent."""
    r, g, b = arr[:, :, 0].astype(np.int16), arr[:, :, 1].astype(np.int16), arr[:, :, 2].astype(np.int16)

    # Écart max entre canaux (gris neutre = faible écart)
    max_diff = np.stack([r, g, b], axis=-1)
    channel_diff = max_diff.max(axis=-1) - max_diff.min(axis=-1)

    lum = (r + g + b) / 3.0

    # Fond = gris neutre (diff < threshold) OU blanc (lum > 240)
    is_bg = ((channel_diff < threshold) & (lum > 60) & (lum < 140)) | (lum > 240)

    # Érosion puis dilatation pour nettoyer les bords
    is_bg = ndimage.binary_erosion(is_bg, iterations=1)
    is_bg = ndimage.binary_dilation(is_bg, iterations=2)

    new_arr = arr.copy()
    new_arr[is_bg, 3] = 0
    return new_arr


def find_frames(mask, min_size=50):
    """Trouve les sprites par composantes connexes, triés de gauche à droite."""
    struct = ndimage.generate_binary_structure(2, 2)
    dilated = ndimage.binary_dilation(mask, structure=struct, iterations=2)
    labeled, num_features = ndimage.label(dilated, structure=struct)

    bboxes = []
    for i in range(1, num_features + 1):
        ys, xs = np.where(labeled == i)
        x1, x2 = int(xs.min()), int(xs.max()) + 1
        y1, y2 = int(ys.min()), int(ys.max()) + 1
        if (x2 - x1) >= min_size and (y2 - y1) >= min_size:
            bboxes.append((x1, y1, x2, y2))

    # Trier de gauche à droite
    bboxes.sort(key=lambda b: b[0])
    return bboxes


def main():
    if len(sys.argv) < 5:
        print("Usage: python slice_sprite.py <input> <output_dir> <sheet_name> <frame_size> [num_expected]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2]
    sheet_name = sys.argv[3]
    frame_size = int(sys.argv[4])
    num_expected = int(sys.argv[5]) if len(sys.argv) > 5 else None

    img = Image.open(input_path).convert("RGBA")
    arr = np.array(img)
    print(f"Image source: {arr.shape[1]}x{arr.shape[0]}")

    # Vérifier si le fond est déjà transparent
    alpha = arr[:, :, 3]
    transparent_pct = (alpha == 0).sum() / alpha.size * 100

    if transparent_pct < 5:
        print(f"Fond opaque détecté ({transparent_pct:.1f}% transparent), suppression du fond...")
        arr = remove_background(arr)
        transparent_pct = (arr[:, :, 3] == 0).sum() / arr[:, :, 3].size * 100
        print(f"Après nettoyage: {transparent_pct:.1f}% transparent")
    else:
        print(f"Fond déjà transparent ({transparent_pct:.1f}%)")

    clean_img = Image.fromarray(arr)

    # Détecter les frames
    mask = arr[:, :, 3] > 0
    bboxes = find_frames(mask)
    print(f"Frames détectées: {len(bboxes)}")

    if num_expected and len(bboxes) != num_expected:
        print(f"ATTENTION: {len(bboxes)} frames détectées, {num_expected} attendues")

    # Créer le dossier de sortie
    os.makedirs(output_dir, exist_ok=True)

    # Découper chaque frame
    frames = []
    for i, (x1, y1, x2, y2) in enumerate(bboxes):
        crop = clean_img.crop((x1, y1, x2, y2))

        # Trim transparent
        bbox = crop.getbbox()
        if bbox:
            crop = crop.crop(bbox)

        # Resize proportionnel
        crop.thumbnail((frame_size, frame_size), Image.LANCZOS)

        # Centrer sur canvas
        frame = Image.new("RGBA", (frame_size, frame_size), (0, 0, 0, 0))
        ox = (frame_size - crop.width) // 2
        oy = (frame_size - crop.height) // 2
        frame.paste(crop, (ox, oy))

        # Sauvegarder le frame individuel
        frame_path = os.path.join(output_dir, f"{sheet_name}-{i+1}.png")
        frame.save(frame_path)
        frames.append(frame)
        print(f"  [{i+1}/{len(bboxes)}] ({x2-x1}x{y2-y1} → {frame_size}x{frame_size}) → {frame_path}")

    # Assembler le sprite sheet (1 ligne)
    sheet = Image.new("RGBA", (frame_size * len(frames), frame_size), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        sheet.paste(frame, (i * frame_size, 0))

    sheet_path = os.path.join(output_dir, f"{sheet_name}.png")
    sheet.save(sheet_path)
    print(f"\nSprite sheet: {sheet_path} ({sheet.size[0]}x{sheet.size[1]})")
    print("Terminé !")


if __name__ == "__main__":
    main()
