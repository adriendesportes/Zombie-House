# STORY-002 : MVP jouable

**Epic** : MVP
**Statut** : DEV (en cours)

---

## Objectif

Prototype jouable : un personnage qui se deplace, tue des zombies, gagne des points. Deux renderers : Canvas 2D et Three.js.

---

## Fait

### Setup projet
- [x] Repo Git + GitHub prive (adriendesportes/Zombie-House)
- [x] Structure dossiers (Design/, public/assets/, scripts/, stories/)
- [x] Scripts Python (venv + Pillow + scipy)
- [x] Pas de bundler — fichiers HTML autonomes

### Map
- [x] Map 28x22 tiles (40x40px) avec 5 zones (exterieurs, hall, caves)
- [x] 9 types de tiles sol (herbe, pierre, terre, gravier, bois, tapis, eau, porte, mur)
- [x] Murs indestructibles (5 variantes visuelles)
- [x] Murs destructibles (3 variantes : caisse, tonneau, pierres)
- [x] Portes (3 variantes : arche, bois, grille)
- [x] Buissons
- [x] Decorations (10 types : os, cranes, fissures, sang, champignons, torches, toiles)
- [x] Export JSON (public/assets/maps/level-1.json)

### Player (Angel Monster)
- [x] Deplacement 8 directions (ZQSD + fleches)
- [x] Collision avec murs, meubles, eau
- [x] Animation idle/walk avec sprites front/back
- [x] Direction tracking (facingDown)
- [x] Bob animation (rebond vertical)

### Input
- [x] Clavier ZQSD/WASD + fleches
- [x] Espace pour tirer
- [x] Clic souris pour tirer
- [x] Joystick virtuel tactile (mobile)
- [x] Bouton attaque tactile (mobile)

### Projectile
- [x] Auto-aim vers zombie le plus proche
- [x] Trainee (trail)
- [x] Collision murs (rebond/destruction)
- [x] Collision murs destructibles (casse le mur + particules)
- [x] Collision zombies (degats + particules)

### Ennemis
- [x] Zombie Normal (hp:1, lent) avec sprites
- [x] Zombie Moyen (hp:2, moyen)
- [x] Zombie Rage (hp:3, rapide)
- [x] IA : suit le joueur, pathfinding basique
- [x] Direction tracking front/back
- [x] Degats au contact du joueur (cooldown)
- [x] 14 zombies repartis sur la map

### Systeme de vie
- [x] 3 coeurs (6 demi-coeurs) affiches
- [x] Degats au contact ennemi
- [x] Nombres de degats pop-up

### Rendu 2D (test-map.html)
- [x] 8 passes de rendu (sol > decos > ombres > Y-sort > projectiles > particules > popups > UI)
- [x] Y-sorting (personnages passent devant/derriere les murs)
- [x] Murs avec extrusion 3D (face dessus + face avant 14px)
- [x] 5 variantes murs, 3 variantes destructibles, 3 variantes portes
- [x] Vignette sombre
- [x] Hash deterministe pour variation visuelle par tile
- [x] Tiles sol ultra detaillees (brins d'herbe, cailloux, grain bois, motifs tapis...)

### Rendu 3D (test-map-3d.html)
- [x] Three.js (ES modules CDN)
- [x] PerspectiveCamera FOV 50, lerp follow
- [x] Sol avec CanvasTexture depuis atlas HQ
- [x] Murs textures depuis atlas (front + top)
- [x] Murs destructibles textures depuis atlas
- [x] Buissons billboard (bush.png)
- [x] Player = sprite billboard (4 sheets PNG)
- [x] Zombies = sprite billboard (4 sheets PNG)
- [x] AmbientLight + DirectionalLight + PointLights torches
- [x] Projectiles sphere + trail
- [x] Particules poolees
- [x] Degats popup Sprite
- [x] Ombres + halos sous personnages
- [x] UI HTML overlay

### UI
- [x] Joystick virtuel (bas gauche)
- [x] Bouton attaque avec viseur (bas droite)
- [x] Compteur zombies en haut
- [x] Coeurs du joueur

---

## Reste a faire (MVP)

- [ ] Systeme de points (compteur + affichage)
- [ ] Condition victoire (tous zombies tues -> ecran victoire)
- [ ] Condition mort (0 coeurs -> ecran game over avec choix rejouer/menu)
- [ ] Perte de 100 points si rejouer
- [ ] Audio minimal (1 musique gameplay + SFX attaque/zombie/degats)
- [ ] Boss de niveau 1 (1 par map, plus gros, plus de PV)
- [ ] Invincibilite temporaire apres degat (clignotement)
