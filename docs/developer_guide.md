# Guide Développeur

Ce document est destiné à vous donner une vue d'ensemble de l'architecture du projet Emergency Coding Navigator et de la manière dont les différentes briques interagissent entre elles.

## Architecture et arborescence

Le code est découpé de manière modulaire pour faciliter la maintenance :

- **`main.py`** : C'est le point d'entrée de l'application. Il initialise l'application PySide6 et lance la fenêtre principale.
- **`ui/`** : Contient tout ce qui touche à l'interface graphique.
  - **`main_window.py`** : Définit la classe `MainWindow`. Elle gère la mise en page, les actions de l'utilisateur (recherche, liste déroulante) et la communication avec la vue web intégrée. C'est aussi ici qu'on trouve `CustomWebEnginePage`, qui permet d'intercepter les clics faits dans le graphe JavaScript.
- **`data/`** : Gère l'import et le traitement des données.
  - **`loader.py`** : S'occupe de lire le fichier Excel brut.
  - **`processor.py`** : Contient les fonctions de nettoyage, de normalisation et de filtrage des données avant qu'elles ne soient envoyées à la visualisation.
- **`visualization/`** : S'occupe de la génération du graphe.
  - **`mindmap.py`** : Utilise la bibliothèque PyVis pour générer la carte mentale en HTML. Ce script injecte également du JavaScript personnalisé pour gérer les clics, les effets de focus et la mise en surbrillance directement dans le navigateur, ce qui permet de garder de très bonnes performances.
- **`utils/`** : Contient des petits scripts utilitaires.
  - **`path_manager.py`** : Gère les chemins de fichiers dynamiquement pour éviter les chemins en dur.

## Technologies principales
- **PySide6** : Framework utilisé pour créer l'interface graphique de bureau native.
- **PyVis / Vis.js** : Librairie utilisée pour le graphe interactif. Le rendu HTML est ensuite intégré dans l'interface PySide6 via le composant `QWebEngineView`.
- **Pandas** : Indispensable ici pour manipuler, filtrer et nettoyer les données issues du fichier Excel.

## Communication entre Python et JavaScript
La partie la plus complexe du projet est l'interactivité entre la vue web (JavaScript) et le code Python. Voici comment cela fonctionne lorsqu'on clique sur un nœud :
1. Le code JavaScript injecté via `mindmap.py` détecte le clic.
2. Il modifie l'URL de la page web avec un format personnalisé, par exemple : `pyvis://click?node=<id_du_noeud>`.
3. Du côté Python (dans `ui/main_window.py`), la classe `CustomWebEnginePage` intercepte cette tentative de navigation. Si elle détecte le préfixe `pyvis`, elle annule la navigation, récupère l'identifiant du nœud et émet un signal PyQt (`node_clicked`).
4. La fenêtre principale reçoit ce signal et met à jour le panneau de détails en fonction du nœud cliqué.

## Pistes d'amélioration et maintenance
- **Changer de jeu de données** : Si vous devez utiliser de nouvelles données, la logique est centralisée dans le dossier `data/`. Assurez-vous que le nouveau DataFrame possède bien les colonnes attendues (`organe`, `type_atteinte`, `intermediaire`, `definition`, `code`), ou adaptez le code dans `visualization/mindmap.py`.
- **Modifier le comportement physique du graphe** : Les paramètres physiques du graphe (gravité, longueur des liens, etc.) se trouvent sous forme de chaîne JSON passée à `net.set_options()` dans le fichier `visualization/mindmap.py`.
- **Modifier le design de l'interface** : L'apparence de l'interface est gérée avec du QSS (l'équivalent CSS pour Qt), que vous retrouverez directement dans la classe `MainWindow` du fichier `ui/main_window.py`.
