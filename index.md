## Jeu du Backjack

Ce jeu de Blackjack est un travail de groupe réalisé pour l'université dans le carde d'un projet de fin de semestre en INF101. Le but était de créer un jeu de Blackjack fonctionnel et se rapprochant le plus possible d'un jeu de Blackjack réel. 

Lors de la création du programme nous avons ajouté progressivements certaines fonctionnalités que nous allons détailler ici. La structure choisie a été de créer un fichier [`blackjack.py`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py) pour stocker toutes les fonctions de jeu et un autre [`main.py`](https://github.com/virgilecheminot/blackjack/blob/master/main.py) pour les exécuter dans l'ordre.

### Table des matières

- #### [Déroulement de base du jeu](#deroulement)
- #### [Structure des données de jeu](#structure)
- #### [Filtrage des inputs](#filtrage)
- #### [Les fonctions de jeu](#fonctions)
- #### [Stratégies de pioche](#pioche)
- #### [Stratégies de choix de la mise](#mises)
- #### [Tournoi automatique et comparaison des stratégies](#statistiques)
- #### [Interface graphique du jeu](#interface)

### <a name="deroulement"></a> Déroulement de base du jeu

Le jeu de Blackjack est un jeu assez simple en soi, donc sa réalisation est plutôt simple à traduire en code. En simplifiant les règles du jeu officiel, nous en avons tiré un déroulement de jeu à peu près similaire à ceci :

- **Initialisation** :
  - Demande du nombre de joueurs
  - Création de la liste des joueurs
  - Choix du type de joueur (humain ou ordinateur)
  - Choix des stratégies de jeu des joueurs ordinateurs
  - Création du portefeuille de chaque joueur à 100 OtterCoins

- **Partie complète :** (tant que rejouer vrai)
  - Scores initialisés à 0 avec la liste des joueurs de base
  - Création de pioche avec nb joueurs × paquet
  - **Premier tour :** (× nb de joueurs)
    - Demande la mise au joueur (si portefeuille non vide)
    - Création de la main initiale des joueurs (2 cartes) & main du croupier
    - Ajout de la main aux scores
    - Affiche nom du joueur
    - Affiche main du joueur
  - **Premier tour ordinateur :**
    - Choix de la mise en fonction de la stratégie choisie
    - Affiche nom du joueur
    - Affiche main du joueur
  - **Tour global :** (× nb de joueurs en jeu)
    - Affiche nom du joueur
    - Affiche main du joueur
    - **Tour joueur :** (tant que je joueur pioche)
      - Propose de continuer à piocher
        - si non : statut "en jeu" du joueur faux → sortir
      - Pioche une carte et lit sa valeur
      - Rajouter valeur de la carte
        - si > 21 → défaite : statut "en jeu" faux
        - si < 21 → continuer
    - **Tour ordinateur :** (tant que le joueur pioche)
      - Choix de continuer ou pas en fonction de la stratégie de jeu
      - Même processus que joueur normal
  - **Tour du croupier :**
    - Tour similaire à un joueur      
  - Vérifier la victoire
  - Répartition des mises en fonction des scores
  - Afficher les vainqueurs
  - Demander pour une nouvelle partie
    - Si oui : demander à chaque joueur humain s'il veut quitter la partie

- **Fin de partie :**
  - Afficher les victoires
  - Afficher les OtterCoins restants dans chaque portefeuille


Les différentes parties distinctes du jeu sont exécutées avec les fonctions suivantes :

- [`PremierTour()`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L335) : réalise le premier tour
- [`partieComplete()`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L465) : exécute la fonction `tourComplet()` puis gère la répartition des mises
- [`tourComplet()`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L445) : éxecute en boucle la fonction [`tourJoueur()`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L404) pour chaque joueur puis éxecute le tour du croupier

### <a name="structure"></a> Structure des données de jeu

L'enjeu majeur de ce programme était de savoir comment stocker les données de jeu et poucoir y accéder facilement avant, durant et après la partie et pouvoir les modifier le plus facilement possible. Pour cela nous avons décidé de nous tourner vers les dictionnaires. Ne pouvant pas utiliser les classes et les objets, les dictionnaires semblaient être la meilleur alternative.

Nous avons donc décidé de rassembler les données en un seul dictionnaire : `GDict` où sont stockées toutes les données liées au jeu en lui-même, comme la pioche ou les stratégies de jeu ; ainsi que toutes les informations liées aux joueurs et au croupier, comme le score actuel, ne nombre de victoires, la mise, etc.

Le dictionnaire prend la forme suivante :

```py
GDict = {
    'pioche': [],
    'stratlist': ['alea', 'risk', 'safe', 'intel', 'croupNormal', 'croupFacile', 'croupDiff'],
    'stratmiselist': ['miseAlea', 'miseFaible', 'miseForte'],
    'joueurs': {
        0: {
            'nom': '',
            'type': 0,
            'strat': '',
            'stratmise': '',
            'score': 0,
            'wallet': 100,
            'mise': 0,
            'ingame': True,
            'blackjack': False,
            'burst': False
        },
    },
    'croupier': {
        'score': 0,
        'wallet': 0,
        'ingame': True,
        'blackjack': False,
        'burst': False
    },
    'victoires': {}
}
```

Les informations liées au joueur comme le score ne sont pas stockées dans un dictionnaire pour chaque, mais dans le dictionnaire personnel du joueur. Cela rallonge quelque peu l'écriture du code mais offre une bien plus grande flexibilité dans l'ajout futur de nouvelles informations.

Les données joueurs sont :

- `nom` : stocke le nom du joueur car la clé du dictionnaire n'est pas le nom mais un index (plus facile pour le déroulement du jeu)
- `type` : stocke le type du joueur : soit humain (0), soit ordinateur (1)
- `strat` : stocke la stratégie de jeu choisie pour le joueur ordinateur
- `stratmise` : stocke la stratégie de choix de la mise choisie pour le joueur ordinateur
- `score` : stocke le score courant du joueur
- `wallet` : stocke le portefeuille du joueur (initialisé à 100)
- `mise` : stocke la mise courante du joueur
- `ingame` : booléen définissant si le joueur est encore dans la partie et continue à piocher ou non
- `blackjack` : booléen définissant si le joueur a effectué un Blackjack au premier tour (utile pour la répartition des mises)
- `burst` : booléen définissant si le joueur a dépassé ou non le score de 21

À noter que le dictionnaire `victoires` n'est pas dans le dictionnaire du joueur : cela permet de potentiellement exporter le dictionnaire dans un fichier et pouvoir ré afficher le compte de victoires au nouveau lancement du programme.

Pour appeler une donnée dans une fonction particulière, seul les variables `GDict` et `GDict` sont nécessaires dans les paramètres. Une donnée s'appelle comme suit : `GDict['joueurs'][indexDuJoueur][cléDeLaDonnée]`. Les propriétés du dictionnaire permettent donc d'accéder facilement à toutes les données et d'être accédé via une boucle for, par exemple :

```py
for j in GDict['joueurs']:
    GDict['joueurs'][j]['scores'] = 0
```

### <a name="filtrage"></a> Filtrage des inputs

Lors du déroulement de la partie, le jeu interagit beaucoup avec l'utilisateur pour demander, soit le nombre de joueurs, soit la mise des joueurs, etc. Il est donc nécessaire de filtrer les données entrées par l'utilisateur afin de ne pas déclencher une erreur dans le programme.

Pour ce qu'il sagit des entrées de texte, la méthode est assez simple, il suffit de faire une boucle `while` qui tourne tant que la réponse de l'utilisateur ne convient pas, comme par exemple :
```py
while True:
    strat = input(s+" (o/n) : ")
    if strat != 'o' and strat != 'n':
        continue
    else:
        break
```

Pour les entrées de valeurs entières, comme la mise ou le nombre de joueur, trier devient plus complexe. En effet, la méthode simple comme ci-dessus ne convient pas car on ne peut pas vérifier facilement si une chaine de caractère est un entier correct ou non. Aussi, lorsque la fonction `int(input())` reçoit une valeur incorrecte, elle renvoie une erreur au lieu de simplement renvoyer `None`, ce qui a pour inconvénient de stopper le programme.

Pour pallier à cela, nous avons utilisé une méthode que nous n'avons pas vu en cours : les erreurs et exceptions. Cela utilise en plus les instructions `try` et `except` :
```py
while True:
    try:
        nbjoueurs = int(input('Nombre de joueurs : '))
    except:
        print("Entrez une valeur correcte")
        continue
    if nbjoueurs <= 0:
        print("Le nombre de joueurs doit être supérieur à 0")
        continue
    else:
        break
```

Ces deux méthodes assez similaires font en sorte qu'aucune erreur ne soit déclenchée directement par l'utilisateur, ce qui est important notamment lors de la phase de testage du programme.

### <a name="fonctions"></a> Les fonctions de jeu

Le fonctionnement du jeu repose sur différentes fonctions créées dans le programme [`blackjack.py`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py). Mise à part les fonctions de déroulement de jeu, elles servent à tout ce qui est gestion du jeu et calcul de différentes variables et données.

- [`initPioche(n)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L44) initialise une pioche composée de n paquets de 52 cartes, n étant le nombre de joueurs dans la partie. La pioche est mélangée avant d'être renvoyée grâce à la fonction `shuffle(pioche)`.

- [`initJoueurs(GDict, n)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L53) initialise les joueurs et une partie des données le concernant dans le dictionnaire `GDict['joueurs']`. La fonction demande à l'utilisateur : le nom du joueur, son type, et sa stratégie de jeu.

- [`initData(GDict, valeur, v=0)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L126) est une fonction multi-usage qui est utilisée pour initialiser notamment les scores, les mises et les portefeuilles des joueurs. Le paramètre `v` est la valeur initialisée (par ex : 0 pour les scores ou 100 pour les portefeuilles).

- [`initVictoires(GDict)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L132) est une fonction similaire à la précédente qui ne marche que pour les victoires, comme elles sont dans un dictionnaire à part.

- [`valeurCartes(carte, score)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L139) se base sur la chaine de caractère de la carte piochée et un dictionnaire de valeurs pour renvoyer la valeur entière de la carte.

- [`valeurAs(score)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L147) prend en compte le score du joueur et renvoie 1 si le score est trop haut ou 11 si le score est inférieur ou égal à 10.

- [`piocheCarte(p, x=1)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L154) prend la première carte de la liste `pioche`, la supprime de la pioche et la renvoie. Le paramètre `x` détermine le nombre de cartes à piocher.

- [`gagnant(GDict)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L161) détermine les joueurs qui ne perdent pas leur mise à la fin de la partie en cours et renvoie une liste avec les indexs des joueurs.

- [`gain(j, GDict)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L173) est une fonction composée d'une série de `if` qui se base sur les règles du jeu pour mettre à jour le portefeuille des joueurs en fonction de leur score (voir la section [Stratégies de choix de la mise](#mises))

### <a name="pioche"></a> Stratégies de pioche

Les stratégies de pioches sont utilisées pour les joueurs ordinateur ou pour le croupier. Ce sont en fait des fonctions qui déterminent si le joueur doit continuer à piocher ou non, basé sur certains critères. 

- [`continueHuman(j, GDict)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L216) est la fonction de base qui interagie avec le joueur pour lui demander s'il veut continuer à piocher ou pas

- [`continueAlea(j,GDict)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L227) ne prend aucun critère en compte et donne juste au hasard une réponse positive ou négative avec une probabilité de 0.5. C'est la forme la moins "intelligente" des fonctions de choix :
```py
def continueAlea(j,GDict):
    if choice([False, True]):
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")
```

- [`continuePara(j,GDict,p=0.5)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L235) est similaire à la fonction précédente, mais les choix ont une probabilité différente (même si la probabilité par défaut est 0.5, ce qui revient à exactement la fonction précédente). Ce choix pondéré est effectué grâce au module numpy.random :
```py
def continuePara(j,GDict,p=0.5):
    if nprd.choice([False, True], p=[1-p, p]):
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")
```

- [`continueIntel(j,GDict,p=0.5)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L243) se base sur le score du joueur pour en tirer une probabilité qui est en suite injectée dans `continuePara()`. C'est la technique la plus "complexe" car elle rassemble le plus de paramètres, mais ça n'es pas forcément la plus logique ni la meilleure stratégie :
```py
def continueIntel(j,GDict):
    if GDict['joueurs'][j]['score'] <= 10:
        p = 1
    elif GDict['joueurs'][j]['score'] < 21:
        p = 1-((GDict['joueurs'][j]['score']-11)/10)
    else:
        p = 0
    continuePara(j,GDict,p)
```
- [`continueCroupier(GDict)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L261) est la méthode utilisée dans la plupart des casinos quand il s'agit de faire piocher le croupier. Tant que son score est inférieur à 17, le croupier continue à piocher, sinon il s'arrête. C'est la méthode imposée au croupier de notre programme :
```py
def continueCroupier(GDict):
    if GDict['croupier']['score'] < 17:
        GDict['croupier']['ingame'] = True
    else:
        GDict['croupier']['ingame'] = False
        print("\nLe croupier ne pioche pas")
```
- [`continueCroupNormal(GDict)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L253) est la même methode utilisé dans la fonction précédente, cependant elle est appliquée à un joueur qui voudrait jouer comme le croupier :
```py
def continueCroupNormal(j, GDict):
    if GDict['joueurs'][j]['score'] < 17:
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")
```
- [`continueCroupFacile(j,GDict)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L269) est la fonction qui definit un joueur qui ne pioche que quand sa main a une valeur strictement inférieure à 16. C'est donc un moyen simple et sécurisé de piocher :
```py
def continueCroupFacile(j, GDict):
    if GDict['joueurs'][j]['score'] < 16:
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")
```
- [`continueCroupDifficile(j,GDict)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L277) fonctionne comme celle au dessus mais avec une valeur de main plus élevée avant d'arrêter de piocher. C'est plus risqué mais paut parfois permettre de vaincre le croupier :
```py
def continueCroupDifficile(j, GDict):
    if GDict['joueurs'][j]['score'] < 19:
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")
```

### <a name="mises"></a> Stratégies de choix de la mise

Le fonctionnement des mises demandé ne correspond pas du tout au fonctionnement des mises du Blackjack classique, faisant jouer les joueurs contre eux et non contre le croupier. C'est pourquoi nous avons décidé de revoir le système avec les règles suivantes :

- Le croupier ne mise pas et comme il représente le casino, il a une ressource "infinie" d'OtterCoins

- Si le joueur dépasse, il perd sa mise instantanément sa mise qui va au croupier

- Si le joueur fait blackjack en un coup, il gagne 1,5 fois sa mise, sauf si le croupier fait aussi blackjack en un coup, au quel cas le joueur est payé à égalité

- Si le joueur a une main supérieure au croupier, il est payé à égalité, c'est à dire qu'il récupère sa mise et gagne la valeur de sa mise

- Si le croupier dépasse, il paye toutes les mains encore en jeu à égalité

- Si le joueur est a égalité avec le croupier, la main est considérée comme nulle et le joueur récupère juste sa mise

De même que les stratégie de pioche, les stratégies de mises peuvent être choisies au moment de l'inscription du joueur ordinateur dans le dictionnaire. Elles déterminenent donc combien d'OtterCoins le joueur va miser en fonction de différents critères.

- [`miseAlea(j, Gdict)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L305) effectue un choix de la mise aléatoirement entre 1 et le portefeuille du joueur :
```py
def miseAlea(j, Gdict):
    return randint(1, floor(Gdict['joueurs'][j]['wallet']))
```
- [`miseFaible(j, Gdict)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L309) effectue un choix de la mise dite "Faible", car il effectue son choix afin qu'elle soit inférieur au quart du portefeuille du joueur :
```py
def miseFaible(j,GDict):
    mise = randint(1 ,floor(GDict['joueurs'][j]['wallet']))
    while mise >((1/4)*(GDict['joueurs'][j]['wallet'])):
        mise = randint(1 ,floor(GDict['joueurs'][j]['wallet']))
    return mise
```
- [`miseForte(j, Gdict)`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py#L316) effectue un choix de la mise dite "Forte", car il effectue son choix afin qu'elle soit supérieure au trois quart du portefeuille du joueur :
```py
def miseForte(j,GDict):
    mise = randint(1 ,floor(GDict['joueurs'][j]['wallet']))
    while mise <((3/4)*(GDict['joueurs'][j]['wallet'])):
        mise = randint(1 ,floor(GDict['joueurs'][j]['wallet']))
    return mise
```

### <a name="statistiques"></a> Tournoi automatique et comparaison des stratégies

Nous allons à présent étudier différentes possibilités de jeux, afin de voir quelle(s) stratégie(s) de mises et/ou de pioches sont les meilleurs pour gagner face au croupier. Pour procéder à cela, nous avons créé une nouvelle branche du jeu (se trouvant [ici](https://github.com/virgilecheminot/blackjack/tree/stats)). Le programme a été complètement simplifié en enlevant tous les affichages console et les interractions avec l'utilisateur, et en enlevant le code concernant les joueurs humains.

Afin de tester toutes les stratégies, le programme principal créé un joueur ordinateur par stratégie et effectue un nombre n de parties affin de comparer le nombre de victoires et les gains pour chaques stratégies.

On utilise ensuite le module matplotlib pour tracer des graphiques avec les valeurs obtenues. On notera le nombre de victoires sous forme d'un histograme et les gains sous forme d'un graphique évoluant à chaque partie effectuée. On effectue 10 000 parties d'affilées pour avoir un résultat se rapprochant le plus possible de la probabilité de réussite de la stratégie.

![Graphique des gains](https://raw.githubusercontent.com/virgilecheminot/blackjack/stats/GainGraph.png) 
![Histogramme des Victoires](https://raw.githubusercontent.com/virgilecheminot/blackjack/stats/WinStrat.png)

On remarque que la stratégie de jeu la plus efficace est finalement `croupFacile`, similaire à celle du croupier, avec un score d'arrêt légèrement plus faible. Cependant, dans certains autres tests, c'est la stratégie `croupNormal` qui l'emportait de peu. C'est donc une de ces stratégies qu'il faudrait choisir, car en plus de cela, le taux de victoire est supérieur à 50%.

Au contraire, la stratégie `risk` qui consiste à continuer à piocher huit fois sur 10 est la pire, car c'est celle qui fait que le joueur dépasse le plus souvent.

On remarque aussi, que qu'importe la stratégie, le gain est toujours négatif et donc le casino s'en sort toujours avec un gain positif.

### <a name="interface"></a> Interface graphique du jeu

(à venir)
