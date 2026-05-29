# The Elder Scroll 2D (Projet NSI)

Jeu 2D en Python réalisé dans le cadre de la NSI, avec sélection de personnage, exploration de cartes, dialogues PNJ, monstres, collisions et transitions entre zones.

## Badges (outils & bibliothèques)

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-0E1117?logo=pygame&logoColor=white)
![PyTMX](https://img.shields.io/badge/PyTMX-TMX%20Loader-2E8B57)
![PyScroll](https://img.shields.io/badge/PyScroll-Map%20Rendering-6A5ACD)
![Tiled](https://img.shields.io/badge/Tiled-Map%20Editor-4CAF50)

## Date de réalisation:
Novembre 2024

## Aperçu

Le jeu démarre sur un menu qui permet de choisir entre **Chevalier**, **Mage** et **Archer**. Ensuite, vous explorez plusieurs cartes (`map`, `catacombes_map`, `Dungeon_map`) avec combats et interactions avec des PNJ.

## Fonctionnalités

- Menu principal avec sélection de personnage.
- Déplacement fluide et animations (marche, attaque, mort).
- Système de dialogues avec affichage progressif du texte.
- Gestion des collisions (murs, portails, entités).
- Monstres avec vision, poursuite et attaque.
- Cartes TMX chargées depuis `assets/map/`.

## Prérequis

- Python 3.x
- Dépendances Python :
	- `pygame`
	- `pytmx`
	- `pyscroll`

> `dataclasses` est intégré à Python (standard library, à partir de Python 3.7).

## Installation

Depuis la racine du projet :

```bash
pip install pygame pytmx pyscroll
```

## Lancer le jeu

```bash
python main.py
```

## Contrôles

- `Z` : avancer
- `S` : reculer
- `Q` : aller à gauche
- `D` : aller à droite
- `R` : courir
- `W` : marcher
- `Espace` : interagir avec un PNJ
- `Flèches` : attaquer (haut, bas, gauche, droite)

## Structure du projet

- `main.py` : point d'entrée.
- `main_choice.py` : menu de sélection du personnage.
- `game.py` : boucle de jeu, inputs, rendu.
- `Map.py` : chargement des cartes, collisions, portails, gestion des PNJ/monstres.
- `player.py` : entités (`Player`, `NPC`, `Monster`) et logique de combat.
- `animation.py` : animations des sprites.
- `dialog.py` : boîte de dialogue.
- `assets/` : sprites et maps TMX/TSX.
- `dialogues/` : ressources de dialogues (boîte, police).

## Auteurs

- Lucas Contreras Hodapp
- Clément Faillet Turon

- Sprites par le projet Liberated Pixel Cup (LPC)
https://opengameart.org/content/lpc-collection

Crédits détaillés : https://github.com/LiberatedPixelCup/Universal-LPC-Spritesheet-Character-Generator/blob/master/CREDITS.csv
