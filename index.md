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
      - Propose de continuer à piocher
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
- `tourComplet()` : éxecute en boucle la fonction `tourJoueur()` puis le tour du croupier

### Structure des données de jeu

L'enjeu majeur de ce programme était de savoir comment stocker les données de jeu et poucoir y accéder facilement avant, durant et après la partie et pouvoir les modifier le plus facilement possible. Pour cela nous avons décidé de nous tourner vers les dictionnaires. Ne pouvant pas utiliser les classes et les objets, les dictionnaires semblaient être la meilleur alternative.

Nous avons donc décidé de séparer les données en deux dictionnaires : `GDict` où sont stockées toutes les données liées au jeu en lui-même, par exemple la pioche, l'état de la partie (terminée ou pas), etc. ainsi que `JDict` où sont toutes les informations liées aux joueurs et au croupier, comme le score actuel, ne nombre de victoires, la mise, etc.

Les dictionnaires prennent la forme suivante :

```py
GDict = {
    'nbtour': 0,
    'pioche': [],
    'partieFinie': False
}

JDict = {
    'joueurs': {
        0: {
            'nom': 'NomJoueur',
            'type': 0,
            'score': 0,
            'wallet': 100,
            'mise': 0,
            'ingame': True
        },
    },
    'croupier': {
        'score': 0,
        'wallet': 100,
        'mise': 0,
        'ingame': True
    },
    'victoires': {}
}
```

Les informations liées au joueur comme le score ne sont pas stockées dans un dictionnaire pour chaque, mais dans le dictionnaire personnel du joueur. Cela rallonge quelque peu l'écriture du code mais offre une bien plus grande flexibilité dans l'ajout futur de nouvelles informations.

Les données joueurs sont :

- `nom` : stocke le nom du joueur car la clé du dictionnaire n'est pas le nom mais un index (plus facile pour le déroulement du jeu)
- `type` : stocke le type du joueur : soit humain (0), soit ordinateur (1)
- `score` : stocke le score courant du joueur
- `wallet` : stocke le portefeuille du joueur (initialisé à 100)
- `mise` : stocke la mise courante du joueur
- `ingame` : booléen définissant si le joueur est encore dans la partie et continue à piocher ou non

À noter que le dictionnaire `victoires` n'est pas dans le dictionnaire du joueur : cela permet de potentiellement exporter le dictionnaire dans un fichier et pouvoir ré afficher le compte de victoires au nouveau lancement du programme.

Pour appeler une donnée dans une fonction particulière, seul les variables `JDict` et `GDict` sont nécessaires dans les paramètres. Une donnée s'appelle comme suit : `JDict['joueurs'][indexDuJoueur][cléDeLaDonnée]`. Les propriétés du dictionnaire permettent donc d'accéder facilement à toutes les données et d'être accédé via une boucle for, par ex :

```py
for j in JDict['joueurs']:
  JDict['joueurs'][j]['scores'] = 0
```

### Les fonctions de jeu

Le fonctionnement du jeu repose sur différentes fonctions créées dans le programme `blackjack.py`. Mise à part les fonctions de déroulement de jeu, elles servent à tout ce qui est gestion du jeu et calcul de différentes variables et données.

- `initPioche(n)` initialise une pioche composée de n paquets de 52 cartes, n étant le nombre de joueurs dans la partie. La pioche est mélangée avant d'être renvoyée grâce à la fonction `shuffle(pioche)`.

- `initJoueurs(JDict, n)` initialise les joueurs et une partie des données le concernant dans le dictionnaire `JDict['joueurs']`. La fonction demande à l'utilisateur : le nom du joueur, son type, et sa stratégie de jeu.

- `initScores(JDict, valeur, v=0)` est une fonction multi-usage qui est utilisée pour initialiser notamment les scores, les mises et les portefeuilles des joueurs. Le paramètre `v` est la valeur initialisée (par ex : 0 pour les scores ou 100 pour les portefeuilles)

 - `initVictoires(JDict)` est une fonction similaire à la précédente qui ne marche que pour les victoires

 - `valeurCartes(carte, score)` se base sur la chaine de caractère de la carte piochée et un dictionnaire de valeurs pour renvoyer la valeur entière de la carte

 - `valeurAs(score)` prend en compte le score du joueur et renvoie 1 si le score est trop haut ou 11 si le score est inférieur ou égal à 10

 - `piocheCarte(p, x=1)` prend la première carte de la liste `pioche`, la supprime de la pioche et la renvoie

 - `gagnant(JDict)` détermine le vainqueur de la partie en se basant sur les scores des joueurs et du croupier. Cette fonction correspond essentiellement à une fonction `max()` revisitée

 - `partieFinie(GDict, JDict)` renvoie un booléen indiquant si la partie est terminée ou non, donc si il reste des joueurs en jeu ou non