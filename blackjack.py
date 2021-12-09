## IMPORTAION MODULES ##

from math import *
from random import *
from numpy import random as nprd


## INITIALISATIONS DIVERSES ##

def paquet():
    return [
        'as de trefle', 'as de carreau', 'as de coeur', 'as de pic',
        '2 de trefle', '2 de carreau', '2 de coeur', 'as de pic',
        '3 de trefle', '3 de carreau', '3 de coeur', '3 de pic',
        '4 de trefle', '4 de carreau', '4 de coeur', '4 de pic',
        '5 de trefle', '5 de carreau', '5 de coeur', '5 de pic',
        '6 de trefle', '6 de carreau', '6 de coeur', '6 de pic',
        '7 de trefle', '7 de carreau', '7 de coeur', '7 de pic',
        '8 de trefle', '8 de carreau', '8 de coeur', '8 de pic',
        '9 de trefle', '9 de carreau', '9 de coeur', '9 de pic',
        '10 de trefle', '10 de carreau', '10 de coeur', '10 de pic',
        'valet de trefle', 'valet de carreau', 'valet de coeur', 'valet de pic',
        'dame de trefle', 'dame de carreau', 'dame de coeur', 'dame de pic',
        'roi de trefle', 'roi de carreau', 'roi de coeur', 'roi de pic'
    ]


ValCartes = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'valet': 10,
    'dame': 10,
    'roi': 10
}


def initPioche(n):
    pioche = []
    cartes = paquet()
    for i in range(n):
        pioche.extend(cartes)
    shuffle(pioche)
    return pioche


def initJoueurs(GDict, n):
    for i in range(n):
        GDict['joueurs'][i] = {}
        GDict['joueurs'][i]['nom'] = GDict['stratlist'][i]
        GDict['joueurs'][i]['type'] = 1
        GDict['joueurs'][i]['strat'] = GDict['stratlist'][i]
        GDict['joueurs'][i]['ingame'] = True
        GDict['joueurs'][i]['blackjack'] = False
        GDict['joueurs'][i]['burst'] = False


def initData(GDict, valeur, v=0):
    for i in GDict['joueurs']:
        GDict['joueurs'][i][valeur] = v
    GDict['croupier'][valeur] = v


def initVictoires(GDict):
    for i in GDict['joueurs']:
        GDict['victoires'][GDict['joueurs'][i]['nom']] = 0


## FONCTIONS DE JEU ##

def valeurCartes(carte, score):
    carte_WO_couleur = carte.split()[0]
    if carte_WO_couleur == 'as':
        return valeurAs(score)
    else:
        return ValCartes[carte_WO_couleur]


def valeurAs(score):
    if score+11 <= 21:
        return 11
    else:
        return 1


def piocheCarte(p, x=1):
    piochees = []
    for i in range(x):
        piochees.append(p.pop(0))
    return piochees


def gagnants(GDict):
    gagnants = []
    for j in GDict['joueurs']:
        if GDict['joueurs'][j]['burst']:
            continue
        elif GDict['croupier']['burst']:
            gagnants.append(j)
        elif GDict['joueurs'][j]['score'] >= GDict['croupier']['score']:
            gagnants.append(j)
    return gagnants


def gain(j, GDict):

    mise = GDict['joueurs'][j]['mise']

    # cas où je joueur dépasse 21
    if GDict['joueurs'][j]['burst']:
        GDict['croupier']['wallet'] += mise

    # cas où le croupier dépasse 21
    elif GDict['croupier']['burst']:
        if GDict['joueurs'][j]['blackjack']:
            GDict['joueurs'][j]['wallet'] += 2.5 * mise
            GDict['croupier']['wallet'] -= 1.5 * mise
        else:
            GDict['joueurs'][j]['wallet'] += 2 * mise
            GDict['croupier']['wallet'] -= mise

    # cas où le croupier fait blackjack
    elif GDict['croupier']['blackjack']:
        if GDict['joueurs'][j]['blackjack']:
            GDict['joueurs'][j]['wallet'] += 2 * mise
            GDict['croupier']['wallet'] -= mise
        else:
            GDict['croupier']['wallet'] += mise

    # cas où le croupier fait un score ≤ 21
    else:
        if GDict['joueurs'][j]['blackjack']:
            GDict['joueurs'][j]['wallet'] += 2.5 * mise
            GDict['croupier']['wallet'] -= 1.5 * mise
        elif GDict['joueurs'][j]['score'] > GDict['croupier']['score']:
            GDict['joueurs'][j]['wallet'] += 2 * mise
            GDict['croupier']['wallet'] -= mise
        elif GDict['joueurs'][j]['score'] == GDict['croupier']['score']:
            GDict['joueurs'][j]['wallet'] += mise
        else:
            GDict['croupier']['wallet'] += mise

    GDict['joueurs'][j]['mise'] = 0


## CHOIX DE PIOCHER ##

def continueAlea(j, GDict):
    if choice([False, True]):
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False


def continuePara(j, GDict, p=0.5):
    if nprd.choice([False, True], p=[1-p, p]):
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False


def continueIntel(j, GDict):
    if GDict['joueurs'][j]['score'] <= 10:
        p = 1
    elif GDict['joueurs'][j]['score'] < 21:
        p = 1-((GDict['joueurs'][j]['score']-11)/10)
    else:
        p = 0
    continuePara(j, GDict, p)


def continueCroupNormal(j, GDict):
    if GDict['joueurs'][j]['score'] < 17:
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False


def continueCroupier(GDict):
    if GDict['croupier']['score'] < 17:
        GDict['croupier']['ingame'] = True
    else:
        GDict['croupier']['ingame'] = False


def continueCroupFacile(j, GDict):
    if GDict['joueurs'][j]['score'] < 15:
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False


def continueCroupDifficile(j, GDict):
    if GDict['joueurs'][j]['score'] < 19:
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False


def selectContinue(j, GDict):
    strat = GDict['joueurs'][j]['strat']
    if strat == 'alea':
        continueAlea(j, GDict)
    elif strat == 'risk':
        continuePara(j, GDict, 0.8)
    elif strat == 'safe':
        continuePara(j, GDict, 0.2)
    elif strat == 'intel':
        continueIntel(j, GDict)
    elif strat == 'croupNormal':
        continueCroupNormal(j, GDict)
    elif strat == 'croupFacile':
        continueCroupFacile(j, GDict)
    elif strat == 'croupDiff':
        continueCroupDifficile(j, GDict)



## FONCTIONS DE DÉROULEMENT ##

def premierTour(GDict):
    for i in GDict['joueurs']:
        if GDict['joueurs'][i]['ingame'] and GDict['joueurs'][i]['type']:
            mise = 10
            GDict['joueurs'][i]['wallet'] -= mise
            GDict['joueurs'][i]['mise'] += mise
            cartes2 = piocheCarte(GDict['pioche'], 2)
            for j in cartes2:
                GDict['joueurs'][i]['score'] += valeurCartes(
                    j, GDict['joueurs'][i]['score'])
            if GDict['joueurs'][i]['score'] == 21:
                GDict['joueurs'][i]['blackjack'] = True
                GDict['joueurs'][i]['ingame'] = False

    if GDict['croupier']['ingame']:
        cartes2 = piocheCarte(GDict['pioche'], 2)
        for j in cartes2:
            GDict['croupier']['score'] += valeurCartes(
                j, GDict['croupier']['score'])
        if GDict['croupier']['score'] == 21:
            GDict['croupier']['blackjack'] = True
            GDict['croupier']['ingame'] = False


def tourJoueur(j, GDict):

    if GDict['joueurs'][j]['ingame'] and GDict['joueurs'][j]['type']:
        selectContinue(j, GDict)
        while GDict['joueurs'][j]['ingame']:
            carte = piocheCarte(GDict['pioche'])[0]
            val = valeurCartes(carte, GDict['joueurs'][j]['score'])
            GDict['joueurs'][j]['score'] += val
            if GDict['joueurs'][j]['score'] == 21:
                GDict['joueurs'][j]['ingame'] = False
            elif GDict['joueurs'][j]['score'] > 21:
                GDict['joueurs'][j]['ingame'] = False
                GDict['joueurs'][j]['burst'] = True
            else:
                selectContinue(j, GDict)


def tourComplet(GDict):
    for j in GDict['joueurs']:
        tourJoueur(j, GDict)
    continueCroupier(GDict)
    while GDict['croupier']['ingame']:
        carte = piocheCarte(GDict['pioche'])[0]
        val = valeurCartes(carte, GDict['croupier']['score'])
        GDict['croupier']['score'] += val
        if GDict['croupier']['score'] == 21:
            GDict['croupier']['ingame'] = False
        elif GDict['croupier']['score'] > 21:
            GDict['croupier']['ingame'] = False
            GDict['croupier']['burst'] = True
        else:
            continueCroupier(GDict)


def partieComplete(GDict):
    tourComplet(GDict)
    victorieux = gagnants(GDict)
    for j in GDict['joueurs']:
        gain(j, GDict)
    for j in GDict['joueurs']:
        if j in victorieux:
            GDict['victoires'][GDict['joueurs'][j]['nom']] += 1
