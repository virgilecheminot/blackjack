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

nbIter = 1000
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

print("Résumé des victoires :")
for j in GDict['victoires']:
    print("-", j, ":", GDict['victoires'][j])

print("Vous avez terminé, le jeu va maintenant se fermer.")
