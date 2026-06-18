# Emergency Coding Navigator

Ce projet est un outil de visualisation interactive sous forme de carte mentale, conçu en Python avec PySide6 et PyVis. Son but est de faciliter l'exploration et la navigation dans la hiérarchie complexe du codage médical des urgences (les fameux RPU). 

L'outil structure les données de manière logique, en partant des grandes catégories (les organes) jusqu'aux codes médicaux spécifiques.

## Fonctionnalités
- **Visualisation interactive** : Un graphe que l'on peut explorer librement.
- **Recherche et filtres** : Vous pouvez filtrer le graphe par organe ou utiliser la barre de recherche avec autocomplétion pour trouver un terme précis.
- **Panneau de détails** : En cliquant sur un nœud, vous affichez ses informations complètes (définition, intermédiaire, code RPU final).
- **Performances** : Le rendu est optimisé pour gérer de grands volumes de données.

## Documentation
- [Guide Utilisateur](docs/user_guide.md) : Pour savoir comment installer et utiliser l'application au quotidien.
- [Guide Développeur](docs/developer_guide.md) : Pour comprendre l'architecture du code et savoir comment le modifier ou l'améliorer.

## Installation
Assurez-vous d'avoir Python 3 installé sur votre machine. Il est fortement recommandé d'utiliser un environnement virtuel (par exemple `.venv`) pour installer les dépendances.

```bash
python -m venv .venv
source .venv/bin/activate  # Sur Windows, utilisez : .venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement de l'application
Pour démarrer l'outil, il suffit de lancer le script principal :
```bash
python main.py
```
