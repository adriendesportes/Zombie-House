# STORY-001b : Sprites 8 directions (style Brawl Stars)

**Epic** : MVP
**Statut** : TODO
**Depends on** : STORY-001

---

## Objectif

Rendre les deplacements des personnages plus naturels en passant de 2 directions (front/back) a 8 directions avec rotation a 45 degres, inspire de Brawl Stars.

## Directions

| # | Direction | Angle | Sprite sheet |
|---|-----------|-------|--------------|
| 1 | Avant (face camera) | 0° (Sud) | `idle-0.png` / `walk-0.png` |
| 2 | Avant-droite | 45° (Sud-Est) | `idle-45.png` / `walk-45.png` |
| 3 | Droite | 90° (Est) | `idle-90.png` / `walk-90.png` |
| 4 | Arriere-droite | 135° (Nord-Est) | `idle-135.png` / `walk-135.png` |
| 5 | Arriere (dos camera) | 180° (Nord) | `idle-180.png` / `walk-180.png` |
| 6 | Arriere-gauche | 225° (Nord-Ouest) | `idle-225.png` / `walk-225.png` |
| 7 | Gauche | 270° (Ouest) | `idle-270.png` / `walk-270.png` |
| 8 | Avant-gauche | 315° (Sud-Ouest) | `idle-315.png` / `walk-315.png` |

> Note : les directions gauche (270°, 225°, 315°) peuvent etre obtenues par flip horizontal des sprites droite (90°, 135°, 45°), ce qui reduit le travail a 5 directions uniques.

## Specifications par sprite sheet

- **idle** : 4 frames x 128px (comme existant)
- **walk** : 6 frames x 128px (comme existant)
- Style : vue isometrique top-down a 45°, coherent avec le rendu actuel

## Personnages concernes (Phase 1)

### 1. Zombie Normal
- Dossier : `public/assets/sprites/enemies/zombie-normal/`
- Existant : `idle-front.png`, `idle-back.png`, `walk-front.png`, `walk-back.png`
- A creer : sprites pour les 5 directions uniques (0°, 45°, 90°, 135°, 180°)
- Les 3 directions miroir (225°, 270°, 315°) sont des flips horizontaux

### 2. Angel Monster (joueur)
- Dossier : `public/assets/sprites/heroes/angel-monster/`
- Existant : `idle.png` (back), `idle-front.png`, `walk.png` (back), `walk-front.png`
- A creer : sprites pour les 5 directions uniques (0°, 45°, 90°, 135°, 180°)
- Les 3 directions miroir (225°, 270°, 315°) sont des flips horizontaux

## Taches

### Assets (par personnage)
- [ ] Generer/dessiner les sprite sheets pour les 5 directions uniques (idle + walk)
- [ ] Renommer les sprites existants pour suivre la nouvelle convention (`idle-front` -> `idle-0`, `idle-back` -> `idle-180`)

### Code - Chargement (`src/renderer/characters.js`)
- [ ] Charger les 5 textures idle + 5 textures walk par personnage
- [ ] Configurer le flip horizontal pour les 3 directions miroir

### Code - Selection de direction (`src/renderer/ThreeRenderer.js`)
- [ ] Remplacer la logique binaire `facingDown` par un calcul d'angle en 8 secteurs
- [ ] Mapper l'angle `atan2(facingDx, facingDy)` vers le sprite sheet correct
- [ ] Gerer le flip horizontal (scale.x = -1) pour les directions 225°, 270°, 315°

### Code - Direction tracking (`src/update.js`)
- [ ] Conserver `facingDx` / `facingDy` (deja en place)
- [ ] Aucun changement necessaire cote logique de jeu

## Logique de selection (pseudo-code)

```javascript
// Convertir le vecteur de direction en angle (0-360)
const angle = (Math.atan2(facingDx, facingDy) * 180 / Math.PI + 360) % 360;

// Snapper a la direction la plus proche (secteurs de 45°)
const sector = Math.round(angle / 45) % 8;
const snappedAngle = sector * 45; // 0, 45, 90, 135, 180, 225, 270, 315

// Determiner si on doit flipper (directions gauche = miroir de droite)
const flip = snappedAngle > 180; // 225, 270, 315
const textureAngle = flip ? (360 - snappedAngle) : snappedAngle;
// textureAngle sera 0, 45, 90, 135 ou 180

// Appliquer le flip horizontal si necessaire
sprite.scale.x = flip ? -Math.abs(sprite.scale.x) : Math.abs(sprite.scale.x);
```

## Pipeline de production

1. **Zombie** : `generate_zombie_sprites.py` adapte pour generer les 5 poses angulaires
2. **Angel** : prompt Gemini adapte avec angle de vue specifique -> `slice_sprite.py`

## Criteres d'acceptation

- [ ] Le personnage affiche un sprite different selon sa direction de deplacement
- [ ] Les transitions entre directions sont fluides (pas de saut visuel)
- [ ] Les directions gauche sont des miroirs horizontaux des directions droite
- [ ] Compatible avec le systeme d'animation existant (idle/walk, frame timer)
