# Projet Albert 1 - Assistant Mairie

Un assistant numérique permettant aux particuliers de contacter facilement la mairie la plus proche de leur domicile.

## Description

Ce projet développe un outil qui simplifie la communication entre les citoyens et les administrations locales en:

- Localisant automatiquement la mairie la plus proche de l'adresse de l'utilisateur
- Générant un email correctement formaté et adapté à la demande spécifique de l'utilisateur

## Fonctionnalités

- Géolocalisation de la mairie la plus proche
- Visualisation cartographique interactive
- Génération d'emails formels via un modèle de langage
- Interface utilisateur simple et intuitive

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### Étapes d'installation

1. **Cloner le dépôt**

```bash
git clone https://github.com/davialabs/projet-albert-1.git
cd projet-albert-1
```

2. **Créer un environnement virtuel**

```bash
python -m venv .venv
```

3. **Activer l'environnement virtuel**

Sur Windows:

```bash
.venv\Scripts\activate
```

Sur macOS/Linux:

```bash
source .venv/bin/activate
```

4. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

5. **Vérifier l'accès aux données**

Assurez-vous que le fichier `data_mairies.csv` est présent dans le répertoire du projet.

## Bonnes pratiques Git

Pour contribuer efficacement à ce projet, suivez ces pratiques Git recommandées:

### Configuration initiale

```bash
# Configurez votre identité Git
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@exemple.com"

# Vérifiez votre configuration
git config --list
```

### Workflow de base

```bash
# Vérifiez l'état de votre dépôt
git status

# Récupérez les dernières modifications
git pull origin main

# Créez une nouvelle branche pour vos modifications
git checkout -b feature/ma-fonctionnalite

# Ajoutez vos modifications
git add .

# Committez avec un message descriptif
git commit -m "Description claire des modifications"

# Poussez vers le dépôt distant
git push origin feature/ma-fonctionnalite
```

### Conseils pour les commits

- Faites des commits atomiques (une seule fonctionnalité/correction par commit)
- Utilisez des messages de commit clairs et descriptifs
- Commitez régulièrement pour éviter les conflits complexes

### Gestion des branches

- `main`: branche principale, toujours stable
- `feature/*`: pour développer de nouvelles fonctionnalités

## Structure du projet

- `data_mairies.csv` - Base de données des mairies françaises
- `requirements.txt` - Liste des dépendances
