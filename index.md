## Jeu du Backjack

Ce jeu de Blackjack est un travail de groupe réalisé pour l'université dans le carde d'un projet de fin de semestre en INF101. Le but était de créer un jeu de Blackjack fonctionnel et se rapprochant le plus possible d'un jeu de Blackjack réel. 

Lors de la création du programme nous avons ajouté progressivements certaines fonctionnalités que nous allons détailler ici. La structure choisie a été de créer un fichier [`blackjack.py`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py) pour stocker toutes les fonctions de jeu et un autre [`main.py`](https://github.com/virgilecheminot/blackjack/blob/master/main.py) pour les exécuter dans l'ordre.

### Déroulement de base du jeu

Le jeu de Blackjack est un jeu assez simple en soi, donc sa réalisation est plutôt simple à traduire en code. En simplifiant les règles du jeu officiel, nous en avons tiré un déroulement de jeu à peu près similaire à ceci :

- **Initialisation** :
  - Demande du nombre de joueurs
  - Création de la liste des joueurs
  - Choix du type de joueur (humain ou ordinateur)
  - Choix des stratégies de jeu des joueurs ordinateurs
  - Création du portefeuille de chaque joueur à 100 OtterCoins

- **Partie complète :** (tant que rejouer vrai)
  - Scores initialisés à 0 avec la liste des joueurs de base
  - Création de pioche avec nb joueurs × paquet
  - **Premier tour :** (× nb de joueurs)
    - Création de la main initiale des joueurs (2 cartes) & main du croupier
    - Ajout de la main aux scores
    - Affiche nom du joueur
    - Affiche main du joueur
    - Demande la mise au joueur (si portefeuille non vide)
  - **Premier tour ordinateur :**
    - Affiche nom du joueur
    - Affiche main du joueur
    - Choix de la mise en fonction de la stratégie choisie
  - **Tour global :** (tant que tous les joueurs sont en jeux ou pas de victoire)
    - **Tour joueur :** (× nb de joueurs encore en jeu)
      - Affiche nom du joueur
      - Affiche main du joueur
      - Propose de continuer
        - si non : statut "en jeu" du joueur faux → sortir
      - Pioche une carte et lit sa valeur
      - Rajouter valeur de la carte
        - si > 21 → défaite : retirer joueur des scores et de la liste
        - si = 21 → victoire : fin de la partie
        - si < 21 → continuer
    - **Tour ordinateur :**
      - Choix de continuer ou pas en fonction de la stratégie de jeu
      - Même processus que joueur normal
    - Vérifier la victoire
  - Si pas de gagnant : comparaison des scores
    - Si égalité : ajouter une victoire pour tout le monde
  - Répartition des mises en fonction des scores et du vainqueur
  - Afficher le vainqueur
  - Demander pour une nouvelle partie
    - Si oui : demander à chaque joueur humain s'il veut quitter la partie

- **Fin de partie :**
  - Afficher les victoires
  - Afficher les OtterCoins restants dans chaque portefeuille


Les différentes parties distinctes du jeu sont exécutées avec les fonctions suivantes :

- `PremierTour()` : réalise le premier tour
- `partieComplete()` : exécute en boucle la fonction `tourComplet()`
| `tourComplet()` : éxecute en boucle la fonction `tourJoueur()` puis le tour du croupier

