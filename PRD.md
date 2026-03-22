# PRD — Zombie House

## 1. Vision

Zombie House est un jeu d'action top-down en vue isométrique légèrement surélevée (style Brawl Stars), jouable sur smartphone (portrait) et Mac (navigateur). Le joueur incarne un monstre gentil qui explore un manoir hanté et élimine des zombies à travers 10 niveaux de difficulté croissante.

---

## 2. Public cible

- Joueurs casual/mid-core mobile (13+)
- Fans de Brawl Stars, Archero, Vampire Survivors

---

## 3. Plateformes et compatibilité

| Plateforme    | Support              |
| ------------- | -------------------- |
| iOS (Safari)  | PWA / navigateur     |
| Android       | PWA / navigateur     |
| Mac           | Navigateur (Chrome, Safari) |

**Orientation** : Portrait uniquement.

---

## 4. Écrans et navigation

```
[Écran titre]
    └──> [Menu principal / Sélection personnage]
              ├──> [Menu amélioration personnage]
              └──> [Sélection niveau]
                        └──> [Jeu (gameplay)]
                                  ├──> [Écran de mort : Rejouer / Menu]
                                  └──> [Écran victoire : Niveau suivant / Menu]
```

---

## 5. Menu principal — Sélection du personnage

- Affichage des **points totaux** du joueur en haut de l'écran.
- 3 emplacements de personnages (extensible plus tard).
  - Personnage 1 : **Angel Monster** (débloqué).
  - Personnage 2 : Verrouillé (silhouette + "Bientôt").
  - Personnage 3 : Verrouillé (silhouette + "Bientôt").
- Chaque personnage est affiché en **haute résolution** (illustration détaillée type menu Brawl Stars).
- Bouton **"Améliorer"** sous chaque personnage débloqué → ouvre le menu d'amélioration.
- Bouton **"Jouer"** → ouvre la sélection de niveau.

---

## 6. Système d'amélioration

### 6.1 Niveaux et coûts

| Niveau | Coût (points) | Effet                                      |
| ------ | ------------- | ------------------------------------------- |
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

**Coût total pour atteindre le niveau 11** : 6 500 points.

### 6.2 Règles

- Progression séquentielle uniquement (2 → 3 → 4, pas de saut).
- Les points dépensés sont **consommés** (déduits du total).

---

## 7. Personnages (Héros)

### 7.1 Angel Monster

- **Apparence** : Monstre bleu avec armure, casque pirate, cache-œil, 4 bras mécaniques, ailes d'énergie bleue, lévite au-dessus du sol. Queue en trident.
- **Attaque principale** : Lance un de ses bras comme projectile en ligne droite. Portée limitée (~5 tiles). Pas de cooldown.
- **Attaque spéciale (niveau 11)** : La queue forme une boule d'électricité projetée à quelques mètres devant lui → explosion de zone détruisant tous les ennemis dans le rayon. Cooldown : 15 secondes.

### 7.2 Personnage 2 — À définir

### 7.3 Personnage 3 — À définir

---

## 8. Ennemis

| Type               | Points | PV   | Dégâts | Vitesse   | Comportement                         |
| ------------------ | ------ | ---- | ------ | --------- | ------------------------------------ |
| Zombie Normal      | 10     | 1    | 0.5 ❤  | Lent      | Marche vers le joueur                |
| Zombie Moyen       | 20     | 2    | 0.5 ❤  | Moyen     | Marche + esquive légère              |
| Zombie Fou de Rage | 30     | 3    | 1 ❤    | Rapide    | Charge en ligne droite               |
| Zombie Boss         | 50     | 10+  | 1 ❤    | Moyen     | Patterns d'attaque, 1 par map       |

- Chaque map contient **20 à 30 zombies** (hors boss).
- Les zombies peuvent apparaître par **surprise** : tombant du plafond, surgissant du sol, derrière des portes.

---

## 9. Système de vie du héros

- **3 cœurs** (6 demi-cœurs).
- Chaque coup reçu = **-0.5 cœur** (zombie normal/moyen) ou **-1 cœur** (fou de rage/boss).
- **À la mort** :
  - Choix : **Rejouer** ou **Retour au menu**.
  - Si rejouer : reprise au point de mort, **-100 points**.
  - Si retour au menu : le niveau est remis à zéro, points conservés.

---

## 10. Système de points

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

Les points sont la **monnaie unique** pour améliorer les personnages dans le menu principal.

---

## 11. Maps / Niveaux

### 11.1 Structure

- **10 niveaux** au total, progression linéaire (finir N pour débloquer N+1).
- Chaque niveau = une zone du manoir (hall, cuisine, bibliothèque, cave, grenier, jardin, etc.).
- Vue isométrique, défilement vertical (portrait) en suivant le joueur.

### 11.2 Éléments de map

| Élément            | Interaction                                             |
| ------------------ | ------------------------------------------------------- |
| Murs               | Collision — bloquent joueur et projectiles               |
| Portes              | S'ouvrent en appuyant sur un bouton/interrupteur nearby |
| Zones de spawn      | Zombies apparaissent (plafond, sol, derrière meubles)   |
| Meubles/Décors      | Collision — éléments décoratifs non traversables         |
| Sol traversable     | Zones de déplacement libre                               |

### 11.3 Niveau 1 — Hall d'entrée du manoir

Basé sur l'image `Design/Maps/level_1_entree_manoir.png` :
- Pièces : Hall d'entrée, Vestiaire, Bibliothèque, Salle de bain, Cuisine, Chambre de la Nourrice, Chambre d'Amis.
- Ambiance sombre, éclairage aux bougies, meubles renversés.
- ~20 zombies normaux + 1 boss.

### 11.4 Difficulté progressive

| Niveau | Zombies normaux | Zombies moyens | Fous de rage | Boss | Points max estimés |
| ------ | --------------- | -------------- | ------------ | ---- | ------------------ |
| 1      | 20              | 0              | 0            | 1    | 250                |
| 2      | 15              | 5              | 0            | 1    | 300                |
| 3      | 10              | 10             | 2            | 1    | 410                |
| 4      | 8               | 10             | 5            | 1    | 480                |
| 5      | 5               | 10             | 8            | 1    | 540                |
| 6      | 5               | 8              | 10            | 1    | 560                |
| 7      | 3               | 8              | 12            | 1    | 600                |
| 8      | 2               | 5              | 15            | 1    | 620                |
| 9      | 0               | 5              | 18            | 1    | 690                |
| 10     | 0               | 3              | 20            | 1    | 710                |

---

## 12. Contrôles

### Smartphone (tactile)

- **Joystick virtuel gauche** : Déplacement 8 directions.
- **Joystick virtuel droit** : Direction du tir (relâcher pour tirer).
- **Bouton spécial** (niveau 11) : Déclenche le pouvoir secret.

### Mac (clavier + souris)

- **ZQSD / WASD** : Déplacement.
- **Souris** : Visée.
- **Clic gauche** : Tir.
- **Espace** : Pouvoir spécial (niveau 11).

---

## 13. Guide de création des assets graphiques (pour LLM)

### 13.1 Personnages (menu principal)

```
Prompt type: illustration de personnage pour jeu mobile
Style: cartoon Brawl Stars, couleurs vives sur fond sombre
Résolution: 1024x1024 px, PNG fond transparent
Vue: face, légèrement en contre-plongée
Détail: très détaillé, éclairage dynamique, effets de particules
```

### 13.2 Sprites personnages (en jeu)

```
Prompt type: sprite sheet vue isométrique top-down
Style: cartoon Brawl Stars, proportions chibi
Résolution: sprite 128x128 px par frame
Vue: isométrique légèrement surélevée (angle ~30°)
Animations nécessaires:
  - Idle (4 frames, 4 directions)
  - Walk (6 frames, 4 directions)
  - Attack (4 frames, 4 directions)
  - Death (4 frames)
  - Special attack (6 frames)
Format: sprite sheet PNG, fond transparent
```

### 13.3 Sprites ennemis (en jeu)

```
Même specs que personnages jouables.
Types à générer:
  - Zombie normal: humanoïde décomposé, lent, verdâtre
  - Zombie moyen: plus grand, vêtements déchirés, yeux rouges
  - Zombie fou de rage: musculature grotesque, mâchoire décrochée, aura rouge
  - Zombie boss: géant (256x256 px), unique par niveau, détaillé
```

### 13.4 Tiles de map

```
Prompt type: tileset isométrique pour jeu top-down
Style: manoir hanté, ambiance sombre, éclairage bougies/lune
Résolution: tiles de 64x64 px ou 128x128 px
Vue: isométrique ~30°
Éléments à générer par set:
  - Sol (parquet, pierre, terre, herbe)
  - Murs (briques, bois, pierre — bords N/S/E/O + coins)
  - Portes (ouverte + fermée)
  - Meubles (tables, chaises, bibliothèques, lits — collisions)
  - Décors (chandeliers, tableaux, tapis — pas de collision)
  - Escaliers (montée/descente)
Format: tileset PNG unifié OU tiles individuels PNG fond transparent
```

### 13.5 Méthode pour lier design et fonctionnel

**Approche recommandée : Dual-layer map**

1. **Layer visuel** : L'image générée par le LLM (belle, détaillée).
2. **Layer collision** : Une image simplifiée (créée manuellement ou par code) qui définit :
   - Noir = mur/obstacle (collision)
   - Blanc = sol traversable
   - Rouge = zone de spawn ennemis
   - Bleu = porte (interactif)
   - Vert = point de départ joueur
   - Jaune = trigger zone (événements)

On superpose les deux layers. Le moteur de jeu utilise le layer collision pour la logique, et le layer visuel pour l'affichage.

**Alternative** : Utiliser **Tiled Map Editor** (gratuit) pour placer les tiles et exporter un fichier JSON lisible par le moteur de jeu.

---

## 14. Audio

### 14.1 Sources gratuites recommandées

| Bibliothèque                  | URL                                      | Licence           | Contenu principal                |
| ----------------------------- | ---------------------------------------- | ----------------- | -------------------------------- |
| **Freesound.org**             | freesound.org                            | CC0 / CC-BY       | SFX variés, bruitages            |
| **OpenGameArt.org**           | opengameart.org                          | CC0 / CC-BY       | SFX + musiques pour jeux         |
| **Mixkit**                    | mixkit.co/free-sound-effects             | Libre de droits   | SFX haute qualité                |
| **Pixabay Music**             | pixabay.com/music                        | Libre de droits   | Musiques d'ambiance              |
| **Kevin MacLeod (Incompetech)**| incompetech.com                         | CC-BY 3.0         | Musiques horreur/ambiance        |

### 14.2 Musiques (boucles)

| Contexte                  | Style                                           | Format      |
| ------------------------- | ----------------------------------------------- | ----------- |
| Menu principal            | Ambiance mystérieuse, piano sombre, calme        | MP3, boucle |
| En jeu (exploration)      | Tension basse, cordes, ambiance manoir hanté      | MP3, boucle |
| En jeu (combat intense)   | Rythme rapide, percussions, urgence               | MP3, boucle |
| Boss                      | Épique sombre, cuivres, montée dramatique         | MP3, boucle |
| Victoire                  | Fanfare courte, triomphale                        | MP3, one-shot |
| Mort / Game Over          | Mélancolique, court, descendant                   | MP3, one-shot |

### 14.3 Effets sonores (SFX)

| Événement                     | Description sonore                            |
| ----------------------------- | --------------------------------------------- |
| **Joueur**                    |                                               |
| Pas du joueur                 | Pas sur bois / pierre (selon le sol)          |
| Attaque (lancer de bras)      | Whoosh mécanique                              |
| Attaque spéciale (électricité)| Charge électrique + explosion                 |
| Dégât reçu                    | Impact + cri de douleur court                 |
| Mort du joueur                | Chute + son dramatique                        |
| **Ennemis**                   |                                               |
| Grognement zombie (idle)      | Grognement sourd, aléatoire                   |
| Zombie apparition surprise    | Son de chute / craquement + cri               |
| Zombie touché                 | Impact chair, splash                          |
| Zombie mort                   | Effondrement + gémissement                    |
| Boss rugissement              | Rugissement grave, puissant                   |
| **Environnement**             |                                               |
| Porte qui s'ouvre             | Grincement bois / métal                       |
| Bouton / interrupteur         | Clic mécanique                                |
| Ambiance manoir               | Craquements, vent, horloge (subtil, en fond)  |
| **UI**                        |                                               |
| Clic bouton menu              | Pop / clic satisfaisant                       |
| Amélioration personnage       | Jingle positif + effet de power-up            |
| Niveau débloqué               | Fanfare courte                                |
| Points gagnés                 | Tintement de pièce (léger)                    |

### 14.4 Spécifications techniques

- **Format** : MP3 (compatibilité maximale web) + OGG en fallback.
- **Musiques** : 128 kbps, stéréo, normalisées à -14 LUFS.
- **SFX** : 44.1 kHz, mono, normalisés, durée < 2 secondes (sauf ambiance).
- **Taille cible** : musiques < 2 Mo chacune, SFX < 100 Ko chacun.
- **Volume par défaut** : Musique 0.4, SFX 0.7 (ajustable dans les options).

---

## 15. Sauvegarde

- **Locale** (localStorage / IndexedDB) :
  - Points totaux
  - Niveau max débloqué
  - Niveau de chaque personnage
  - Personnages débloqués
  - **Volume musique** (0.0 – 1.0)
  - **Volume SFX** (0.0 – 1.0)
  - **Mute** (on/off)

---

## 17. Roadmap

| Phase | Contenu                                                  |
| ----- | -------------------------------------------------------- |
| MVP   | Angel Monster + Niveau 1 + Menu + Amélioration + Audio   |
| V1.1  | Niveaux 2-5                                              |
| V1.2  | Personnage 2 + Niveaux 6-8                               |
| V1.3  | Personnage 3 + Niveaux 9-10                              |
| V2.0  | Multijoueur ? Événements ? Leaderboard ?                 |
