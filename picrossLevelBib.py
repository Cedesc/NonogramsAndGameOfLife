import random

""" Grundfunktionen """
def levelAnzeigen(level):
    for zeile in level:
        print(zeile)
    return

def zufaelligesLevel(weite, hoehe):
    resultlevel = []
    for y in range(hoehe):
        zeile = []
        for x in range(weite):
            zeile.append(random.randint(0,1))
        resultlevel.append(zeile)
    return resultlevel

def zufaelligesLevelMitSchwierigkeit(weite, hoehe, schwierigkeit):  # leichter: negative Zahl, schwerer: positive Zahl
    # abs(schwierigkeit) viele zufaellige Level erstellen. Fuer leichtere Level, die mit den meisten schwarzen Feldern,
    # fuer schwierigere, die mit den wenigsten schwarzen Feldern zurueckgeben
    zufaelligeLevel = []
    for i in range(abs(schwierigkeit)):
        templevel = zufaelligesLevel(weite, hoehe)
        zaehler = 0
        for j in templevel:
            for k in j:
                if k == 1:
                    zaehler += 1
        zufaelligeLevel.append((templevel, zaehler))
    if schwierigkeit < 0:
        maxim = zufaelligeLevel[0]
        for i in zufaelligeLevel:

            if i[1] > maxim[1]:
                maxim = i

        return maxim[0]
    if schwierigkeit > 0:
        mindest = zufaelligeLevel[0]
        for i in zufaelligeLevel:
            if i[1] < mindest[1]:
                mindest = i
        return mindest[0]

""" Beispiel-Level """
beispiellevel = [[0,1,1,1,0],
                 [0,0,1,0,0],
                 [0,1,1,0,1],
                 [0,0,0,0,0],
                 [1,0,1,1,1],
                 [1,0,1,0,0]]

beispiellevel2 = [[0,1,1,1,1,1,0],
                  [0,1,0,1,0,1,0],
                  [0,1,0,1,0,1,0],
                  [0,1,1,1,1,1,0],
                  [0,1,0,0,0,1,0],
                  [0,1,0,0,0,1,0],
                  [0,1,0,0,0,1,0],
                  [0,1,0,0,0,1,0],
                  [0,1,0,0,0,1,0],
                  [0,1,0,0,0,1,0],
                  [1,0,0,0,0,0,1],
                  [1,1,0,1,0,1,1],
                  [0,1,1,0,1,1,0]]

beispiellevel3 = [
                 [0,1,1,1,1,1,0,
                  0,1,0,1,0,1,0],
                  [0,1,0,1,0,1,0,
                  0,1,1,1,1,1,0],
                  [0,1,0,0,0,1,0,
                  0,1,0,0,0,1,0],
                  [0,1,0,0,0,1,0,
                  0,1,0,0,0,1,0],
                  [0,1,0,0,0,1,0,
                  0,1,0,0,0,1,0],
                  [1,0,0,0,0,0,1,
                  1,1,0,1,0,1,1]]



# Smiley
nummer01 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
           ]

# kariert
nummer02 = [
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
           ]

# Spitzhacke
nummer03 = [
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
            [1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
           ]

# Kaffe
nummer04 = [
            [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
           ]

# irgendwas
nummer05 = [
            [0, 1, 0, 0, 0, 0, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
           ]