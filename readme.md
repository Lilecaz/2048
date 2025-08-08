# 2048 Game

Un jeu 2048 développé en Python avec Pygame, incluant des animations fluides pour les mouvements des tuiles.

## Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Contrôles](#contrôles)

## Aperçu

Ce projet est une implémentation du célèbre jeu 2048 en Python utilisant la bibliothèque Pygame. Le jeu inclut des animations fluides pour les mouvements des tuiles, rendant l'expérience de jeu plus agréable et moderne.

## Fonctionnalités

- ✨ **Animations fluides** : Les tuiles bougent avec des transitions animées
- 🎮 **Contrôles intuitifs** : Utilisation des flèches directionnelles
- 📊 **Système de score** : Suivi du score actuel et du meilleur score
- 🔄 **Restart rapide** : Possibilité de recommencer une partie facilement
- 🎨 **Interface moderne** : Design coloré et épuré

## Installation

### Prérequis

- Python 3.7 ou plus récent
- Pygame

### Étapes d'installation

1. **Cloner le repository :**
   ```bash
   git clone https://github.com/Lilecaz/2048
   cd 2048
   ```

2. **Installer Pygame :**
   ```bash
   pip install pygame
   ```

## Utilisation

Pour lancer le jeu :

```bash
python main.py
```

## Contrôles

- **Flèches directionnelles** : Déplacer les tuiles
- **R** : Recommencer la partie (quand le jeu est terminé)
- **Q** : Quitter le jeu (quand le jeu est terminé)
- **Fermer la fenêtre** : Quitter le jeu

## Règles du jeu

1. Utilisez les flèches pour déplacer les tuiles
2. Quand deux tuiles avec le même nombre se touchent, elles fusionnent
3. Le but est d'atteindre la tuile 2048
4. Le jeu se termine quand aucun mouvement n'est possible
