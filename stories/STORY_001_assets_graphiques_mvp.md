# STORY-001 : Créer les assets graphiques pour le MVP

**Epic** : MVP — Zombie House
**Priorité** : Haute (bloquant pour toutes les autres stories)
**Statut** : Backlog

---

## Objectif

Produire le minimum d'assets graphiques nécessaires pour avoir un jeu testable : un personnage jouable, quelques ennemis, une map de test avec quelques pièces, et les éléments d'UI.

---

## Assets requis

### 1. Personnage — Angel Monster (sprites en jeu)

| Asset                         | Taille     | Frames | Directions | Format              |
| ----------------------------- | ---------- | ------ | ---------- | ------------------- |
| Idle                          | 128x128 px | 4      | 4 (N/S/E/O)| Sprite sheet PNG    |
| Walk                          | 128x128 px | 6      | 4          | Sprite sheet PNG    |
| Attack (lancer de bras)       | 128x128 px | 4      | 4          | Sprite sheet PNG    |
| Death                         | 128x128 px | 4      | 1          | Sprite sheet PNG    |

**Vue** : Isométrique ~30° surélevée.
**Style** : Cartoon Brawl Stars, couleurs vives (bleu dominant), fond transparent.
**Référence** : `Design/Personnages/angle_monster_vue_dessus.png`

**Prompt LLM suggéré** :
```
Create a sprite sheet for a top-down isometric game (30° elevated view, Brawl Stars cartoon style).
Character: "Angel Monster" — a blue armored flying monster with 4 mechanical arms, energy wings, pirate helmet with skull, eye patch, and a trident-shaped tail. Levitates above the ground.
Sheet layout: 4 rows (North, South, East, West facing) x 4 columns (idle animation frames).
Each frame: 128x128 pixels. Transparent background. Consistent lighting from top-left.
Style: vibrant colors, thick outlines, chibi proportions, dark blue/cyan palette with glowing energy effects.
```

---

### 2. Projectile — Bras lancé

| Asset                  | Taille    | Frames | Format           |
| ---------------------- | --------- | ------ | ---------------- |
| Bras en vol            | 64x64 px  | 2      | Sprite sheet PNG |
| Impact / disparition   | 64x64 px  | 3      | Sprite sheet PNG |

**Prompt LLM suggéré** :
```
Top-down isometric sprite (30° view, Brawl Stars style): a detached blue mechanical arm projectile flying forward with energy trail. 2 animation frames, 64x64 px each, transparent background.
Also: 3 frames of impact explosion (blue sparks), 64x64 px each.
```

---

### 3. Ennemis (MVP : 2 types)

#### Zombie Normal

| Asset      | Taille     | Frames | Directions | Format           |
| ---------- | ---------- | ------ | ---------- | ---------------- |
| Walk       | 128x128 px | 4      | 4          | Sprite sheet PNG |
| Hit        | 128x128 px | 2      | 1          | Sprite sheet PNG |
| Death      | 128x128 px | 4      | 1          | Sprite sheet PNG |

**Prompt LLM suggéré** :
```
Sprite sheet for a top-down isometric game (30° elevated view, Brawl Stars cartoon style).
Character: classic zombie — decomposing humanoid, greenish skin, torn clothes, slow shambling pose, arms reaching forward.
Sheet: 4 rows (N/S/E/W) x 4 columns (walk cycle). Each frame 128x128 px. Transparent background.
Dark color palette: greens, browns, grays. Thick outlines. Chibi proportions.
```

#### Zombie Boss (simplifié pour MVP)

| Asset      | Taille     | Frames | Directions | Format           |
| ---------- | ---------- | ------ | ---------- | ---------------- |
| Idle/Walk  | 256x256 px | 4      | 4          | Sprite sheet PNG |
| Attack     | 256x256 px | 4      | 1          | Sprite sheet PNG |
| Death      | 256x256 px | 6      | 1          | Sprite sheet PNG |

**Prompt LLM suggéré** :
```
Sprite sheet for a top-down isometric game (30° elevated view, Brawl Stars cartoon style).
Character: giant zombie boss — twice the size of normal zombies, muscular, glowing red eyes, chains hanging from arms, exposed ribcage, dark aura.
Sheet: 4 rows (N/S/E/W) x 4 columns (walk cycle). Each frame 256x256 px. Transparent background.
Color palette: dark greens, reds, purples. Menacing but cartoon style.
```

---

### 4. Tileset — Manoir (MVP : 1 set minimal)

**Taille des tiles** : 64x64 px.
**Format** : PNG grille unique (tileset) ou tiles individuels.

| Tile                        | Variantes | Requis MVP |
| --------------------------- | --------- | ---------- |
| Sol parquet                 | 2         | Oui        |
| Sol pierre                  | 2         | Oui        |
| Mur brique (N, S, E, O)    | 4         | Oui        |
| Mur coin (NE, NO, SE, SO)  | 4         | Oui        |
| Porte fermée (N/S, E/O)    | 2         | Oui        |
| Porte ouverte (N/S, E/O)   | 2         | Oui        |
| Table                       | 1         | Oui        |
| Chaise                      | 1         | Non        |
| Bibliothèque                | 1         | Oui        |
| Chandelier                  | 1         | Oui        |
| Escalier                    | 1         | Non        |
| **Total tiles MVP**         |           | **~20**    |

**Prompt LLM suggéré** :
```
Create a tileset grid for a top-down isometric game (30° elevated view).
Theme: haunted mansion interior, dark gothic cartoon style (Brawl Stars aesthetic).
Grid: 6 columns x 4 rows, each tile 64x64 px. Transparent background.

Row 1: floor tiles — dark wood parquet (2 variants), gray stone (2 variants), cracked tiles, carpet
Row 2: wall tiles — dark brick wall facing North, South, East, West
Row 3: wall corners — NE, NW, SE, SW + door closed (N/S facing) + door open (N/S facing)
Row 4: furniture — wooden table, bookshelf, chandelier (floor), broken chair, cobweb decoration, barrel

Color palette: dark browns, grays, deep purples. Accent: orange candlelight, green/blue ghostly glow.
All tiles must connect seamlessly. Consistent perspective and lighting (top-left source).
```

---

### 5. UI

| Asset                   | Taille     | Format |
| ----------------------- | ---------- | ------ |
| Joystick base (cercle)  | 128x128 px | PNG    |
| Joystick thumb (pouce)  | 64x64 px   | PNG    |
| Cœur plein              | 32x32 px   | PNG    |
| Cœur moitié             | 32x32 px   | PNG    |
| Cœur vide               | 32x32 px   | PNG    |
| Bouton "Jouer"          | 200x60 px  | PNG    |
| Bouton "Améliorer"      | 160x48 px  | PNG    |
| Fond menu               | 390x844 px | PNG    |
| Icône points (étoile)   | 32x32 px   | PNG    |

**Style** : Dark UI, bords arrondis, lueur subtile, cohérent avec l'ambiance manoir.

**Prompt LLM suggéré (cœurs)** :
```
Game UI heart icons, top-down isometric game, cartoon Brawl Stars style:
- Full heart: glowing red, 32x32 px
- Half heart: left half red, right half dark/empty, 32x32 px
- Empty heart: dark outline only, 32x32 px
Transparent background. Thick outlines. Slight glow effect.
```

---

### 6. Illustration menu — Angel Monster (haute résolution)

Déjà disponible : `Design/Personnages/angel_monster.png` (1024x1024 environ).
**Statut** : Existant, pas besoin de le régénérer.

---

## Critères d'acceptation

- [ ] Tous les sprite sheets sont en PNG fond transparent
- [ ] Les tailles de frames respectent les specs (128x128 perso, 64x64 tiles, 256x256 boss)
- [ ] Les animations sont fluides (pas de sauts visuels entre frames)
- [ ] Le tileset permet de construire au moins 3-4 pièces interconnectées
- [ ] Le style est cohérent entre tous les assets (même palette, même angle iso)
- [ ] Les assets sont placés dans `public/assets/` selon l'arborescence ARCH.md

---

## Fichiers de sortie attendus

```
public/assets/
├── sprites/
│   ├── heroes/
│   │   └── angel-monster/
│   │       ├── idle.png          (512x512 : 4x4 frames de 128x128)
│   │       ├── walk.png          (768x512 : 6x4 frames de 128x128)
│   │       ├── attack.png        (512x512 : 4x4 frames de 128x128)
│   │       └── death.png         (512x128 : 4x1 frames de 128x128)
│   └── enemies/
│       ├── zombie-normal.png     (512x512 : 4x4 walk + hit/death en feuille séparée)
│       ├── zombie-normal-fx.png  (256x128 : hit 2f + death 4f de 128x128)
│       └── bosses/
│           └── boss-level1.png   (1024x1024 : 4x4 walk de 256x256)
├── tilesets/
│   └── manor-tileset.png         (384x256 : 6x4 tiles de 64x64)
├── projectiles/
│   ├── arm-projectile.png        (128x64 : 2 frames de 64x64)
│   └── arm-impact.png            (192x64 : 3 frames de 64x64)
└── ui/
    ├── joystick-base.png
    ├── joystick-thumb.png
    ├── heart-full.png
    ├── heart-half.png
    ├── heart-empty.png
    ├── btn-play.png
    ├── btn-upgrade.png
    ├── menu-bg.png
    └── icon-points.png
```
