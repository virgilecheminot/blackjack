from blackjack import *
import matplotlib.pyplot as plt


# INITIALISATION

GDict = {
    'pioche': [],
    'stratlist': ['alea', 'risk', 'safe', 'intel', 'croupNormal', 'croupFacile', 'croupDiff'],
    'joueurs': {
        0: {
            'nom': 'nomJoueur',
            'type': 0,
            'strat': 'strategie',
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

gains = [[] for i in range(nbjoueurs)]

# PARTIE COMPLETE

nbIter = 10000
print()
avancement = 0
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

    for j in GDict['joueurs']:
        gains[j].append(GDict['joueurs'][j]['wallet'])

    if int(((i+1)/nbIter)*30) != 0:
        avancement = int(((i+1)/nbIter)*30)
        # print("\033[A                                \033[A")
        print('|'+'█'*avancement+'-'*(30-avancement)+'| '+str(round((i/nbIter)*100,1))+'%',end='\r')

# print("\033[A                             \033[A")
print("Résumé des victoires :                 ")
for j in GDict['joueurs']:
    print("-", GDict['joueurs'][j]['nom'], ":", GDict['victoires']
          [GDict['joueurs'][j]['nom']], "gain :", GDict['joueurs'][j]['wallet'])


fig1 = plt.figure(dpi=120,figsize=(7,4))
fig1.patch.set_facecolor('white')
sub1 = fig1.add_subplot(1,1,1)
for i in range(len(gains)):
    sub1.plot(gains[i],label=str(GDict['joueurs'][i]['nom']))
sub1.legend()
sub1.grid(True)

fig1.savefig('GainGraph.png')

fig2 = plt.figure(dpi=120,figsize=(7,4))
fig2.patch.set_facecolor('white')
plt.subplots_adjust(bottom=0.15)
vic = []
lose = []
nom = []
for i in GDict['victoires']:
    nom.append(i)
    vic.append(GDict['victoires'][i])
    lose.append(nbIter - GDict['victoires'][i])

plt.bar(nom,vic,0.7)
plt.xticks(rotation='20')
plt.grid(True,'both','y')

plt.savefig('WinStrat.png')


print("Vous avez terminé, le jeu va maintenant se fermer.")
