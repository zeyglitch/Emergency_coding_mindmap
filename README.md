# Carte mentale interactive du codage RPU (urgences)

Outil de visualisation interactive sous forme de carte mentale pour explorer la hiérarchie du codage médical des urgences (Résumé de Passage aux Urgences, RPU). Développé en Python avec PySide6 et PyVis.

## Contexte et contribution

Ce projet a été **co-développé** dans le cadre d'un stage de 3ème année d'école d'ingénieur (ISIS Castres, partenaire INSA) au Département d'Information Médicale du Centre Hospitalier de Cahors, entre avril et juin 2026. Le concept général de l'applicatif a été défini par le DIM du Centre Hospitalier de Cahors ; le code présenté ici en est la réalisation technique, publiée avec leur accord.

**Contribution de Mathieu Jonniaux** (auteur de ce dépôt) :
- Conception et implémentation de la visualisation en carte mentale interactive (PySide6 + PyVis)
- Structure de navigation, filtres et panneau de détails
- Corrections mineures sur la structuration des données

**Contribution de la tutrice de stage** :
- Constitution et importation du jeu de données RPU (dossier `data/`)
- Liaison sémantique entre les organes, catégories intermédiaires et codes finaux
- Validation métier

Publication de ce dépôt réalisée **avec l'accord explicite de la tutrice de stage**.

## Fonctionnalités

- **Visualisation interactive** : graphe explorable, organisé du général (grandes catégories/organes) au spécifique (codes RPU).
- **Filtres** : par organe / catégorie.
- **Recherche avec autocomplétion** pour trouver un terme précis.
- **Panneau de détails** : au clic sur un nœud, affichage de la définition, du terme intermédiaire et du code RPU final.
- **Optimisations de rendu** pour gérer de grands volumes de données.

## Stack technique

- Python 3.9+
- PySide6 (interface Qt)
- PyVis (rendu graphe interactif dans une WebView intégrée)
- Pandas (chargement et traitement des données)

## Confidentialité

Les fichiers du dossier `data/` sont **génériques** et ne contiennent aucune information nominative de patient. Ils reposent sur des nomenclatures médicales standardisées (RPU) et une organisation hiérarchique par organe/catégorie qui n'est pas spécifique à un établissement.

Publication réalisée avec l'accord du Centre Hospitalier de Cahors.

## Structure

```
├── main.py               # Point d'entrée
├── test_mindmap.py       # Tests
├── data/                 # Nomenclature RPU structurée
├── ui/                   # Widgets et interface PySide6
├── utils/                # Fonctions utilitaires
├── visualization/        # Rendu PyVis
├── docs/
│   ├── user_guide.md
│   └── developer_guide.md
├── requirements.txt
└── .gitignore
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate     # macOS/Linux
# ou : .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Lancement

```bash
python main.py
```

## Documentation

- **[Guide utilisateur](docs/user_guide.md)** — installation et utilisation.
- **[Guide développeur](docs/developer_guide.md)** — architecture, extension.

## Licence

MIT — voir [LICENSE](LICENSE).
