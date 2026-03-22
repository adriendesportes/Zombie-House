# Epic Suivi — Zombie House

> Dernière mise à jour : 2026-03-22

## Légende des statuts

| Statut      | Description                              |
| ----------- | ---------------------------------------- |
| `BACKLOG`   | À faire, pas encore commencé             |
| `DEV`       | En cours de développement                |
| `TEST`      | Développé, en cours de test              |
| `DONE`      | Terminé et validé                        |
| `BLOCKED`   | Bloqué par une dépendance               |

---

## EPIC 1 — MVP (Gameplay core jouable)

| Story | Titre                                      | Dépendances | Statut    |
| ----- | ------------------------------------------ | ----------- | --------- |
| 001   | Assets graphiques MVP                      | —           | `BACKLOG` |
| 002   | MVP jouable (map test + gameplay minimal)  | 001         | `BACKLOG` |
| 003   | Setup projet (Vite + Phaser + TS)          | —           | `BACKLOG` |
| 004   | Tilemap + map de test (4 pièces)           | 001, 003    | `BACKLOG` |
| 005   | Player Angel Monster (déplacement + anim)  | 001, 003    | `BACKLOG` |
| 006   | Input Manager (joystick + clavier/souris)  | 003         | `BACKLOG` |
| 007   | Projectile (bras lancé)                    | 005         | `BACKLOG` |
| 008   | Ennemis (Zombie Normal + Boss simplifié)   | 001, 004    | `BACKLOG` |
| 009   | Système de vie (cœurs + dégâts)            | 005, 008    | `BACKLOG` |
| 010   | Système de points                          | 008         | `BACKLOG` |
| 011   | Portes (ouverture au contact)              | 004         | `BACKLOG` |
| 012   | Condition victoire + Game Over             | 008, 009    | `BACKLOG` |
| 013   | Audio minimal (1 musique + SFX de base)    | 003         | `BACKLOG` |
| 014   | HUD en jeu (cœurs, points, joysticks)      | 006, 009, 010 | `BACKLOG` |

---

## EPIC 2 — Menu et progression

| Story | Titre                                      | Dépendances     | Statut    |
| ----- | ------------------------------------------ | --------------- | --------- |
| 020   | Menu principal (sélection personnage)      | 001, EPIC 1     | `BACKLOG` |
| 021   | Assets menu (fond, boutons, portraits HD)  | —               | `BACKLOG` |
| 022   | Système d'amélioration (niveaux 1-11)      | 020, 010        | `BACKLOG` |
| 023   | Sélection de niveau (progression linéaire) | 020             | `BACKLOG` |
| 024   | Sauvegarde localStorage                    | 022, 023        | `BACKLOG` |
| 025   | Écran de mort (Rejouer / Menu)             | 012, 020        | `BACKLOG` |
| 026   | Écran de victoire (Niveau suivant / Menu)  | 012, 023        | `BACKLOG` |

---

## EPIC 3 — Gameplay complet

| Story | Titre                                      | Dépendances     | Statut    |
| ----- | ------------------------------------------ | --------------- | --------- |
| 030   | Zombie Moyen (IA + sprites)                | 008             | `BACKLOG` |
| 031   | Zombie Fou de Rage (charge + sprites)      | 008             | `BACKLOG` |
| 032   | Zombie Boss avancé (patterns d'attaque)    | 008             | `BACKLOG` |
| 033   | Spawns surprise (plafond, sol)             | 004, 008        | `BACKLOG` |
| 034   | Portes avec boutons/interrupteurs          | 011             | `BACKLOG` |
| 035   | Attaque spéciale niveau 11 (électricité)   | 007, 022        | `BACKLOG` |
| 036   | Stats progression (puissance/vie par lvl)  | 022             | `BACKLOG` |
| 037   | Invincibilité temporaire + clignotement    | 009             | `BACKLOG` |

---

## EPIC 4 — Audio complet

| Story | Titre                                      | Dépendances     | Statut    |
| ----- | ------------------------------------------ | --------------- | --------- |
| 040   | Crossfade musique contextuel (explo/combat/boss) | 013       | `BACKLOG` |
| 041   | SFX complets (tous les sons du PRD §14.3)  | 013             | `BACKLOG` |
| 042   | Ambiance manoir (craquements, vent)        | 013             | `BACKLOG` |
| 043   | Options volume (musique / SFX / mute)      | 024, 013        | `BACKLOG` |
| 044   | Jingles victoire / game over               | 013             | `BACKLOG` |

---

## EPIC 5 — Maps et contenu

| Story | Titre                                      | Dépendances     | Statut    |
| ----- | ------------------------------------------ | --------------- | --------- |
| 050   | Niveau 1 complet (Hall d'entrée, 7 pièces) | 004, EPIC 3    | `BACKLOG` |
| 051   | Niveau 2 (Caves)                           | 050             | `BACKLOG` |
| 052   | Niveau 3 (Cuisine + Salle à manger)       | 050             | `BACKLOG` |
| 053   | Niveau 4 (Chambres étage 1)               | 050             | `BACKLOG` |
| 054   | Niveau 5 (Grenier)                         | 050             | `BACKLOG` |
| 055   | Niveau 6 (Jardin / Extérieur)             | 050             | `BACKLOG` |
| 056   | Niveau 7 (Chapelle)                        | 050             | `BACKLOG` |
| 057   | Niveau 8 (Donjon)                          | 050             | `BACKLOG` |
| 058   | Niveau 9 (Tour)                            | 050             | `BACKLOG` |
| 059   | Niveau 10 (Boss final — Crypte)            | 050             | `BACKLOG` |
| 060   | Tilesets additionnels (cave, extérieur, grenier) | 001       | `BACKLOG` |

---

## EPIC 6 — Personnages additionnels

| Story | Titre                                      | Dépendances     | Statut    |
| ----- | ------------------------------------------ | --------------- | --------- |
| 070   | Personnage 2 — Concept + Design            | —               | `BACKLOG` |
| 071   | Personnage 2 — Sprites + Animations        | 070             | `BACKLOG` |
| 072   | Personnage 2 — Implémentation gameplay     | 071, 005        | `BACKLOG` |
| 073   | Personnage 3 — Concept + Design            | —               | `BACKLOG` |
| 074   | Personnage 3 — Sprites + Animations        | 073             | `BACKLOG` |
| 075   | Personnage 3 — Implémentation gameplay     | 074, 005        | `BACKLOG` |

---

## EPIC 7 — Polish et publication

| Story | Titre                                      | Dépendances     | Statut    |
| ----- | ------------------------------------------ | --------------- | --------- |
| 080   | Animations de transition entre scènes      | EPIC 2          | `BACKLOG` |
| 081   | Effets de particules (attaques, morts)     | EPIC 3          | `BACKLOG` |
| 082   | Écran titre                                | 021             | `BACKLOG` |
| 083   | PWA (manifest, service worker, icônes)     | EPIC 1          | `BACKLOG` |
| 084   | Déploiement (Vercel / Netlify)             | 083             | `BACKLOG` |
| 085   | Test multi-navigateurs (Chrome, Safari, FF)| 084             | `BACKLOG` |
| 086   | Test performance mobile                    | 084             | `BACKLOG` |

---

## Résumé par Epic

| Epic | Nom                      | Stories | Done | Progression |
| ---- | ------------------------ | ------- | ---- | ----------- |
| 1    | MVP                      | 14      | 0    | 0%          |
| 2    | Menu et progression      | 7       | 0    | 0%          |
| 3    | Gameplay complet         | 8       | 0    | 0%          |
| 4    | Audio complet            | 5       | 0    | 0%          |
| 5    | Maps et contenu          | 11      | 0    | 0%          |
| 6    | Personnages additionnels | 6       | 0    | 0%          |
| 7    | Polish et publication    | 7       | 0    | 0%          |
| **Total** |                     | **58**  | **0**| **0%**      |
