from blackjack import *


# INITIALISATION

GDict = {
    'pioche': [],
    'joueurs': {
        0: {
            'nom': '',
            'type': 0,
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


while True:
    try:
        nbjoueurs = int(input('Nombre de joueurs : '))
    except:
        print("Entrez une valeur correcte")
        continue
    else:
        break

initJoueurs(GDict, nbjoueurs)
# AJOUTER CHOIX DE STRATÉGIES DE JEU
initVictoires(GDict)
initScores(GDict, 'wallet', 100)


# PARTIE COMPLETE

rejouer = True
while rejouer:
    initScores(GDict, 'score')
    GDict['pioche'] = initPioche(nbjoueurs+1)
    initScores(GDict, 'mise')
    initScores(GDict, 'ingame', True)

    # PREMIER TOUR

    premierTour(GDict)
    partieComplete(GDict)

    while True:
        rep = input("Voulez vous lancer une nouvelle partie ? (o/n)")
        if rep != 'o' and rep != 'n':
            continue
        else:
            break
        
    if rep == 'o':
        rejouer = True
    else:
        rejouer = False
    if rejouer:
        voulezVousPartir(GDict)
        if len(GDict['joueurs']) == 0:
            rejouer = False

print("Vous avez terminé, le jeu va maintenant se fermer.")
