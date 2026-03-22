# STORY-002 : MVP jouable — Map de test avec gameplay minimal

**Epic** : MVP — Zombie House
**Priorité** : Haute
**Statut** : Backlog
**Dépendances** : STORY-001 (assets graphiques)

---

## Objectif

Créer une version jouable minimale : un personnage qui se déplace dans quelques pièces, tue des zombies, gagne des points. Pas besoin de menu complet ni d'amélioration — juste le gameplay core.

---

## Scope MVP de test

### Map de test : 3-4 pièces

Sous-ensemble du niveau 1 (Hall d'entrée du manoir) :

```
┌─────────────────────────────────┐
│         Salle de bain           │
│    (2 zombies normaux)          │
│                                 │
├────────┬──[porte]───────────────┤
│        │                        │
│ Vesti- │    Hall d'entrée       │
│ aire   │    (spawn joueur)      │
│        │    (3 zombies)         │
│        │                        │
├──[porte]┼──────────┬──[porte]───┤
│         │          │            │
│         │          │ Biblio-    │
│         │          │ thèque     │
│         │          │ (5 zombies │
│         │          │  + BOSS)   │
└─────────┴──────────┴────────────┘
```

- **Taille map** : ~20x30 tiles (64x64 px) = 1280x1920 px
- **4 pièces** : Hall d'entrée, Vestiaire, Salle de bain, Bibliothèque
- **3 portes** qui s'ouvrent au contact (simplifié, pas de bouton pour le MVP)
- **Murs** avec collisions
- **Meubles** (table, bibliothèque) comme obstacles avec collision

### Ennemis de test

| Type           | Quantité | Comportement MVP                      |
| -------------- | -------- | ------------------------------------- |
| Zombie Normal  | 10       | Marche vers le joueur quand il entre dans la pièce |
| Zombie Boss    | 1        | Dans la bibliothèque, plus de vie, même IA |

**Total points récoltables** : 10×10 + 1×50 = **150 points**

### Personnage jouable

- Angel Monster uniquement
- Déplacement 8 directions (joystick gauche / ZQSD)
- Attaque : lancer de bras (joystick droit / clic souris)
- Pas d'attaque spéciale dans le MVP
- 3 cœurs (6 demi-cœurs)

### UI minimale en jeu

- 3 cœurs en haut à gauche
- Points en haut à droite
- Joystick gauche (déplacement) — mobile uniquement
- Joystick droit (visée/tir) — mobile uniquement

---

## Tâches techniques

### T1 — Setup projet
- [ ] Init projet Vite + TypeScript + Phaser 3
- [ ] `npm create vite@latest` → template TypeScript
- [ ] `npm install phaser`
- [ ] Structure dossiers selon ARCH.md
- [ ] Config Phaser (390x844, Scale.FIT, Arcade Physics)
- [ ] Vérifier que le jeu tourne dans le navigateur (écran noir = OK)

### T2 — Scènes de base
- [ ] `BootScene` : affiche "Chargement..."
- [ ] `PreloadScene` : charge tous les assets
- [ ] `GameScene` : scène principale du jeu
- [ ] `HUDScene` : overlay UI (cœurs, points)
- [ ] Transition Boot → Preload → Game + HUD

### T3 — Tilemap et map de test
- [ ] Créer la map dans **Tiled Map Editor** (ou en code avec un tableau 2D)
- [ ] Layer "ground" : sols
- [ ] Layer "walls" : murs avec collision
- [ ] Layer "furniture" : meubles avec collision
- [ ] Layer "doors" : portes
- [ ] Layer "objects" : spawn points (joueur + zombies + boss)
- [ ] Charger la tilemap dans GameScene
- [ ] Caméra qui suit le joueur avec limites de map

### T4 — Player (Angel Monster)
- [ ] Classe `Player` extends `Phaser.Physics.Arcade.Sprite`
- [ ] Chargement sprite sheet idle/walk/attack
- [ ] Animation idle (4 frames, boucle)
- [ ] Animation walk (6 frames, change selon direction)
- [ ] Animation attack (4 frames, jouée au tir)
- [ ] Déplacement via InputManager (8 directions, vitesse 150 px/s)
- [ ] Collision avec les murs et meubles
- [ ] Hitbox ajustée (plus petite que le sprite)

### T5 — Input Manager
- [ ] Détection tactile vs desktop (auto)
- [ ] **Mobile** : 2 joysticks virtuels (VirtualJoystick plugin ou custom)
  - Gauche (bas-gauche écran) : déplacement
  - Droit (bas-droite écran) : visée, relâcher = tirer
- [ ] **Desktop** : ZQSD/WASD + souris + clic gauche
- [ ] Retourne `Vector2` normalisé pour mouvement et direction tir

### T6 — Projectile (Bras lancé)
- [ ] Classe `Projectile` extends `Phaser.Physics.Arcade.Sprite`
- [ ] Créé à la position du joueur, direction = visée
- [ ] Vitesse : 400 px/s
- [ ] Portée max : 5 tiles (320 px) → auto-destroy
- [ ] Animation vol (2 frames)
- [ ] Animation impact (3 frames) puis destroy
- [ ] Collision avec murs → destroy immédiat
- [ ] Collision avec ennemi → dégâts + destroy

### T7 — Ennemis (Zombie Normal)
- [ ] Classe `Enemy` extends `Phaser.Physics.Arcade.Sprite`
- [ ] Classe `ZombieNormal` extends `Enemy`
- [ ] IA simple : si joueur dans la même pièce → marche vers joueur
- [ ] Vitesse : 60 px/s
- [ ] PV : 1 (meurt en 1 coup)
- [ ] Animation walk, hit, death
- [ ] Collision avec murs (ne traverse pas)
- [ ] Au contact du joueur → inflige 0.5 cœur de dégât (cooldown 1s)
- [ ] À la mort → +10 points, animation death, puis suppression

### T8 — Zombie Boss (simplifié)
- [ ] Classe `ZombieBoss` extends `Enemy`
- [ ] Même IA que normal mais PV : 10, vitesse : 40 px/s
- [ ] Plus gros sprite (256x256)
- [ ] Dégât au contact : 1 cœur
- [ ] À la mort → +50 points
- [ ] Quand boss mort → condition de victoire

### T9 — Système de vie
- [ ] Player a `hp = 6` (3 cœurs × 2 demi-cœurs)
- [ ] Quand touché : `-1 hp` (zombie normal) ou `-2 hp` (boss)
- [ ] Invincibilité 1s après un coup (clignotement)
- [ ] `hp <= 0` → animation mort → écran simple "Game Over" avec bouton "Rejouer"
- [ ] Rejouer = recharger la GameScene, `-100 points`

### T10 — Système de points
- [ ] `PointsManager` : compteur global persistant en mémoire
- [ ] Affichage en temps réel dans le HUD
- [ ] Incrémenté quand un ennemi meurt

### T11 — Portes (simplifié)
- [ ] Tile "porte fermée" = collision active
- [ ] Quand joueur touche la porte → animation ouverture → collision désactivée
- [ ] La porte reste ouverte (pas de refermeture pour le MVP)

### T12 — Condition de victoire
- [ ] Quand tous les ennemis sont morts (compteur à 0) → écran "Victoire !"
- [ ] Bouton "Retour" (pour le MVP, pas de niveau suivant)
- [ ] Affiche les points gagnés dans le niveau

### T13 — Audio minimal
- [ ] AudioManager basique (play/stop music, play SFX)
- [ ] 1 musique de gameplay en boucle
- [ ] SFX : attaque, zombie mort, joueur touché, porte
- [ ] Gestion autoplay mobile (unlock au premier touch)

---

## Critères d'acceptation

- [ ] Le jeu se lance dans Chrome (Mac) et Safari (iPhone)
- [ ] Le joueur se déplace dans 4 pièces avec collisions murs/meubles
- [ ] Le joueur peut tirer et tuer des zombies
- [ ] Les zombies marchent vers le joueur et infligent des dégâts
- [ ] Les portes s'ouvrent
- [ ] Les cœurs diminuent quand le joueur est touché
- [ ] Les points s'affichent et augmentent quand un zombie meurt
- [ ] Game Over + Rejouer fonctionne
- [ ] Victoire quand tous les ennemis sont morts
- [ ] Le jeu est jouable au joystick (mobile) ET clavier/souris (desktop)
- [ ] Audio : musique + SFX de base fonctionnels

---

## Ce qui est HORS scope MVP

- Menu principal / sélection personnage
- Système d'amélioration
- Personnages 2 et 3
- Zombie Moyen et Zombie Fou de Rage
- Attaque spéciale niveau 11
- Spawns surprise (plafond/sol)
- Boutons/interrupteurs pour les portes
- Sauvegarde localStorage
- Niveaux 2 à 10
- Options volume
