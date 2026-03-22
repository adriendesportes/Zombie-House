# STORY-002 : MVP jouable

**Epic** : MVP
**Statut** : DONE

---

## Objectif

Prototype jouable complet : deplacement, tir, zombies, points, victoire, game over, audio.

---

## Tout est fait

### Setup projet
- [x] Repo Git + GitHub prive
- [x] Structure dossiers
- [x] Scripts Python (venv + Pillow + scipy)

### Map
- [x] Map 28x22 tiles avec 5 zones
- [x] 9 types de tiles sol
- [x] Murs indestructibles (5 variantes)
- [x] Murs destructibles (3 variantes)
- [x] Portes (3 variantes)
- [x] Buissons, decorations (10 types)
- [x] Export JSON

### Player
- [x] Deplacement 8 directions
- [x] Collision murs/eau
- [x] Sprites front/back (idle + walk)
- [x] Direction tracking
- [x] Bob animation
- [x] Invincibilite temporaire (1s) + clignotement apres degat

### Input
- [x] ZQSD/WASD + fleches
- [x] Espace + clic pour tirer
- [x] Joystick tactile + bouton attaque

### Projectile
- [x] Auto-aim zombie le plus proche
- [x] Trainee, collision murs/destructibles/zombies
- [x] SFX tir

### Ennemis
- [x] Zombie Normal (hp:1, 10pts)
- [x] Zombie Moyen (hp:2, 20pts)
- [x] Zombie Rage (hp:3, 30pts)
- [x] Boss (hp:10, 50pts, plus gros)
- [x] IA poursuite, direction front/back, sprites
- [x] SFX mort zombie

### Systeme de points
- [x] +10/20/30/50 par zombie tue
- [x] Affichage "+X" en popup jaune
- [x] Compteur en haut a droite
- [x] -100 si rejouer apres game over

### Systeme de vie
- [x] 3 coeurs affiches
- [x] Degats au contact
- [x] SFX degat joueur
- [x] Invincibilite 1s + clignotement

### Conditions de fin
- [x] Victoire quand tous zombies tues (ecran vert + points + R pour recommencer)
- [x] Game Over quand 0 HP (ecran rouge + choix R=rejouer -100pts / M=menu)
- [x] SFX victoire et game over

### Audio
- [x] Web Audio API (procedural)
- [x] Musique ambient dark (oscillateurs en boucle)
- [x] SFX tir (sine+square)
- [x] SFX hit zombie (sawtooth)
- [x] SFX mort zombie (sawtooth+sine)
- [x] SFX degat joueur (square+sine)
- [x] SFX victoire (3 notes montantes)
- [x] SFX game over (3 notes descendantes)
- [x] Init au premier input (autoplay policy)

### Rendu 2D
- [x] 8 passes, Y-sort, extrusion murs, vignette
- [x] 5 variantes murs, 3 destructibles, 3 portes
- [x] Tiles HQ depuis atlas

### Rendu 3D
- [x] Three.js, camera perspective, atlas textures
- [x] Sprites billboard player + zombies
- [x] UI HTML overlay

### HUD
- [x] Joystick + bouton attaque
- [x] Compteur zombies
- [x] Coeurs
- [x] Points
- [x] Ecrans victoire / game over
