# Guide Utilisateur

Bienvenue sur la documentation d'utilisation de l'Emergency Coding Navigator. Ce guide est là pour vous aider à prendre en main l'application rapidement.

## Lancer l'application
Pour démarrer l'outil, ouvrez votre terminal, placez-vous dans le dossier du projet et exécutez la commande suivante :
```bash
python main.py
```
La fenêtre principale va s'ouvrir.

## Tour d'horizon de l'interface
L'interface est divisée en deux parties :
1. **Le panneau de gauche** : Il contient les filtres, la barre de recherche et la carte mentale interactive.
2. **Le panneau de droite** : Il sert à afficher le détail des informations du nœud que vous avez sélectionné.

## Comment utiliser l'outil

### Filtrer par organe
En haut à gauche de l'interface, vous trouverez un menu déroulant. Il vous permet de sélectionner un organe en particulier. C'est très utile pour réduire la taille du graphe et ne garder que les informations qui vous intéressent sur le moment.

### Chercher une information
Juste en dessous de ce menu, une barre de recherche intelligente est à votre disposition.
- Commencez à taper un mot (une maladie, un code, une partie d'une définition).
- Choisissez l'un des termes proposés par l'autocomplétion.
- Le graphe se recentrera et mettra en évidence le résultat de votre recherche.

### Manipuler la carte mentale
- **Zoomer** : Utilisez la molette de votre souris pour zoomer ou dézoomer.
- **Se déplacer** : Cliquez sur un espace vide du graphe et maintenez le clic pour faire glisser la vue.
- **Sélectionner un nœud** : Cliquez simplement sur un élément. Le graphe va alors se concentrer sur cet élément et ses liens directs (parents et enfants), en grisant le reste. Le panneau de droite se mettra à jour avec toutes les informations correspondantes (Organe, Type, Intermédiaire, Définition et Code).

### Remettre à zéro
Si vous voulez annuler votre recherche ou vos filtres et revenir à la vue par défaut, il vous suffit de cliquer sur le bouton "Réinitialiser".

## Résolution des problèmes courants
- **Aucun résultat** : Si votre recherche ou votre filtre ne donne rien, le message "Aucun résultat" apparaîtra au milieu de l'écran. Essayez de taper un mot plus générique ou cliquez sur Réinitialiser.
- **Lenteurs** : Pour des questions de performances, le graphe est limité à l'affichage des 2000 premiers éléments. Si vous sentez que l'application ralentit, n'hésitez pas à utiliser le filtre par organe pour réduire la quantité de données affichées.
