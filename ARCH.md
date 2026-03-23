# Architecture — Zombie House

## 1. Choix technologique

### Renderer unique : Three.js

Le jeu utilise un seul renderer 3D base sur Three.js charge via CDN (ES modules). Pas de bundler, pas de framework de jeu.

| Critere              | Choix                                   |
| -------------------- | ---------------------------------------- |
| Rendu                | Three.js r162 (ES modules CDN)           |
| Shading              | MeshToonMaterial, cel-shading            |
| Murs                 | BoxGeometry avec textures atlas          |
| Personnages          | Sprite billboard (PNG sheets)            |
| Eclairage            | AmbientLight + DirectionalLight + PointLights |
| Dependances          | Three.js CDN uniquement                  |
| Audio                | Web Audio API (procedural)               |

### Stack

```
Renderer      — Three.js r162 (ES modules, CDN unpkg)
Code          — ES modules natifs (pas de bundler)
Tiles         — Python + Pillow (generation procedurale d'atlas PNG 128x128)
Sprites       — Gemini (LLM) + slicing Python, ou procedural Python
Maps          — JSON dans public/assets/maps/
Sauvegarde    — localStorage
```

---

## 2. Structure du projet

```
zombie-house/
├── index.html                              # HTML/CSS minimal + importmap Three.js
├── src/                                    # Code source ES modules
│   ├── main.js                             # Point d'entree, game loop
│   ├── state.js                            # Etat global, constantes, MAP, DECO, hash(), spawnZ()
│   ├── input.js                            # Clavier, joystick, touch, getMove()
│   ├── update.js                           # update(), collision, IA zombies, projectiles
│   ├── audio.js                            # Web Audio, musique procedurale, SFX
│   ├── map-loader.js                       # loadMapJSON(), parsing JSON
│   ├── hud.js                              # updateHUD(), overlay victoire/game over
│   └── renderer/
│       ├── ThreeRenderer.js                # Scene, camera, eclairage, fog, render()
│       ├── ground.js                       # Sol texture depuis atlas PNG
│       ├── walls.js                        # Murs 3D (exterieur pierre + interieur varie)
│       ├── doors.js                        # Portes 3D avec ouverture animee
│       ├── furniture.js                    # Escaliers 3D, chandeliers, meubles BoxGeometry
│       ├── trees.js                        # Foret (sapins, chenes, morts, buissons)
│       ├── water.js                        # Riviere animee, pont-levis
│       ├── characters.js                   # Joueur + zombies (sprite billboard)
│       ├── effects.js                      # Projectiles, particules, chauves-souris
│       └── torches.js                      # Torches murales avec PointLight
├── Design/
│   ├── Personnages/
│   │   ├── angel_monster.png               # Illustration menu
│   │   ├── angle_monster_vue_dessus.png
│   │   └── sprites/                        # Sorties brutes LLM
│   └── Maps/
│       └── level_1_entree_manoir.png       # Image de reference niveau 1
├── public/assets/
│   ├── sprites/
│   │   ├── heroes/angel-monster/           # idle/walk front+back PNG
│   │   └── enemies/zombie-normal/          # idle/walk front+back PNG
│   ├── tilesets/
│   │   ├── ground-atlas.png                # 9 sols (128x128 chacun)
│   │   ├── wall-front-atlas.png            # 9 variantes murs interieurs
│   │   ├── wall-top-atlas.png              # 9 variantes dessus murs
│   │   ├── wall-exterior-atlas.png         # 5 variantes pierre grise exterieur
│   │   ├── wall-exterior-top-atlas.png     # 5 variantes dessus exterieur
│   │   ├── wall-dest-atlas.png             # 3 murs destructibles
│   │   ├── door-atlas.png                  # 3 variantes de portes
│   │   ├── deco-atlas.png                  # 15 decorations
│   │   ├── bush.png                        # Buisson
│   │   ├── tree-pine.png                   # Sapin
│   │   ├── tree-oak.png                    # Chene
│   │   ├── tree-spooky.png                 # Arbre mort
│   │   ├── bush-thorny.png                 # Buisson epineux
│   │   ├── bush-fern.png                   # Fougere
│   │   ├── bush-dead.png                   # Buisson mort
│   │   └── furniture-*.png                 # Meubles individuels
│   └── maps/
│       ├── level-1.json                    # Map legacy (fallback)
│       └── level-1-manoir.json             # Niveau 1 complet (40x32, 7 pieces)
├── scripts/
│   ├── generate_tiles_hq.py                # Generateur atlas 128x128
│   ├── generate_zombie_sprites.py          # Sprites zombie proceduraux
│   └── slice_sprite.py                     # Decoupe sprites LLM
├── PRD.md
├── ARCH.md
├── epic_suivi.md
└── stories/
```

---

## 3. Systeme de modules ES

### Architecture modulaire

Le code est organise en modules ES natifs sans bundler. Three.js est charge via CDN avec un `importmap` dans index.html.

```
index.html
  └── <script type="module" src="src/main.js">

src/main.js           ← point d'entree, game loop
  ├── state.js        ← etat global (state, MAP, DECO, constantes, hash, spawnZ)
  ├── input.js        ← setupInput(), getMove()
  ├── update.js       ← update(), collision, IA, projectiles, triggers
  ├── audio.js        ← Web Audio, SFX proceduraux
  ├── map-loader.js   ← loadMapJSON()
  ├── hud.js          ← updateHUD(), overlay
  └── renderer/
      └── ThreeRenderer.js
          ├── ground.js       ← sol texture canvas depuis atlas
          ├── walls.js        ← murs BoxGeometry (exterieur + interieur)
          ├── doors.js        ← portes 3D animees
          ├── furniture.js    ← escaliers, chandeliers, meubles
          ├── trees.js        ← foret procedurale
          ├── water.js        ← riviere, pont-levis
          ├── characters.js   ← sprites billboard joueur/zombies
          ├── effects.js      ← projectiles, particules, chauves-souris
          └── torches.js      ← torches murales + PointLight
```

### Principes

- **state.js** est le hub central : tous les modules importent depuis ce fichier
- **Pas de dependances circulaires** : state.js n'importe rien
- **Mutabilite partagee** : variables `let` modifiees via fonctions setter
- **Renderer passe par reference** : update.js recoit le renderer via `setRenderer()`
- **Three.js via importmap** : `import * as THREE from 'three'` resout vers CDN

---

## 4. Rendu 3D Three.js

### 4.1 Camera

- `PerspectiveCamera` FOV ~50, au-dessus et derriere le joueur
- Suivi par interpolation lineaire (lerp)

### 4.2 Sol

- `PlaneGeometry` unique couvrant la map
- `CanvasTexture` generee en dessinant chaque tile depuis les atlas PNG
- Tiles eau peintes en noir (les water planes 3D couvrent par-dessus)

### 4.3 Murs

- BoxGeometry individuel par mur avec textures atlas sur chaque face
- Murs exterieurs : 5 variantes pierre grise coherente (`wall-exterior-atlas`)
- Murs interieurs : 9 variantes diversifiees (`wall-front-atlas`)
- Detection exterieur/interieur par position (perimetre rows/cols)

### 4.4 Portes

- Cadre en bois (2 montants + linteau) avec panneau PlaneGeometry texture
- Fermees par defaut, ouverture par action (espace/clic) quand le joueur est proche
- Le panneau pivote sur une charniere
- Grand porte d'entree : double battant avec texture `grand_door.png`

### 4.5 Meubles

- BoxGeometry avec texture atlas sur la face du dessus
- Escaliers 3D : marches individuelles, certaines cassees avec debris
- Chandeliers : TorusGeometry + bougies + PointLight, suspendus au plafond
- Hauteurs realistes par type (lit 0.35, etagere 0.8, armoire 0.9)

### 4.6 Foret exterieure

- 3 types d'arbres (sapin, chene, mort) + 4 types de buissons
- 2-4 sprites par tile pour densite, tailles variees
- Tint sombre (0x404838) pour ambiance nuit
- Filtrage : aucun arbre sur eau, murs, interieur, ou pres de l'entree

### 4.7 Ambiance nuit

- AmbientLight bleu sombre (0x283848)
- DirectionalLight clair de lune (0x7888a0)
- FogExp2 pour assombrir les distances
- Sol herbe nuit (vert tres fonce)
- Chauves-souris animees qui traversent la scene

### 4.8 Eau et pont

- PlaneGeometry par tile d'eau avec ondulation vertex sinusoidale
- Riviere/douves autour du manoir
- Pont-levis en bois avec planches et rambardes

### 4.9 Eclairage

- Torches fixees aux murs avec support 3D + flamme animee
- PointLight par torche (intensite 2.5, portee 8)
- Grosses torches d'entree (intensite 4.0, portee 12)
- Chandeliers avec PointLight (intensite 3.5-6.0)

### 4.10 Personnages

- Sprite billboard (toujours face camera) avec PNG sheets
- 4 sheets par personnage : idle-front, idle-back, walk-front, walk-back
- Direction trackee par flag `facingDown`
- Bob animation sinusoidal
- Ombre (CircleGeometry) + halo colore (vert joueur, rouge ennemi)

### 4.11 Effets

- Projectiles : SphereGeometry avec trail (spheres degressives)
- Particules : pool pre-alloue recycle
- Popups degats : Sprite avec CanvasTexture
- Destruction murs : petits cubes ejectes

---

## 5. Format des maps (JSON)

```json
{
  "name": "Manoir Hante - Etage 1",
  "cols": 40, "rows": 32,
  "ground": [[...32 rows of 40 values...]],
  "walls": {
    "indestructible": [[r,c], ...],
    "destructible": [[r,c], ...]
  },
  "doors": [[r,c], ...],
  "furniture": [
    {"type": "bed", "r": 7, "c": 5, "w": 2, "h": 1},
    {"type": "chandelier", "r": 21, "c": 20, "w": 1, "h": 1, "grand": true}
  ],
  "decorations": [
    {"type": "torch", "r": 5, "c": 4},
    {"type": "blood", "r": 13, "c": 6}
  ],
  "bushes": [[r,c], ...],
  "spawns": {
    "player": {"col": 20, "row": 26},
    "zombies": [{"col": 6, "row": 18, "type": "normal"}],
    "surprises": [{"col": 8, "row": 24, "type": "normal", "trigger": {"row": 20, "col": 8, "radius": 3}}],
    "boss": {"col": 34, "row": 9, "trigger": {"furniture": "wardrobe", "r": 8, "c": 33}}
  }
}
```

Types de sol (indices ground) : 0=herbe, 1=pierre, 2=terre, 3=gravier, 4=bois, 5=tapis, 6=eau, 7=porte, 8=carrelage, 9=tapis use

---

## 6. Pipeline d'assets

### 6.1 Tiles (Python + Pillow)

```
python scripts/generate_tiles_hq.py
→ ground-atlas.png (9 sols), wall-front-atlas.png (9 murs),
  wall-exterior-atlas.png (5 pierres grises), wall-dest-atlas.png (3 destructibles),
  door-atlas.png (3 portes), deco-atlas.png (15 decos),
  tree-*.png (3 arbres), bush-*.png (4 buissons), furniture-*.png (10 meubles)
```

### 6.2 Sprites personnages

```
1. Gemini (LLM) : personnage sur fond blanc
2. scripts/slice_sprite.py : suppression fond, detection frames, assembly PNG
3. Resultat : public/assets/sprites/heroes/angel-monster/*.png
```

### 6.3 Sprites zombies

```
python scripts/generate_zombie_sprites.py
→ public/assets/sprites/enemies/zombie-normal/*.png
```

---

## 7. Audio

Web Audio API native. Musique procedurale (oscillateurs). SFX proceduraux (frequences + durees).

```javascript
initAudio()     // cree AudioContext au premier input
sfxShoot()      // sine 800Hz + square 600Hz
sfxHit()        // sawtooth 200Hz
sfxZombieDie()  // sawtooth 150Hz + sine 100Hz
sfxPlayerHit()  // square 120Hz + sine 80Hz
sfxVictory()    // 3 notes montantes (C-E-G)
sfxGameOver()   // 3 notes descendantes
```

---

## 8. Sauvegarde

```javascript
const SaveManager = {
  KEY: 'zombie-house-save',
  defaultSave: () => ({
    points: 0,
    maxLevelUnlocked: 1,
    heroes: { 'angel-monster': { unlocked: true, level: 1 } },
    audio: { musicVolume: 0.4, sfxVolume: 0.7, muted: false },
  }),
  save(data) { localStorage.setItem(this.KEY, JSON.stringify(data)); },
  load() { return JSON.parse(localStorage.getItem(this.KEY)) || this.defaultSave(); },
};
```
