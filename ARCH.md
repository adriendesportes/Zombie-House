# Architecture — Zombie House

## 1. Choix technologique

### Framework : Phaser 3 (TypeScript)

| Critère                | Phaser 3                                      |
| ---------------------- | --------------------------------------------- |
| Multi-plateforme       | Web = fonctionne partout (iOS, Android, Mac)  |
| Vue isométrique        | Plugin isométrique natif + tilemap support     |
| Performance mobile     | WebGL + fallback Canvas                        |
| Sprites / Animations   | Sprite sheets, atlas, animations intégrées     |
| Physique               | Arcade Physics (léger, suffisant pour top-down)|
| Tilemap                | Support natif Tiled JSON                       |
| Communauté             | Large, bien documenté                          |
| Déploiement            | Static hosting (Vercel, Netlify, GitHub Pages) |

### Stack complet

```
Phaser 3          — moteur de jeu
TypeScript        — typage, maintenabilité
Vite              — bundler (dev rapide, HMR)
Tiled Map Editor  — création des maps (export JSON)
localStorage      — sauvegarde locale
PWA (optionnel)   — installation mobile
```

---

## 2. Structure du projet

```
zombie-house/
├── Design/
│   ├── Personnages/          # Illustrations haute résolution
│   └── Maps/                 # Images de référence des maps
├── public/
│   └── assets/
│       ├── sprites/
│       │   ├── heroes/
│       │   │   └── angel-monster/
│       │   │       ├── idle.png
│       │   │       ├── walk.png
│       │   │       ├── attack.png
│       │   │       └── special.png
│       │   └── enemies/
│       │       ├── zombie-normal.png
│       │       ├── zombie-medium.png
│       │       ├── zombie-rage.png
│       │       └── bosses/
│       ├── tilesets/
│       │   └── manor-tileset.png
│       ├── maps/
│       │   ├── level-1.json        # Export Tiled
│       │   └── level-1-collision.json
│       ├── ui/
│       │   ├── joystick-base.png
│       │   ├── joystick-thumb.png
│       │   ├── heart-full.png
│       │   ├── heart-half.png
│       │   ├── heart-empty.png
│       │   └── buttons/
│       └── audio/
│           ├── music/
│           │   ├── menu-theme.mp3
│           │   ├── gameplay-exploration.mp3
│           │   ├── gameplay-combat.mp3
│           │   ├── boss-fight.mp3
│           │   ├── victory.mp3
│           │   └── game-over.mp3
│           └── sfx/
│               ├── player-footstep-wood.mp3
│               ├── player-footstep-stone.mp3
│               ├── player-attack-whoosh.mp3
│               ├── player-special-electric.mp3
│               ├── player-hit.mp3
│               ├── player-death.mp3
│               ├── zombie-groan.mp3
│               ├── zombie-spawn-surprise.mp3
│               ├── zombie-hit.mp3
│               ├── zombie-death.mp3
│               ├── boss-roar.mp3
│               ├── door-creak.mp3
│               ├── button-click.mp3
│               ├── ambiance-manor.mp3
│               ├── ui-click.mp3
│               ├── ui-upgrade.mp3
│               ├── ui-level-unlock.mp3
│               └── ui-points.mp3
├── src/
│   ├── main.ts               # Point d'entrée Phaser
│   ├── config.ts             # Configuration Phaser (résolution, physique)
│   ├── scenes/
│   │   ├── BootScene.ts      # Chargement initial
│   │   ├── PreloadScene.ts   # Chargement des assets
│   │   ├── MenuScene.ts      # Menu principal + sélection perso
│   │   ├── UpgradeScene.ts   # Menu d'amélioration
│   │   ├── LevelSelectScene.ts
│   │   ├── GameScene.ts      # Gameplay principal
│   │   ├── HUDScene.ts       # UI en jeu (cœurs, points, joystick)
│   │   ├── DeathScene.ts     # Écran de mort
│   │   └── VictoryScene.ts   # Écran de victoire
│   ├── entities/
│   │   ├── Player.ts         # Classe joueur (hérite de Phaser.GameObjects.Sprite)
│   │   ├── Enemy.ts          # Classe ennemi de base
│   │   ├── ZombieNormal.ts
│   │   ├── ZombieMedium.ts
│   │   ├── ZombieRage.ts
│   │   ├── ZombieBoss.ts
│   │   └── Projectile.ts    # Bras projeté, boule d'électricité
│   ├── heroes/
│   │   ├── HeroBase.ts       # Classe abstraite héros
│   │   └── AngelMonster.ts   # Implémentation Angel Monster
│   ├── systems/
│   │   ├── InputManager.ts   # Joystick virtuel + clavier/souris
│   │   ├── CollisionManager.ts
│   │   ├── SpawnManager.ts   # Gestion des vagues de zombies
│   │   ├── PointsManager.ts  # Score et économie
│   │   ├── AudioManager.ts   # Musique + SFX + volume
│   │   └── SaveManager.ts    # localStorage
│   ├── ui/
│   │   ├── VirtualJoystick.ts
│   │   ├── HealthBar.ts
│   │   └── PointsDisplay.ts
│   ├── data/
│   │   ├── heroes.ts         # Config des héros (stats par niveau)
│   │   ├── enemies.ts        # Config des ennemis
│   │   └── levels.ts         # Config des niveaux (ennemis, spawn points)
│   └── utils/
│       └── constants.ts
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── PRD.md
└── ARCH.md
```

---

## 3. Configuration Phaser

```typescript
// src/config.ts
const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,              // WebGL avec fallback Canvas
  width: 390,                     // iPhone 14 width (portrait)
  height: 844,                    // iPhone 14 height (portrait)
  scale: {
    mode: Phaser.Scale.FIT,       // S'adapte à l'écran
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: 0 },   // Top-down, pas de gravité
      debug: false,
    },
  },
  scene: [BootScene, PreloadScene, MenuScene, UpgradeScene,
          LevelSelectScene, GameScene, HUDScene, DeathScene, VictoryScene],
};
```

---

## 4. Architecture des entités

### 4.1 Hiérarchie des classes

```
Phaser.GameObjects.Sprite
├── Player (HeroBase)
│   └── AngelMonster
│       ├── stats: { hp, power, level }
│       ├── attack()         → lance un bras (Projectile)
│       └── specialAttack()  → boule d'électricité (si level 11)
├── Enemy
│   ├── ZombieNormal    → suit le joueur, lent
│   ├── ZombieMedium    → suit + esquive
│   ├── ZombieRage      → charge en ligne droite
│   └── ZombieBoss      → patterns d'attaque uniques
└── Projectile
    ├── ArmProjectile       → ligne droite, portée limitée
    └── ElectricBall        → AoE explosion à l'impact
```

### 4.2 Stats des héros par niveau

```typescript
// src/data/heroes.ts
export const ANGEL_MONSTER = {
  name: 'Angel Monster',
  baseStats: {
    hp: 6,          // 3 cœurs = 6 demi-cœurs
    power: 1,       // Dégâts de base
    speed: 150,     // px/sec
    attackRange: 5,  // tiles
  },
  levelMultipliers: {
    // Chaque niveau augmente power de +10% et hp de +1 demi-cœur
    power: 0.10,
    hp: 1,
  },
  specialAttack: {
    unlockLevel: 11,
    cooldown: 15000,  // ms
    radius: 3,        // tiles
    damage: 999,      // one-shot tout
  },
  upgradeCosts: [0, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100],
};
```

---

## 5. Système de map (Dual-Layer)

### 5.1 Pipeline de création d'une map

```
1. Image de référence (LLM)     →  Design/Maps/level_X.png
2. Ouvrir dans Tiled Map Editor  →  Créer la tilemap
3. Layer "ground"                →  Tiles de sol (visuel)
4. Layer "walls"                 →  Tiles de murs (collision)
5. Layer "decoration"            →  Meubles, objets (certains avec collision)
6. Layer "objects"               →  Spawn points, portes, triggers
7. Export JSON                   →  public/assets/maps/level-X.json
```

### 5.2 Format Tiled

```json
{
  "width": 30,
  "height": 50,
  "tilewidth": 64,
  "tileheight": 64,
  "layers": [
    { "name": "ground", "type": "tilelayer", "data": [...] },
    { "name": "walls", "type": "tilelayer", "data": [...] },
    { "name": "decoration", "type": "tilelayer", "data": [...] },
    {
      "name": "objects", "type": "objectgroup",
      "objects": [
        { "name": "player_spawn", "x": 192, "y": 2800 },
        { "name": "zombie_spawn", "type": "zombie_normal", "x": 500, "y": 400 },
        { "name": "door", "x": 320, "y": 600, "properties": { "trigger": "button_1" } },
        { "name": "surprise_spawn", "type": "zombie_rage", "x": 700, "y": 300,
          "properties": { "trigger": "proximity", "animation": "fall_ceiling" } }
      ]
    }
  ]
}
```

### 5.3 Specs techniques pour générer les images de map

Pour demander à un LLM de générer les visuels de map compatibles avec le jeu :

```
TILESET (à générer une seule fois, réutilisé pour toutes les maps) :
- Format : PNG, grille de tiles 64x64 px
- Vue : isométrique ~30° surélevée
- Style : manoir hanté, cartoon sombre (Brawl Stars)
- Contenu requis :
  Row 1 : sols (parquet clair, parquet sombre, pierre, terre, herbe, carrelage)
  Row 2 : murs (brique N, brique S, brique E, brique O, coin NE, coin NO, coin SE, coin SO)
  Row 3 : portes (fermée N/S, fermée E/O, ouverte N/S, ouverte E/O)
  Row 4 : meubles (table, chaise, lit, bibliothèque, coffre, canapé)
  Row 5 : décors (chandelier, tableau, tapis, plante morte, toile d'araignée)
  Row 6 : escaliers (montée, descente), trappe sol, trou plafond
- Palette : tons sombres (brun, gris, violet foncé) + accents lumineux (bougies orange, lueur verte/bleue)
- Pas de fond (transparent)
- Cohérence de style entre toutes les tiles

IMAGE DE RÉFÉRENCE PAR NIVEAU (pour le level design) :
- Format : PNG, 1920x1080 px minimum
- Vue : isométrique identique au tileset
- Contenu : vue complète du niveau avec toutes les pièces visibles
- Labels texte sur chaque pièce (comme level_1_entree_manoir.png)
- Cette image sert de GUIDE pour placer les tiles dans Tiled, pas d'asset in-game
```

---

## 6. Système d'input (mobile + desktop)

```typescript
// src/systems/InputManager.ts
class InputManager {
  private joystickMove: VirtualJoystick;   // Joystick gauche
  private joystickAim: VirtualJoystick;    // Joystick droit (tir)
  private keys: Phaser.Input.Keyboard.CursorKeys;
  private mouse: Phaser.Input.Pointer;

  getMovement(): Phaser.Math.Vector2 {
    // Mobile : joystick gauche
    // Desktop : ZQSD/WASD
    // Retourne vecteur direction normalisé
  }

  getAimDirection(): Phaser.Math.Vector2 {
    // Mobile : joystick droit (direction au relâchement = tir)
    // Desktop : direction vers curseur souris
  }

  isAttacking(): boolean {
    // Mobile : relâchement joystick droit
    // Desktop : clic gauche
  }

  isSpecialAttack(): boolean {
    // Mobile : bouton spécial
    // Desktop : espace
  }
}
```

---

## 7. Game loop (GameScene)

```
update(time, delta):
  1. InputManager.getMovement()     → déplacer le joueur
  2. InputManager.getAimDirection() → orienter le joueur
  3. Si isAttacking()               → créer Projectile
  4. Si isSpecialAttack() + lvl 11  → créer ElectricBall
  5. Pour chaque Enemy:
       - AI : pathfinding vers joueur
       - Zombies surprise : vérifier trigger proximity
  6. CollisionManager.check()
       - Projectile vs Enemy → dégâts, points
       - Enemy vs Player     → perte de vie
       - Player vs Walls     → bloquer
       - Player vs Door      → ouvrir si bouton activé
  7. SpawnManager.update()          → spawns programmés
  8. Vérifier victoire (tous ennemis tués)
  9. Vérifier mort (0 cœurs)
  10. HUDScene.update()             → afficher cœurs, points
```

---

## 8. Sauvegarde

```typescript
// src/systems/SaveManager.ts
interface SaveData {
  points: number;
  maxLevelUnlocked: number;
  heroes: {
    [heroId: string]: {
      unlocked: boolean;
      level: number;       // 1-11
    };
  };
  audio: {
    musicVolume: number;   // 0.0 – 1.0, défaut 0.4
    sfxVolume: number;     // 0.0 – 1.0, défaut 0.7
    muted: boolean;
  };
}

class SaveManager {
  private static KEY = 'zombie-house-save';

  static save(data: SaveData): void {
    localStorage.setItem(this.KEY, JSON.stringify(data));
  }

  static load(): SaveData {
    const raw = localStorage.getItem(this.KEY);
    if (!raw) return this.defaultSave();
    return JSON.parse(raw);
  }

  private static defaultSave(): SaveData {
    return {
      points: 0,
      maxLevelUnlocked: 1,
      heroes: {
        'angel-monster': { unlocked: true, level: 1 },
        'hero-2': { unlocked: false, level: 1 },
        'hero-3': { unlocked: false, level: 1 },
      },
    };
  }
}
```

---

## 9. Système audio (AudioManager)

### 9.1 Architecture

```typescript
// src/systems/AudioManager.ts
class AudioManager {
  private scene: Phaser.Scene;
  private currentMusic: Phaser.Sound.BaseSound | null;
  private ambianceLoop: Phaser.Sound.BaseSound | null;
  private musicVolume: number;  // 0.0 – 1.0
  private sfxVolume: number;    // 0.0 – 1.0
  private muted: boolean;

  // Musique — une seule piste active à la fois, crossfade entre pistes
  playMusic(key: string, loop?: boolean): void;
  stopMusic(fadeOut?: number): void;
  crossfadeTo(key: string, duration?: number): void;

  // SFX — fire-and-forget, supporte plusieurs sons simultanés
  playSFX(key: string, config?: { volume?: number, rate?: number }): void;

  // Ambiance — boucle indépendante de la musique (craquements manoir)
  startAmbiance(key: string): void;
  stopAmbiance(): void;

  // Volume
  setMusicVolume(vol: number): void;
  setSFXVolume(vol: number): void;
  toggleMute(): void;
}
```

### 9.2 Déclenchement contextuel

```
GameScene.update():
  - Aucun ennemi à proximité     → crossfade vers "gameplay-exploration"
  - Ennemi à < 5 tiles           → crossfade vers "gameplay-combat"
  - Boss spawn                   → crossfade vers "boss-fight"
  - Victoire                     → stopMusic + play "victory"
  - Mort                         → stopMusic + play "game-over"

SpawnManager:
  - Zombie surprise              → playSFX("zombie-spawn-surprise")
  - Boss apparition              → playSFX("boss-roar")

CollisionManager:
  - Projectile hit enemy         → playSFX("zombie-hit")
  - Enemy killed                 → playSFX("zombie-death")
  - Player hit                   → playSFX("player-hit")
  - Player death                 → playSFX("player-death")

Player.update():
  - En mouvement                 → playSFX("footstep-wood") tous les 0.3s
  - Attaque                      → playSFX("player-attack-whoosh")
  - Attaque spéciale             → playSFX("player-special-electric")

Door interaction:
  - Ouverture                    → playSFX("door-creak")
  - Bouton pressé                → playSFX("button-click")
```

### 9.3 Gestion mobile (autoplay policy)

Les navigateurs mobiles bloquent l'audio avant une interaction utilisateur. Solution :
```typescript
// Dans BootScene ou au premier touch
this.input.once('pointerdown', () => {
  this.sound.unlock();  // Phaser gère le déblocage WebAudio
});
```

### 9.4 Chargement des assets audio

```typescript
// PreloadScene.ts
// Musiques (streaming pour réduire la mémoire)
this.load.audio('music-menu', 'assets/audio/music/menu-theme.mp3');
this.load.audio('music-exploration', 'assets/audio/music/gameplay-exploration.mp3');
this.load.audio('music-combat', 'assets/audio/music/gameplay-combat.mp3');
this.load.audio('music-boss', 'assets/audio/music/boss-fight.mp3');
this.load.audio('sfx-victory', 'assets/audio/music/victory.mp3');
this.load.audio('sfx-gameover', 'assets/audio/music/game-over.mp3');

// SFX (chargés en mémoire, petits fichiers)
this.load.audio('sfx-footstep-wood', 'assets/audio/sfx/player-footstep-wood.mp3');
this.load.audio('sfx-attack', 'assets/audio/sfx/player-attack-whoosh.mp3');
this.load.audio('sfx-special', 'assets/audio/sfx/player-special-electric.mp3');
// ... etc.
```

---

## 10. Responsive et adaptation écran

```
Résolution de base : 390 x 844 (iPhone 14, portrait)
Mode de scaling : Phaser.Scale.FIT
Centre : AUTO_CENTER

Sur Mac (navigateur) :
  - Le jeu s'affiche centré dans la fenêtre
  - Barres noires latérales si ratio différent
  - Joysticks masqués, contrôles clavier/souris activés

Sur tablette :
  - Scale FIT avec le même ratio portrait
```

---

## 11. Pipeline de développement

```
Phase 1 — Fondations (MVP)
  ├── Setup projet (Vite + Phaser + TypeScript)
  ├── Scènes de base (Boot, Preload, Menu, Game)
  ├── Player (Angel Monster) + mouvement + attaque
  ├── Joystick virtuel
  ├── 1 ennemi (Zombie Normal) avec IA basique
  ├── Collision murs + tilemap niveau 1
  ├── Système de vie (cœurs)
  ├── Système de points
  ├── AudioManager + musique menu + musique gameplay
  └── SFX de base (attaque, zombie hit/death, pas)

Phase 2 — Complet
  ├── Menu amélioration + système de niveaux
  ├── 4 types de zombies
  ├── Spawns surprise + SFX surprise
  ├── Portes + boutons + SFX interactions
  ├── Écrans mort / victoire + jingles
  ├── Sauvegarde localStorage (+ prefs audio)
  ├── Attaque spéciale niveau 11 + SFX électricité
  ├── Crossfade musique contextuel (exploration/combat/boss)
  └── Options volume (musique / SFX / mute)

Phase 3 — Contenu
  ├── 10 maps complètes
  ├── Personnages 2 et 3
  ├── Ambiance sonore par type de salle
  └── Polish (animations, effets, sons additionnels)
```
