# STORY-001 : Assets graphiques MVP

**Epic** : MVP
**Statut** : DONE

---

## Livrable

Tous les assets graphiques minimaux pour un prototype jouable.

## Fait

### Angel Monster (sprites en jeu)
- [x] idle-back.png (4 frames x 128px) — Gemini + slice_sprite.py
- [x] idle-front.png (4 frames x 128px) — Gemini + slice_sprite.py
- [x] walk-back.png (6 frames x 128px) — Gemini + slice_sprite.py
- [x] walk-front.png (6 frames x 128px) — Gemini + slice_sprite.py

### Zombie Normal (sprites en jeu)
- [x] idle-front.png (4 frames x 128px) — generate_zombie_sprites.py
- [x] idle-back.png (4 frames x 128px) — generate_zombie_sprites.py
- [x] walk-front.png (6 frames x 128px) — generate_zombie_sprites.py
- [x] walk-back.png (6 frames x 128px) — generate_zombie_sprites.py

### Tilesets HQ (128x128, atlas PNG)
- [x] ground-atlas.png (7 tiles : herbe, pierre, terre, gravier, bois, tapis, eau)
- [x] wall-front-atlas.png (5 variantes : briques rouges, pierre grise, bois, briques grises, mousse)
- [x] wall-top-atlas.png (5 variantes assorties)
- [x] wall-dest-atlas.png (3 variantes : caisse, tonneau, pierres)
- [x] door-atlas.png (3 variantes : arche pierre, bois, grille fer)
- [x] deco-atlas.png (10 types : os, crane, fissure, toile, sang, cailloux, herbe, champignon, torche, flaque)
- [x] bush.png (buisson individuel)

### Illustrations menu
- [x] angel_monster.png (illustration HD face)
- [x] angle_monster_vue_dessus.png (vue de dessus)

### Map de reference
- [x] level_1_entree_manoir.png (image de reference)

## Pipeline de production
1. Personnage : prompt Gemini (fond blanc) -> slice_sprite.py (bg removal + detection frames + assembly)
2. Zombie : generate_zombie_sprites.py (dessin procedural PIL complet)
3. Tiles : generate_tiles_hq.py (dessin procedural PIL 128x128, assembly en atlas)
