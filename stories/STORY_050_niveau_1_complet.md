# STORY-050 : Niveau 1 complet — Hall d'entree du manoir

**Epic** : Maps et contenu
**Statut** : BACKLOG
**Dependances** : STORY-001 (assets), STORY-002 (MVP jouable)
**Reference visuelle** : `Design/Maps/level_1_entree_manoir.png`

---

## Objectif

Creer le premier vrai niveau du jeu : l'etage 1 du manoir hante, avec 7 pieces interconnectees, une ambiance sombre et detaillee, 20 zombies normaux + 1 boss. La map doit etre visuellement riche (style Brawl Stars) et offrir un vrai parcours de jeu de 3 a 5 minutes.

---

## Layout de la map (base sur l'image de reference)

```
┌──────────────────────────────────────────────────────────┐
│                    MANOIR HANTE — ETAGE 1                │
│                                                          │
│  ┌─────────────┬──────────────┬─────────┬──────────────┐ │
│  │  CHAMBRE DE │  SALLE DE    │ CUISINE │  CHAMBRE     │ │
│  │  LA NOURRICE│  BAIN        │         │  D'AMIS      │ │
│  │  (bois)     │  (carrelage) │ (dalle) │  (tapis)     │ │
│  │             │              │         │              │ │
│  ├────[porte]──┼───[porte]────┼─[porte]─┼──[porte]─────┤ │
│  │             │                        │              │ │
│  │  VESTIAIRE  │      HALL D'ENTREE     │ BIBLIOTHEQUE │ │
│  │  (pierre)   │      (parquet + tapis) │ (bois)       │ │
│  │             │                        │              │ │
│  └─────────────┴────────────────────────┴──────────────┘ │
│                      [PORTE ENTREE]                      │
└──────────────────────────────────────────────────────────┘
```

---

## Dimensions

- **Taille map** : 40 colonnes x 32 lignes (1600x1280 px a 40px/tile)
- **Camera** : suit le joueur, defilement libre dans toute la map
- **Spawn joueur** : devant la porte d'entree (bas du hall)

---

## Pieces detaillees

### 1. Hall d'entree (centre, grande piece)
- **Sol** : parquet clair avec un grand tapis rouge central
- **Decor** :
  - Grand lustre (torche centrale)
  - Escalier en ruine (mur destructible bloquant un passage)
  - Colonnes decoratives (demi-murs)
  - Debris au sol (os, fissures)
  - Porte d'entree massive en bas (la ou le joueur spawn)
- **Eclairage** : torches aux 4 coins, lueur chaude
- **Zombies** : 4 normaux qui patrouillent

### 2. Vestiaire (gauche du hall)
- **Sol** : pierre grise
- **Decor** :
  - Porte-manteaux (murs destructibles)
  - Tonneaux, caisses
  - Toiles d'araignee dans les coins
  - Miroir brise (decoration au sol)
- **Zombies** : 2 normaux, 1 spawn surprise (apparait quand on entre)
- **Acces** : porte depuis le hall

### 3. Bibliotheque (droite du hall)
- **Sol** : parquet sombre
- **Decor** :
  - Etageres de livres le long des murs (meubles-obstacles)
  - Table de lecture avec chandelier
  - Livres tombes au sol (decorations)
  - Passage secret derriere une etagere (mur destructible)
- **Zombies** : 3 normaux
- **Acces** : porte depuis le hall

### 4. Chambre de la Nourrice (haut gauche)
- **Sol** : parquet avec zones de tapis use
- **Decor** :
  - Lit brise (obstacle)
  - Berceau renverse (decoration)
  - Vieux jouets au sol (decorations)
  - Rideaux dechires (buissons/obstacles visuels)
- **Zombies** : 2 normaux
- **Acces** : porte depuis le vestiaire ou la salle de bain

### 5. Salle de bain (haut centre)
- **Sol** : carrelage (gravier ou pierre claire)
- **Decor** :
  - Baignoire (obstacle, eau a l'interieur)
  - Lavabo casse (decoration)
  - Flaques d'eau au sol
  - Miroir brise, sang sur les murs
- **Zombies** : 2 normaux, 1 spawn surprise depuis la baignoire
- **Acces** : portes depuis chambre nourrice et cuisine

### 6. Cuisine (haut centre-droit)
- **Sol** : dalles de pierre
- **Decor** :
  - Tables de travail (obstacles)
  - Tonneaux de provisions
  - Ustensiles eparpilles (decorations)
  - Four eteint (gros obstacle)
  - Flaques de sang
- **Zombies** : 3 normaux
- **Acces** : portes depuis salle de bain et chambre d'amis

### 7. Chambre d'amis (haut droit)
- **Sol** : tapis rouge use
- **Decor** :
  - Grand lit a baldaquin (obstacle central)
  - Armoire (mur destructible, cache le BOSS)
  - Chandeliers
  - Rideaux (buissons)
- **Zombies** : 3 normaux + **1 BOSS** (cache derriere l'armoire destructible)
- **Acces** : porte depuis la bibliotheque ou la cuisine

---

## Zombies (total : 20 normaux + 1 boss)

| Piece              | Normaux | Surprise | Boss |
| ------------------ | ------- | -------- | ---- |
| Hall d'entree      | 4       | 0        | 0    |
| Vestiaire          | 2       | 1        | 0    |
| Bibliotheque       | 3       | 0        | 0    |
| Chambre Nourrice   | 2       | 0        | 0    |
| Salle de bain      | 2       | 1        | 0    |
| Cuisine            | 3       | 0        | 0    |
| Chambre d'amis     | 3       | 0        | 1    |
| **Total**          | **19**  | **2**    | **1**|

Points max possibles : 19x10 + 2x10 + 1x50 = **260 points**

---

## Nouveaux assets necessaires

### Tiles sol supplementaires
- [ ] Carrelage blanc/gris (salle de bain) — ajouter au ground-atlas
- [ ] Parquet use avec tapis integre (chambres)

### Meubles/obstacles (nouveaux types de murs)
- [ ] Lit (2x1 tiles, obstacle)
- [ ] Table longue (2x1 tiles, obstacle)
- [ ] Etagere de livres (1x1, obstacle, variante du mur)
- [ ] Baignoire (2x1, obstacle + eau interieure)
- [ ] Armoire (1x1, mur destructible special = cache le boss)

### Decorations sol (ajouter au deco-atlas)
- [ ] Livres tombes
- [ ] Ustensiles de cuisine
- [ ] Jouets casses
- [ ] Miroir brise
- [ ] Flaques d'eau

### Elements de jeu
- [ ] Spawn surprise : zombie apparait quand le joueur entre dans un rayon (trigger zone)
- [ ] Boss cache : apparait quand le mur destructible (armoire) est detruit

---

## Taches techniques

### T1 — Nouveaux assets tiles
- [ ] Ajouter les tiles au script generate_tiles_hq.py
- [ ] Regenerer les atlas
- [ ] Ajouter les types dans le code (TILE_BATHROOM, FURNITURE_BED, etc.)

### T2 — Map JSON
- [ ] Creer public/assets/maps/level-1-manoir.json (remplace level-1.json)
- [ ] 40x32 grille avec les 7 pieces
- [ ] Placement des murs, portes, meubles, decorations
- [ ] Spawn points joueur + zombies + boss
- [ ] Trigger zones pour spawns surprise

### T3 — Charger la map depuis JSON
- [ ] Refactorer index.html pour charger la map depuis le JSON au lieu de la hardcoder
- [ ] Parser les murs (rows, cols, individuels)
- [ ] Parser les decorations
- [ ] Parser les spawn points

### T4 — Spawn surprise
- [ ] Trigger zones dans le JSON (position + rayon)
- [ ] Quand le joueur entre dans la zone, un zombie apparait avec animation
- [ ] Le zombie apparait avec un petit delai + effet de particules

### T5 — Boss cache
- [ ] L'armoire est un mur destructible marque "boss_trigger"
- [ ] Quand detruite, le boss spawn a cette position
- [ ] Le boss a un cri (SFX rugissement) a l'apparition

### T6 — Test et equilibrage
- [ ] Tester le parcours complet (3-5 minutes)
- [ ] Verifier que les 260 points sont atteignables
- [ ] Ajuster la difficulte si necessaire (vitesse zombies, nombre)

---

## Criteres d'acceptation

- [ ] 7 pieces interconnectees avec des portes
- [ ] Chaque piece a une identite visuelle distincte (sol, decor, ambiance)
- [ ] 20 zombies normaux + 2 surprises + 1 boss = 23 ennemis total
- [ ] Le boss est cache derriere un mur destructible
- [ ] Les spawns surprise fonctionnent (trigger zone)
- [ ] Le joueur peut explorer toute la map et tuer tous les zombies
- [ ] Ecran de victoire quand tous les zombies sont morts
- [ ] La map se charge depuis un fichier JSON
- [ ] Les tiles sont visuellement riches (pas de zones vides ou repetitives)
- [ ] Fonctionne en 3D (Three.js) et sur mobile
- [ ] Performance 60fps sur mobile
