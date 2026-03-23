"""
Découpe un sprite sheet en grille en frames individuels et crée un sprite sheet horizontal.
Supprime le fond noir, détecte la grille, redimensionne chaque frame.

Usage: python scripts/slice_grid_sprite.py <input> <output_dir> <sheet_name> <frame_size> [<cols>x<rows>] [--ref-size WxH]
Example: python scripts/slice_grid_sprite.py Design/Personnages/sprites/angel_monster_idle_front-256px-36.png public/assets/sprites/heroes/angel-monster idle-0 256 6x6
         python scripts/slice_grid_sprite.py ... 256 6x6 --ref-size 200x180
"""

from PIL import Image
import numpy as np
import os
import sys


def remove_black_background(img, threshold=30):
    """Remplace le fond noir par de la transparence."""
    arr = np.array(img.convert("RGBA"))
    r, g, b = arr[:, :, 0].astype(int), arr[:, :, 1].astype(int), arr[:, :, 2].astype(int)
    luminance = (r + g + b) / 3.0
    is_bg = luminance < threshold
    arr[is_bg, 3] = 0
    return Image.fromarray(arr)


def slice_grid(img, cols, rows):
    """Découpe l'image en grille régulière et retourne les frames."""
    w, h = img.size
    fw = w // cols
    fh = h // rows
    frames = []
    for row in range(rows):
        for col in range(cols):
            x1 = col * fw
            y1 = row * fh
            frame = img.crop((x1, y1, x1 + fw, y1 + fh))
            frames.append(frame)
    return frames, fw, fh


def compute_uniform_bbox(frames):
    """Calcule un bounding box englobant toutes les frames (taille max)."""
    max_w = 0
    max_h = 0
    for frame in frames:
        bbox = frame.getbbox()
        if bbox:
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            max_w = max(max_w, w)
            max_h = max(max_h, h)
    return max_w, max_h


def resize_frame(frame, target_size):
    """Resize la frame brute (sans trim) en target_size x target_size.
    Garde les proportions, centre sur le canvas."""
    if not frame.getbbox():
        return Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))

    ratio = min(target_size / frame.width, target_size / frame.height)
    new_w = int(frame.width * ratio)
    new_h = int(frame.height * ratio)
    resized = frame.resize((new_w, new_h), Image.LANCZOS)

    canvas = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
    ox = (target_size - new_w) // 2
    oy = (target_size - new_h) // 2
    canvas.paste(resized, (ox, oy))
    return canvas


def main():
    if len(sys.argv) < 5:
        print("Usage: python slice_grid_sprite.py <input> <output_dir> <sheet_name> <frame_size> [<cols>x<rows>]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2]
    sheet_name = sys.argv[3]
    frame_size = int(sys.argv[4])
    grid = None
    ref_size = None
    i = 5
    while i < len(sys.argv):
        if sys.argv[i] == '--ref-size':
            ref_size = tuple(map(int, sys.argv[i + 1].split('x')))
            i += 2
        else:
            grid = sys.argv[i]
            i += 1

    img = Image.open(input_path).convert("RGBA")
    print(f"Image source: {img.size[0]}x{img.size[1]}")

    # Supprimer le fond noir
    print("Suppression du fond noir...")
    img = remove_black_background(img)

    # Déterminer la grille
    if grid:
        cols, rows = map(int, grid.split("x"))
    else:
        # Auto-detect: essayer de deviner à partir du ratio
        w, h = img.size
        ratio = w / h
        if ratio > 1.5:
            cols, rows = 6, 1
        elif ratio > 1:
            cols, rows = 4, 1
        else:
            # Probablement une grille carrée
            cols = rows = int(round((w * h / (256 * 256)) ** 0.5))
        print(f"Grille auto-détectée: {cols}x{rows}")

    print(f"Grille: {cols}x{rows} = {cols * rows} frames")

    # Découper
    frames_raw, fw, fh = slice_grid(img, cols, rows)
    print(f"Taille frame brute: {fw}x{fh}")

    os.makedirs(output_dir, exist_ok=True)

    # Traiter chaque frame (pas de trim, resize direct de la cellule de grille)
    frames = []
    for i, frame in enumerate(frames_raw):
        processed = resize_frame(frame, frame_size)

        # Vérifier que le frame n'est pas vide
        if processed.getbbox() is None:
            print(f"  [{i + 1}/{len(frames_raw)}] VIDE — ignoré")
            continue

        frame_path = os.path.join(output_dir, f"{sheet_name}-{i + 1}.png")
        processed.save(frame_path)
        frames.append(processed)
        print(f"  [{i + 1}/{len(frames_raw)}] ({fw}x{fh} → {frame_size}x{frame_size}) → {frame_path}")

    # Assembler le sprite sheet horizontal
    if frames:
        sheet = Image.new("RGBA", (frame_size * len(frames), frame_size), (0, 0, 0, 0))
        for i, frame in enumerate(frames):
            sheet.paste(frame, (i * frame_size, 0))

        sheet_path = os.path.join(output_dir, f"{sheet_name}.png")
        sheet.save(sheet_path)
        print(f"\nSprite sheet: {sheet_path} ({sheet.size[0]}x{sheet.size[1]}, {len(frames)} frames)")
    else:
        print("\nAucun frame valide trouvé!")

    print("Terminé !")


if __name__ == "__main__":
    main()
