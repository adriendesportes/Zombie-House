# Architecture — Zombie House

## 1. Choix technologique

### Deux prototypes independants

Le projet est actuellement organise en deux renderers distincts, chacun dans un seul fichier HTML autonome. Il n'y a pas de bundler, pas de framework de jeu, pas de Tiled Map Editor.

| Critere              | 2D Canvas (test-map.html)           | 3D Three.js (test-map-3d.html)         |
| -------------------- | ------------------------------------ | --------------------------------------- |
| Rendu                | HTML5 Canvas 2D natif               | Three.js (ES modules CDN)              |
| Shading              | Dessin manuel, palette fixe         | MeshToonMaterial, cel-shading          |
| Murs                 | Face top + face front dessinee       | BoxGeometry InstancedMesh              |
| Personnages          | Sprite sheets PNG frame-by-frame    | Sprite billboard (PNG) + primitives    |
| Dependances          | Aucune                              | Three.js CDN uniquement                |
| Cible principale     | Gameplay, logique, mobile           | Exploration visuelle                   |

### Stack complet

```
2D renderer   — HTML5 Canvas 2D pur (test-map.html)
3D renderer   — Three.js r165+ (ES modules, CDN) (test-map-3d.html)
Tiles         — Python + Pillow (generation procedurale d'atlas PNG)
Sprites       — Python + Pillow (generation procedurale) ou Gemini (LLM) + slicing Python
Maps          — JSON manuel dans public/assets/maps/
Sauvegarde    — localStorage
PWA           — optionnel, mobile install
```

---

## 2. Structure du projet

```
zombie-house/
├── Design/
│   ├── Personnages/
│   │   ├── angel_monster.png               # Illustration menu haute resolution
│   │   ├── angle_monster_vue_dessus.png
│   │   └── sprites/                        # Sorties brutes LLM avant slicing
│   ├── Tilesets/                           # Tentatives de tilesets LLM (reference)
│   └── Maps/
│       └── level_1_entree_manoir.png       # Image de reference niveau 1
├── public/assets/
│   ├── sprites/
│   │   ├── heroes/
│   │   │   └── angel-monster/
│   │   │       ├── idle-front.png
│   │   │       ├── idle-back.png
│   │   │       ├── walk-front.png
│   │   │       └── walk-back.png
│   │   └── enemies/
│   │       └── zombie-normal/
│   │           ├── idle-front.png
│   │           ├── idle-back.png
│   │           ├── walk-front.png
│   │           └── walk-back.png
│   ├── tilesets/
│   │   ├── ground-atlas.png                # 7 types de sol (128x128 par tile)
│   │   ├── wall-front-atlas.png            # 5 variants de face avant
│   │   ├── wall-top-atlas.png              # 5 variants de face superieure
│   │   ├── wall-dest-atlas.png             # 3 murs destructibles
│   │   ├── door-atlas.png                  # 3 variants de portes
│   │   ├── deco-atlas.png                  # 10 types de decorations
│   │   ├── bush.png                        # Sprite de buisson individuel
│   │   └── tiles/                          # Tiles individuelles 32x32 (legacy)
│   └── maps/
│       └── level-1.json
│   └── audio/
│       ├── music/
│       │   ├── menu-theme.mp3
│       │   ├── gameplay-exploration.mp3
│       │   ├── gameplay-combat.mp3
│       │   ├── boss-fight.mp3
│       │   ├── victory.mp3
│       │   └── game-over.mp3
│       └── sfx/
│           ├── player-footstep-wood.mp3
│           ├── player-footstep-stone.mp3
│           ├── player-attack-whoosh.mp3
│           ├── player-special-electric.mp3
│           ├── player-hit.mp3
│           ├── player-death.mp3
│           ├── zombie-groan.mp3
│           ├── zombie-spawn-surprise.mp3
│           ├── zombie-hit.mp3
│           ├── zombie-death.mp3
│           ├── boss-roar.mp3
│           ├── door-creak.mp3
│           ├── button-click.mp3
│           ├── ambiance-manor.mp3
│           ├── ui-click.mp3
│           ├── ui-upgrade.mp3
│           ├── ui-level-unlock.mp3
│           └── ui-points.mp3
├── scripts/
│   ├── generate_tiles_hq.py                # Generateur d'atlas 128x128 (actif)
│   ├── generate_tiles.py                   # Generateur 32x32 (legacy)
│   ├── generate_zombie_sprites.py          # Sprites zombie proceduraux
│   ├── slice_sprite.py                     # Decoupe sprites LLM (fond blanc → frames)
│   └── slice_tileset*.py                   # Scripts de decoupe de tilesets
├── test-map.html                           # Prototype renderer 2D Canvas
├── test-map-3d.html                        # Prototype renderer Three.js
├── test-animation.html                     # Apercu des animations de sprites
├── PRD.md
├── ARCH.md
├── epic_suivi.md
└── stories/
```

---

## 3. Rendu 2D Canvas

### 3.1 Grille et coordonnees

- Tiles carrees de **40x40 px** (taille affichage, pas la taille source de l'atlas).
- Origine (0,0) en haut a gauche. X vers la droite, Y vers le bas.
- Les murs occupent 40x40 en face superieure et ajoutent une **face avant de 40x14 px** qui depasse en dessous de la tile (cette face est rendue dans le Y-sort).

### 3.2 Pipeline de rendu (8 passes)

```
1. Ground pass       : Toutes les tiles de sol, de gauche a droite, haut en bas.
2. Decorations       : Decorations au sol (os, flaques, etc.) sous les entites.
3. Wall shadows      : Ombres projetees par les murs (rectangle sombre sous la face avant).
4. Y-sorted entities : Murs (face top + face avant), buissons, personnages, portes.
                       Trie par coordonnee Y (bas de l'entite), du plus petit au plus grand.
5. Projectiles       : Bras projetes, boules electriques.
6. Particles         : Effets de particules (impact, explosion, fumee).
7. Damage popups     : Nombres de degats flottants.
8. UI overlay        : Coeurs, score, joystick virtuel, bouton attaque.
```

### 3.3 Y-sorting

Chaque entite expose une valeur `sortY` (generalement le bas du sprite ou le milieu du personnage). La passe 4 trie toutes les entites par `sortY` croissant avant le dessin. Cela permet a un personnage devant un mur d'etre dessine apres le mur et donc de sembler en avant.

### 3.4 Variation deterministe des tiles

Pour eviter la repetition visuelle sans aleatoire au runtime, chaque position de tile utilise un hash de sa coordonnee (x, y) pour selectionner une variante dans l'atlas. Le rendu est identique a chaque chargement.

```javascript
function tileVariant(x, y, numVariants) {
  const hash = (x * 73856093) ^ (y * 19349663);
  return Math.abs(hash) % numVariants;
}
```

---

## 4. Rendu 3D Three.js

### 4.1 Camera

- `PerspectiveCamera`, FOV ~50, positionnee au-dessus et derriere le joueur.
- Suivi du joueur par interpolation lineaire (`lerp`) sur la cible de la camera.

### 4.2 Sol

- `PlaneGeometry` unique couvrant la map entiere.
- Texture generee via `CanvasTexture` (dessin des tiles sur un canvas offscreen).

### 4.3 Murs

- `InstancedMesh` avec `BoxGeometry` parametree en hauteur.
- Chaque mur est une instance avec sa matrice de transformation.
- Materiau : `MeshToonMaterial`.

### 4.4 Personnages

- Player : sprite billboard (plane qui fait face a la camera) avec la PNG du sprite sheet.
- Zombies : geometries low-poly primitives (box/capsule) avec MeshToonMaterial.

### 4.5 Eclairage

- `AmbientLight` pour la lumiere de base.
- `DirectionalLight` pour les ombres globales.
- `PointLight` positionnes aux torches decoratives.

### 4.6 Contours (cel-shading outlines)

- Technique "inverted hull" : le mesh est duplique, les faces sont inversees, le materiau est noir opaque avec `side: BackSide`, et la geometrie est legrement agrandie. Cela produit un contour epais visible.

### 4.7 Effets

- Projectiles : sphere avec trail (suite de spheres degressives en opacite).
- Particules : pool pre-alloue de `Sprite` Three.js recycles.
- Popups de degats : `Sprite` Three.js avec texture texte generee sur canvas.

### 4.8 UI

- Overlay HTML positionne par-dessus le canvas Three.js.
- Joystick virtuel et bouton attaque en HTML/CSS pour les mobiles.
- Compteurs (coeurs, score) en HTML.

---

## 5. Format des maps (JSON)

Les maps sont definies manuellement en JSON. Pas de Tiled Map Editor.

```json
{
  "width": 30,
  "height": 50,
  "tileSize": 40,
  "layers": {
    "ground": [
      [1, 1, 1, 0, 0],
      [1, 1, 0, 0, 0]
    ],
    "walls": [
      [0, 0, 2, 2, 2],
      [0, 0, 2, 0, 2]
    ],
    "decorations": [
      [0, 3, 0, 0, 0],
      [0, 0, 0, 0, 0]
    ]
  },
  "objects": [
    { "type": "player_spawn", "x": 3, "y": 45 },
    { "type": "zombie_normal", "x": 10, "y": 20 },
    { "type": "zombie_boss", "x": 15, "y": 5 },
    { "type": "door", "x": 12, "y": 30, "trigger": "switch_1" },
    { "type": "surprise_spawn", "subtype": "zombie_rage", "x": 8, "y": 15,
      "trigger": "proximity", "animation": "fall_ceiling" }
  ]
}
```

- Les couches `ground`, `walls`, `decorations` sont des tableaux 2D d'indices de tiles (0 = vide).
- Les indices referent aux colonnes des atlas PNG correspondants.
- Les objets definissent les entites dynamiques, spawn points et triggers.

---

## 6. Pipeline d'assets

### 6.1 Tiles (Python + Pillow)

Le script `scripts/generate_tiles_hq.py` genere les atlas PNG a 128x128 px par tile de maniere procedurale. Chaque atlas est une bande horizontale de N tiles.

```
python scripts/generate_tiles_hq.py
→ public/assets/tilesets/ground-atlas.png      (7 tiles)
→ public/assets/tilesets/wall-front-atlas.png  (5 tiles)
→ public/assets/tilesets/wall-top-atlas.png    (5 tiles)
→ public/assets/tilesets/wall-dest-atlas.png   (3 tiles)
→ public/assets/tilesets/door-atlas.png        (3 tiles)
→ public/assets/tilesets/deco-atlas.png        (10 tiles)
```

Le renderer charge ces atlas et extrait chaque tile par decalage (`sourceX = tileIndex * 128`), puis la redimensionne a 40x40 px (ou 40x14 px pour la face avant).

### 6.2 Sprites de personnages (pipeline LLM + slicing)

```
1. Generation via Gemini (LLM) : personnage sur fond blanc, vue de face ou de dos.
2. scripts/slice_sprite.py     : suppression du fond blanc, detection des frames,
                                 assemblage en sprite sheet PNG transparent.
3. Resultat                    : public/assets/sprites/heroes/angel-monster/idle-front.png, etc.
```

### 6.3 Sprites zombies (Python procedural)

```
python scripts/generate_zombie_sprites.py
→ public/assets/sprites/enemies/zombie-normal/idle-front.png
→ public/assets/sprites/enemies/zombie-normal/idle-back.png
→ public/assets/sprites/enemies/zombie-normal/walk-front.png
→ public/assets/sprites/enemies/zombie-normal/walk-back.png
```

---

## 7. Architecture des entites (2D Canvas)

### 7.1 Hierarchie conceptuelle

```
Entity (base)
├── props : x, y, width, height, sortY
├── update(delta)
└── draw(ctx)

Player extends Entity
├── stats      : hp, maxHp, power, speed, level
├── facingDown : boolean (true = vue front, false = vue back)
├── spriteSheet: { idleFront, idleBack, walkFront, walkBack }
├── move(dx, dy)
├── attack()           → cree un ArmProjectile vers la cible la plus proche
└── specialAttack()    → cree un ElectricBall (si level 11, cooldown OK)

Enemy extends Entity
├── type      : 'normal' | 'medium' | 'rage' | 'boss'
├── hp, maxHp, damage, speed, points
├── facingDown: boolean
└── update(delta) → pathfinding vers le joueur

ZombieNormal extends Enemy
ZombieMedium extends Enemy
ZombieRage   extends Enemy  → charge en ligne droite
ZombieBoss   extends Enemy  → patterns d'attaque

Projectile extends Entity
├── vx, vy, damage, range, traveled
├── type : 'arm' | 'electric'
└── update(delta) → deplacement, detection collision, expiration

Particle extends Entity
└── pool pre-alloue, recyclage apres duree de vie
```

### 7.2 Stats Angel Monster par niveau

```javascript
const ANGEL_MONSTER = {
  baseStats: {
    hp: 6,          // 3 coeurs = 6 demi-coeurs
    power: 1,
    speed: 150,     // px/sec
    attackRange: 5, // tiles
  },
  levelBonus: {
    power: 0.10,    // +10% par niveau
    hp: 1,          // +1 demi-coeur par niveau
  },
  specialAttack: {
    unlockLevel: 11,
    cooldown: 15000, // ms
    radius: 3,       // tiles
    damage: 999,
  },
  upgradeCosts: [0, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100],
};
```

---

## 8. Systeme d'input

### 8.1 Desktop

```javascript
// Mouvement : ZQSD ou WASD
// Attaque   : Espace ou clic gauche (auto-vise le zombie le plus proche)
// Special   : (niveau 11 uniquement)

window.addEventListener('keydown', e => { keys[e.code] = true; });
window.addEventListener('keyup',   e => { keys[e.code] = false; });
canvas.addEventListener('click',   () => player.attack());
```

### 8.2 Mobile

- **Joystick virtuel gauche** : zone touch HTML positionnee en bas a gauche. Calcul du vecteur direction normalise depuis le centre du joystick.
- **Bouton attaque droit** : zone touch HTML en bas a droite. Declenche `player.attack()` en continu pendant la pression.
- **Bouton special** : apparait au niveau 11.
- L'UI mobile est un overlay HTML sur le canvas.

### 8.3 Detection de plateforme

```javascript
const isMobile = /Android|iPhone|iPad/i.test(navigator.userAgent)
              || ('ontouchstart' in window);
// Affiche joystick/boutons si mobile, masque sinon.
```

---

## 9. Game loop

```javascript
let lastTime = 0;

function gameLoop(timestamp) {
  const delta = (timestamp - lastTime) / 1000; // secondes
  lastTime = timestamp;

  // 1. Input
  const { dx, dy } = getMovementInput();
  player.move(dx * player.speed * delta, dy * player.speed * delta);

  // 2. Attaque auto ou manuelle
  if (isAttacking()) player.attack();
  if (isSpecial() && player.level >= 11) player.specialAttack();

  // 3. IA ennemis
  for (const enemy of enemies) {
    enemy.update(delta);
  }

  // 4. Projectiles
  for (const proj of projectiles) {
    proj.update(delta);
  }

  // 5. Collisions
  checkProjectileVsEnemies();
  checkEnemiesVsPlayer();
  checkPlayerVsWalls();
  checkPlayerVsDoors();

  // 6. Spawns programmes
  spawnManager.update(delta);

  // 7. Conditions de fin
  if (enemies.length === 0) triggerVictory();
  if (player.hp <= 0)       triggerDeath();

  // 8. Rendu (8 passes)
  render();

  requestAnimationFrame(gameLoop);
}
```

---

## 10. Systeme audio

### 10.1 Architecture

L'audio utilise l'API Web Audio native. Pas de librairie audio tierce.

```javascript
const AudioManager = {
  ctx: new AudioContext(),
  musicGain: null,    // GainNode pour la musique
  sfxGain: null,      // GainNode pour les SFX
  currentMusic: null, // AudioBufferSourceNode actif

  async playMusic(url, loop = true) { ... },
  async crossfadeTo(url, duration = 1.0) { ... },
  async playSFX(url) { ... },
  setMusicVolume(vol) { this.musicGain.gain.value = vol; },
  setSFXVolume(vol)   { this.sfxGain.gain.value = vol; },
  // Deblocage autoplay mobile : appele au premier touch
  unlock() { if (this.ctx.state === 'suspended') this.ctx.resume(); },
};
```

### 10.2 Declenchement contextuel

```
game loop :
  - Aucun ennemi a proximite     → crossfadeTo("gameplay-exploration")
  - Ennemi a moins de 5 tiles    → crossfadeTo("gameplay-combat")
  - Boss spawn                   → crossfadeTo("boss-fight")
  - Victoire                     → stopMusic() + playSFX("victory")
  - Mort                         → stopMusic() + playSFX("game-over")

spawnManager :
  - Zombie surprise              → playSFX("zombie-spawn-surprise")
  - Boss apparition              → playSFX("boss-roar")

collision :
  - Projectile touche ennemi     → playSFX("zombie-hit")
  - Ennemi tue                   → playSFX("zombie-death")
  - Joueur touche                → playSFX("player-hit")
  - Joueur mort                  → playSFX("player-death")

player.move() :
  - En deplacement               → playSFX("footstep-wood") tous les 0.3s

player.attack() :
  - Attaque normale              → playSFX("player-attack-whoosh")
  - Attaque speciale             → playSFX("player-special-electric")
```

---

## 11. Sauvegarde

```javascript
const SaveManager = {
  KEY: 'zombie-house-save',

  defaultSave: () => ({
    points: 0,
    maxLevelUnlocked: 1,
    heroes: {
      'angel-monster': { unlocked: true, level: 1 },
      'hero-2':         { unlocked: false, level: 1 },
      'hero-3':         { unlocked: false, level: 1 },
    },
    audio: {
      musicVolume: 0.4,
      sfxVolume: 0.7,
      muted: false,
    },
  }),

  save(data)  { localStorage.setItem(this.KEY, JSON.stringify(data)); },
  load()      {
    const raw = localStorage.getItem(this.KEY);
    return raw ? JSON.parse(raw) : this.defaultSave();
  },
};
```

---

## 12. Responsive et adaptation ecran

```
Resolution de base : 390 x 844 (iPhone 14, portrait)
Scaling            : Le canvas est redimensionne pour remplir la fenetre
                     en conservant le ratio portrait (letterbox horizontal si necessaire).

Sur Mac (navigateur) :
  - Canvas centre dans la fenetre du navigateur.
  - Joysticks HTML masques, controles clavier/souris actives.

Sur mobile :
  - Canvas plein ecran.
  - Joystick et boutons HTML overlay actives.
  - Pinch-to-zoom desactive via meta viewport.
```

---

## 13. Pipeline de developpement

```
Phase 1 — Fondations (MVP)
  ├── Renderer 2D Canvas : grille, murs extrudes, Y-sort
  ├── Atlas de tiles generes par script Python
  ├── Angel Monster : mouvement, sprites front/back, attaque
  ├── Joystick virtuel HTML (mobile) + clavier/souris (desktop)
  ├── 1 ennemi (Zombie Normal) avec IA basique
  ├── Collision murs + map JSON niveau 1
  ├── Systeme de vie (coeurs)
  ├── Systeme de points + sauvegarde localStorage
  ├── AudioManager Web Audio + musique menu + musique gameplay
  └── SFX de base (attaque, zombie hit/death, pas)

Phase 2 — Contenu et menus
  ├── Menu principal + selection personnage
  ├── Menu amelioration + systeme de niveaux 1-11
  ├── 4 types de zombies
  ├── Spawns surprise + SFX surprise
  ├── Portes + declencheurs + SFX interactions
  ├── Ecrans mort / victoire + jingles
  ├── Attaque speciale niveau 11 + SFX electricite
  ├── Crossfade musical contextuel
  └── Options volume (musique / SFX / mute)

Phase 3 — Contenu complet
  ├── 10 maps completes (JSON)
  ├── Personnages 2 et 3
  ├── Ambiance sonore par type de salle
  ├── Polish animations, particules, effets visuels
  └── PWA manifest pour installation mobile (optionnel)
```
