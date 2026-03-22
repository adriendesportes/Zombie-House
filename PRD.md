# PRD — Zombie House

## 1. Vision

Zombie House est un jeu d'action top-down jouable sur smartphone (portrait) et Mac (navigateur). Le joueur incarne l'Angel Monster, un monstre gentil qui explore un manoir hanté et elimine des zombies a travers 10 niveaux de difficulte croissante. Le style visuel est inspire de Brawl Stars : couleurs saturees, contours epais noirs, proportions chibi.

---

## 2. Public cible

- Joueurs casual/mid-core mobile (13+)
- Fans de Brawl Stars, Archero, Vampire Survivors

---

## 3. Plateformes et compatibilite

| Plateforme    | Support              |
| ------------- | -------------------- |
| iOS (Safari)  | PWA / navigateur     |
| Android       | PWA / navigateur     |
| Mac           | Navigateur (Chrome, Safari) |

**Orientation** : Portrait uniquement.

---

## 4. Ecrans et navigation

```
[Ecran titre]
    └──> [Menu principal / Selection personnage]
              ├──> [Menu amelioration personnage]
              └──> [Selection niveau]
                        └──> [Jeu (gameplay)]
                                  ├──> [Ecran de mort : Rejouer / Menu]
                                  └──> [Ecran victoire : Niveau suivant / Menu]
```

---

## 5. Menu principal — Selection du personnage

- Affichage des **points totaux** du joueur en haut de l'ecran.
- 3 emplacements de personnages (extensible plus tard).
  - Personnage 1 : **Angel Monster** (debloque).
  - Personnage 2 : Verrouille (silhouette + "Bientot").
  - Personnage 3 : Verrouille (silhouette + "Bientot").
- Chaque personnage est affiche en **haute resolution** (illustration detaillee type menu Brawl Stars).
- Bouton **"Ameliorer"** sous chaque personnage debloque — ouvre le menu d'amelioration.
- Bouton **"Jouer"** — ouvre la selection de niveau.

---

## 6. Systeme d'amelioration

### 6.1 Niveaux et couts

| Niveau | Cout (points) | Effet                                      |
| ------ | ------------- | -------------------------------------------|
| 1      | Gratuit       | Stats de base                               |
| 2      | 200           | +Puissance, +Vie                            |
| 3      | 300           | +Puissance, +Vie                            |
| 4      | 400           | +Puissance, +Vie                            |
| 5      | 500           | +Puissance, +Vie                            |
| 6      | 600           | +Puissance, +Vie                            |
| 7      | 700           | +Puissance, +Vie                            |
| 8      | 800           | +Puissance, +Vie                            |
| 9      | 900           | +Puissance, +Vie                            |
| 10     | 1000          | +Puissance, +Vie                            |
| 11     | 1100          | **Pouvoir secret** + stats max              |

**Cout total pour atteindre le niveau 11** : 6 500 points.

### 6.2 Regles

- Progression sequentielle uniquement (2 → 3 → 4, pas de saut).
- Les points depenses sont **consommes** (deduits du total).

---

## 7. Personnages (Heros)

### 7.1 Angel Monster

- **Apparence** : Monstre avec armure bleue, casque de pirate en verre, 4 bras, ailes d'energie cyan, levite au-dessus du sol, queue en trident. Proportions chibi (tete = 40-50% du corps).
- **Sprites en jeu** : 4 sprite sheets PNG (idle-front, idle-back, walk-front, walk-back). Direction determinee par le flag `facingDown`.
- **Attaque principale** : Lance un de ses bras comme projectile en ligne droite. Portee limitee (~5 tiles). Pas de cooldown. Auto-vise le zombie le plus proche.
- **Attaque speciale (niveau 11)** : La queue forme une boule d'electricite projetee devant lui — explosion de zone detruisant tous les ennemis dans le rayon. Cooldown : 15 secondes.

### 7.2 Personnage 2 — A definir

### 7.3 Personnage 3 — A definir

---

## 8. Ennemis

| Type               | Points | PV   | Degats    | Vitesse   | Comportement                         |
| ------------------ | ------ | ---- | --------- | --------- | ------------------------------------ |
| Zombie Normal      | 10     | 1    | 0.5 coeur | Lent      | Marche vers le joueur                |
| Zombie Moyen       | 20     | 2    | 0.5 coeur | Moyen     | Marche + esquive legere              |
| Zombie Fou de Rage | 30     | 3    | 1 coeur   | Rapide    | Charge en ligne droite               |
| Zombie Boss        | 50     | 10+  | 1 coeur   | Moyen     | Patterns d'attaque, 1 par map        |

- Chaque map contient **20 a 30 zombies** (hors boss).
- Les zombies peuvent apparaitre par **surprise** : tombant du plafond, surgissant du sol, derriere des portes.
- Proportions chibi, style cartoon Brawl Stars.

---

## 9. Systeme de vie du heros

- **3 coeurs** (6 demi-coeurs).
- Chaque coup recu = **-0.5 coeur** (zombie normal/moyen) ou **-1 coeur** (fou de rage/boss).
- **A la mort** :
  - Choix : **Rejouer** ou **Retour au menu**.
  - Si rejouer : reprise au point de mort, **-100 points**.
  - Si retour au menu : le niveau est remis a zero, points conserves.

---

## 10. Systeme de points

### 10.1 Gains

| Source             | Points |
| ------------------ | ------ |
| Zombie Normal      | 10     |
| Zombie Moyen       | 20     |
| Zombie Fou de Rage | 30     |
| Zombie Boss        | 50     |

### 10.2 Pertes

| Action                  | Points |
| ----------------------- | ------ |
| Mort + choix "Rejouer"  | -100   |

### 10.3 Utilisation

Les points sont la **monnaie unique** pour ameliorer les personnages dans le menu principal.

---

## 11. Maps / Niveaux

### 11.1 Structure

- **10 niveaux** au total, progression lineaire (finir N pour debloquer N+1).
- Chaque niveau = une zone du manoir (hall, cuisine, bibliotheque, cave, grenier, jardin, etc.).
- Grille de tiles carres 40x40 px, vue top-down avec pseudo-3D (extrusion de murs).
- La camera suit le joueur avec defilement vertical (portrait).

### 11.2 Elements de map

| Element            | Interaction                                              |
| ------------------ | -------------------------------------------------------- |
| Murs               | Collision — bloquent joueur et projectiles               |
| Portes             | S'ouvrent en interagissant avec un interrupteur nearby   |
| Zones de spawn     | Zombies apparaissent (plafond, sol, derriere des objets) |
| Meubles/Decors     | Collision — elements decoratifs non traversables         |
| Buissons           | Sprite individuel avec Y-sorting, semi-obstacle          |
| Murs destructibles | Peuvent etre detruits par les projectiles                |
| Sol traversable    | Zones de deplacement libre                               |

### 11.3 Niveau 1 — Hall d'entree du manoir

Base sur l'image `Design/Maps/level_1_entree_manoir.png` :
- Pieces : Hall d'entree, Vestiaire, Bibliotheque, Salle de bain, Cuisine, Chambre de la Nourrice, Chambre d'Amis.
- Ambiance sombre, eclairage aux bougies, meubles renverses.
- ~20 zombies normaux + 1 boss.

### 11.4 Difficulte progressive

| Niveau | Zombies normaux | Zombies moyens | Fous de rage | Boss | Points max estimes |
| ------ | --------------- | -------------- | ------------ | ---- | ------------------ |
| 1      | 20              | 0              | 0            | 1    | 250                |
| 2      | 15              | 5              | 0            | 1    | 300                |
| 3      | 10              | 10             | 2            | 1    | 410                |
| 4      | 8               | 10             | 5            | 1    | 480                |
| 5      | 5               | 10             | 8            | 1    | 540                |
| 6      | 5               | 8              | 10           | 1    | 560                |
| 7      | 3               | 8              | 12           | 1    | 600                |
| 8      | 2               | 5              | 15           | 1    | 620                |
| 9      | 0               | 5              | 18           | 1    | 690                |
| 10     | 0               | 3              | 20           | 1    | 710                |

---

## 12. Controles

### Smartphone (tactile)

- **Joystick virtuel gauche** : Deplacement 8 directions.
- **Bouton attaque (droit)** : Tir auto-vise (zombie le plus proche).
- **Bouton special** (niveau 11) : Declenche le pouvoir secret.

### Mac (clavier + souris)

- **ZQSD / WASD** : Deplacement.
- **Espace / Clic gauche** : Tir (auto-vise le zombie le plus proche).
- **Espace** : Pouvoir special (niveau 11).

---

## 13. Style visuel

### 13.1 Grille et rendu

- Grille carree de **tiles 40x40 px** (pas de projection isometrique).
- Les murs ont une **hauteur visible** : face superieure (40x40 px) + face avant (40x14 px) s'etendant sous la tile.
- **Y-sorting** : toutes les entites (murs, buissons, personnages) sont triees par coordonnee Y pour simuler la profondeur.
- **8 passes de rendu** (ordre strict) :
  1. Sol (ground)
  2. Decorations au sol
  3. Ombres des murs
  4. Entites Y-triees (murs, buissons, personnages)
  5. Projectiles
  6. Particules
  7. Popups de degats
  8. UI

### 13.2 Style cartoon

- Couleurs saturees, contours noirs epais, cel-shading.
- Proportions chibi : tete = 40-50% de la hauteur totale du personnage.
- Style Brawl Stars : lisible, contrastee, sans realisme.

### 13.3 Sprites personnages (en jeu)

```
Sprite sheets PNG, fond transparent
Proportions chibi (tete = 40-50% du corps)
Animations requises par personnage :
  - idle-front  (4 frames)
  - idle-back   (4 frames)
  - walk-front  (6 frames)
  - walk-back   (6 frames)
Taille des frames : 128x128 px (HQ source), redimensionne selon usage
```

### 13.4 Sprites ennemis (en jeu)

```
Memes specs que les heros jouables.
Types a generer :
  - Zombie normal    : humanoide decompose, lent, verdatre
  - Zombie moyen     : plus grand, vetements dechires, yeux rouges
  - Zombie fou de rage : musculature grotesque, machoire decrochee, aura rouge
  - Zombie boss      : geant (frames 256x256 px), unique par niveau, detaille
```

### 13.5 Tiles de map

```
Generees par script Python (Pillow) en 128x128 px dans des atlas PNG.
Atlas disponibles :
  - ground-atlas.png       : 7 types de sol (herbe, pierre, terre, gravier, bois, moquette, eau)
  - wall-front-atlas.png   : 5 variants de face avant de mur
  - wall-top-atlas.png     : 5 variants de face superieure (correspondant aux fronts)
  - wall-dest-atlas.png    : 3 murs destructibles (caisse bois, tonneau, pierres empilees)
  - door-atlas.png         : 3 variants de portes
  - deco-atlas.png         : 10 types de decors (os, crane, fissure, toile, sang, etc.)
  - bush.png               : sprite de buisson individuel

Style : manoir hante, cartoon sombre (Brawl Stars)
Palette : tons sombres (brun, gris, violet fonce) + accents lumineux (bougies orange, lueur verte/bleue)
Variation deterministe par position via hash (pas de Math.random)
```

---

## 14. Audio

### 14.1 Sources gratuites recommandees

| Bibliotheque                   | URL                          | Licence           | Contenu principal                |
| ------------------------------ | ---------------------------- | ----------------- | -------------------------------- |
| **Freesound.org**              | freesound.org                | CC0 / CC-BY       | SFX varies, bruitages            |
| **OpenGameArt.org**            | opengameart.org              | CC0 / CC-BY       | SFX + musiques pour jeux         |
| **Mixkit**                     | mixkit.co/free-sound-effects | Libre de droits   | SFX haute qualite                |
| **Pixabay Music**              | pixabay.com/music            | Libre de droits   | Musiques d'ambiance              |
| **Kevin MacLeod (Incompetech)**| incompetech.com              | CC-BY 3.0         | Musiques horreur/ambiance        |

### 14.2 Musiques (boucles)

| Contexte                  | Style                                           | Format        |
| ------------------------- | ----------------------------------------------- | ------------- |
| Menu principal            | Ambiance mysterieuse, piano sombre, calme        | MP3, boucle   |
| En jeu (exploration)      | Tension basse, cordes, ambiance manoir hante     | MP3, boucle   |
| En jeu (combat intense)   | Rythme rapide, percussions, urgence              | MP3, boucle   |
| Boss                      | Epique sombre, cuivres, montee dramatique        | MP3, boucle   |
| Victoire                  | Fanfare courte, triomphale                       | MP3, one-shot |
| Mort / Game Over          | Melancolique, court, descendant                  | MP3, one-shot |

### 14.3 Effets sonores (SFX)

| Evenement                     | Description sonore                            |
| ----------------------------- | --------------------------------------------- |
| **Joueur**                    |                                               |
| Pas du joueur                 | Pas sur bois / pierre (selon le sol)          |
| Attaque (lancer de bras)      | Whoosh mecanique                              |
| Attaque speciale (electricite)| Charge electrique + explosion                 |
| Degat recu                    | Impact + cri de douleur court                 |
| Mort du joueur                | Chute + son dramatique                        |
| **Ennemis**                   |                                               |
| Grognement zombie (idle)      | Grognement sourd, aleatoire                   |
| Zombie apparition surprise    | Son de chute / craquement + cri               |
| Zombie touche                 | Impact chair, splash                          |
| Zombie mort                   | Effondrement + gemissement                    |
| Boss rugissement              | Rugissement grave, puissant                   |
| **Environnement**             |                                               |
| Porte qui s'ouvre             | Grincement bois / metal                       |
| Bouton / interrupteur         | Clic mecanique                                |
| Ambiance manoir               | Craquements, vent, horloge (subtil, en fond)  |
| **UI**                        |                                               |
| Clic bouton menu              | Pop / clic satisfaisant                       |
| Amelioration personnage       | Jingle positif + effet de power-up            |
| Niveau debloque               | Fanfare courte                                |
| Points gagnes                 | Tintement de piece (leger)                    |

### 14.4 Specifications techniques

- **Format** : MP3 (compatibilite maximale web) + OGG en fallback.
- **Musiques** : 128 kbps, stereo, normalisees a -14 LUFS.
- **SFX** : 44.1 kHz, mono, normalises, duree < 2 secondes (sauf ambiance).
- **Taille cible** : musiques < 2 Mo chacune, SFX < 100 Ko chacun.
- **Volume par defaut** : Musique 0.4, SFX 0.7 (ajustable dans les options).
- **Crossfade contextuel** : exploration → combat → boss selon la proximite des ennemis.
- **Autoplay mobile** : l'audio est debloque au premier touch de l'utilisateur.

---

## 15. Sauvegarde

- **Locale** (localStorage / IndexedDB) :
  - Points totaux
  - Niveau max debloque
  - Niveau de chaque personnage
  - Personnages debloques
  - **Volume musique** (0.0 – 1.0)
  - **Volume SFX** (0.0 – 1.0)
  - **Mute** (on/off)

---

## 16. Roadmap

| Phase | Contenu                                                  |
| ----- | -------------------------------------------------------- |
| MVP   | Angel Monster + Niveau 1 + Menu + Amelioration + Audio   |
| V1.1  | Niveaux 2-5                                              |
| V1.2  | Personnage 2 + Niveaux 6-8                               |
| V1.3  | Personnage 3 + Niveaux 9-10                              |
| V2.0  | Multijoueur ? Evenements ? Leaderboard ?                 |
