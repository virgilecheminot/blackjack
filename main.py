from blackjack import *


# INITIALISATION

GDict = {
    'pioche': [],
    'stratlist':['alea', 'risk', 'safe', 'intel', 'croupNormal', 'croupFacile', 'croupDiff'],
    'joueurs': {
        0: {
            'nom': 'nomJoueur',
            'type': 0,
            'strat':'strategie',
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

nbjoueurs = len(GDict['stratlist'])
initJoueurs(GDict, nbjoueurs)
# AJOUTER CHOIX DE STRATÉGIES DE JEU
initVictoires(GDict)
initData(GDict, 'wallet')


# PARTIE COMPLETE

nbIter = 10000
print()
for i in range(nbIter):
    initData(GDict, 'score')
    GDict['pioche'] = initPioche(nbjoueurs+1)
    initData(GDict, 'mise')
    initData(GDict, 'ingame', True)
    initData(GDict, 'blackjack', False)
    initData(GDict, 'burst', False)

    # PREMIER TOUR

    premierTour(GDict)
    partieComplete(GDict)
    print ("\033[A                             \033[A")
    avancement = int(((i+1)/nbIter)*30)
    print('█'*avancement+'░'*(30-avancement))

print("Résumé des victoires :")
for j in GDict['joueurs']:
    print("-", GDict['joueurs'][j]['nom'], ":", GDict['victoires'][GDict['joueurs'][j]['nom']],"gain :",GDict['joueurs'][j]['wallet'])

print("Vous avez terminé, le jeu va maintenant se fermer.")
