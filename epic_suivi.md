# Epic Suivi — Zombie House

> Derniere mise a jour : 2026-03-22

## Legende des statuts

| Statut      | Description                              |
| ----------- | ---------------------------------------- |
| `BACKLOG`   | A faire, pas encore commence             |
| `DEV`       | En cours de developpement                |
| `TEST`      | Developpe, en cours de test              |
| `DONE`      | Termine et valide                        |

---

## EPIC 1 — MVP (Gameplay core jouable)

| Story | Titre                                      | Dependances | Statut    |
| ----- | ------------------------------------------ | ----------- | --------- |
| 001   | Assets graphiques MVP                      | —           | `DONE`    |
| 002   | MVP jouable (prototype complet)            | 001         | `DONE`    |
| 003   | Setup projet (HTML + Canvas + Three.js)    | —           | `DONE`    |
| 004   | Map de test (28x22, 5 zones, JSON)         | 001, 003    | `DONE`    |
| 005   | Player Angel Monster (deplacement + sprites)| 001, 003   | `DONE`    |
| 006   | Input (joystick tactile + clavier/souris)  | 003         | `DONE`    |
| 007   | Projectile (auto-aim + trail + particules) | 005         | `DONE`    |
| 008   | Ennemis (Normal + Moyen + Rage, sprites)   | 001, 004    | `DONE`    |
| 009   | Systeme de vie (coeurs + degats contact)   | 005, 008    | `DONE`    |
| 010   | Systeme de points                          | 008         | `DONE`    |
| 011   | Portes (3 variantes visuelles)             | 004         | `DONE`    |
| 012   | Condition victoire + Game Over             | 008, 009    | `DONE`    |
| 013   | Audio minimal (1 musique + SFX de base)    | 003         | `DONE`    |
| 014   | HUD en jeu (coeurs, compteur, joystick)    | 006, 009    | `DONE`    |
| 015   | Rendu 3D Three.js (camera + textures atlas)| 001, 004    | `DONE`    |
| 016   | Murs destructibles (3 variantes + particules)| 004       | `DONE`    |
| 017   | Boss niveau 1                              | 008         | `DONE`    |
| 018   | Invincibilite temporaire + clignotement    | 009         | `DONE`    |

---

## EPIC 2 — Menu et progression

| Story | Titre                                      | Dependances     | Statut    |
| ----- | ------------------------------------------ | --------------- | --------- |
| 020   | Menu principal (selection personnage)      | EPIC 1          | `BACKLOG` |
| 021   | Assets menu (fond, boutons, portraits HD)  | —               | `BACKLOG` |
| 022   | Systeme d'amelioration (niveaux 1-11)      | 020, 010        | `BACKLOG` |
| 023   | Selection de niveau (progression lineaire) | 020             | `BACKLOG` |
| 024   | Sauvegarde localStorage                    | 022, 023        | `BACKLOG` |
| 025   | Ecran de mort (Rejouer -100pts / Menu)     | 012, 020        | `BACKLOG` |
| 026   | Ecran de victoire (Niveau suivant / Menu)  | 012, 023        | `BACKLOG` |

---

## EPIC 3 — Gameplay complet

| Story | Titre                                      | Dependances     | Statut    |
| ----- | ------------------------------------------ | --------------- | --------- |
| 030   | Zombie Boss avance (patterns d'attaque)    | 017             | `BACKLOG` |
| 031   | Spawns surprise (plafond, sol)             | 004, 008        | `BACKLOG` |
| 032   | Portes avec boutons/interrupteurs          | 011             | `BACKLOG` |
| 033   | Attaque speciale niveau 11 (electricite)   | 007, 022        | `BACKLOG` |
| 034   | Stats progression (puissance/vie par lvl)  | 022             | `BACKLOG` |

---

## EPIC 4 — Audio complet

| Story | Titre                                      | Dependances     | Statut    |
| ----- | ------------------------------------------ | --------------- | --------- |
| 040   | Crossfade musique contextuel               | 013             | `BACKLOG` |
| 041   | SFX complets (tous les sons du PRD)        | 013             | `BACKLOG` |
| 042   | Ambiance manoir (craquements, vent)        | 013             | `BACKLOG` |
| 043   | Options volume (musique / SFX / mute)      | 024, 013        | `BACKLOG` |
| 044   | Jingles victoire / game over               | 013             | `BACKLOG` |

---

## EPIC 5 — Maps et contenu

| Story | Titre                                      | Dependances     | Statut    |
| ----- | ------------------------------------------ | --------------- | --------- |
| 050   | Niveau 1 complet (Hall d'entree, 7 pieces) | 004, EPIC 3    | `BACKLOG` |
| 051   | Niveau 2 (Caves)                           | 050             | `BACKLOG` |
| 052   | Niveau 3 (Cuisine + Salle a manger)       | 050             | `BACKLOG` |
| 053   | Niveau 4 (Chambres etage 1)               | 050             | `BACKLOG` |
| 054   | Niveau 5 (Grenier)                         | 050             | `BACKLOG` |
| 055   | Niveau 6 (Jardin / Exterieur)             | 050             | `BACKLOG` |
| 056   | Niveau 7 (Chapelle)                        | 050             | `BACKLOG` |
| 057   | Niveau 8 (Donjon)                          | 050             | `BACKLOG` |
| 058   | Niveau 9 (Tour)                            | 050             | `BACKLOG` |
| 059   | Niveau 10 (Boss final — Crypte)            | 050             | `BACKLOG` |
| 060   | Tilesets additionnels par biome            | 001             | `BACKLOG` |

---

## EPIC 6 — Personnages additionnels

| Story | Titre                                      | Dependances     | Statut    |
| ----- | ------------------------------------------ | --------------- | --------- |
| 070   | Personnage 2 — Concept + Design            | —               | `BACKLOG` |
| 071   | Personnage 2 — Sprites + Animations        | 070             | `BACKLOG` |
| 072   | Personnage 2 — Implementation gameplay     | 071, 005        | `BACKLOG` |
| 073   | Personnage 3 — Concept + Design            | —               | `BACKLOG` |
| 074   | Personnage 3 — Sprites + Animations        | 073             | `BACKLOG` |
| 075   | Personnage 3 — Implementation gameplay     | 074, 005        | `BACKLOG` |

---

## EPIC 7 — Polish et publication

| Story | Titre                                      | Dependances     | Statut    |
| ----- | ------------------------------------------ | --------------- | --------- |
| 080   | Animations de transition entre scenes      | EPIC 2          | `BACKLOG` |
| 081   | Effets de particules avances               | EPIC 3          | `DONE`    |
| 082   | Ecran titre                                | 021             | `BACKLOG` |
| 083   | PWA (manifest, service worker, icones)     | EPIC 1          | `BACKLOG` |
| 084   | Deploiement (Vercel / Netlify)             | 083             | `BACKLOG` |
| 085   | Test multi-navigateurs (Chrome, Safari, FF)| 084             | `BACKLOG` |
| 086   | Test performance mobile                    | 084             | `BACKLOG` |

---

## Resume par Epic

| Epic | Nom                      | Stories | Done | Progression |
| ---- | ------------------------ | ------- | ---- | ----------- |
| 1    | MVP                      | 18      | 17   | 94%         |
| 2    | Menu et progression      | 7       | 0    | 0%          |
| 3    | Gameplay complet         | 5       | 0    | 0%          |
| 4    | Audio complet            | 5       | 0    | 0%          |
| 5    | Maps et contenu          | 11      | 0    | 0%          |
| 6    | Personnages additionnels | 6       | 0    | 0%          |
| 7    | Polish et publication    | 7       | 1    | 14%         |
| **Total** |                     | **59**  | **18**| **31%**    |
