import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen, QImage, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QEvent, QRect, QPointF, QPropertyAnimation, QTimer
import copy
import picrossSettings as ps


""" 
Erklaerung: 
    - 3 geschachtelte Listen mit Tiefe 2, 1. mit der Loesung, 2. mit dem momentanen Stand, 3. mit Koordinaten
    - linke Maustaste um Feld zu bestaetigen, rechte Maustaste um Feld zu blocken
"""




class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.wW = ps.FENSTERBREITE       # wW = windowWidth
        self.wH = ps.FENSTERHOEHE        # wH = windowHeight
        self.setGeometry(500, 30, self.wW, self.wH)
        self.setWindowTitle("Picross")
        self.loesung = ps.LEVEL

        self.nachUnten = self.wH // 8     # Gesamtverschiebung nach unten
        self.nachRechts = self.wW // 8    # Gesamtverschiebung nach rechts
        self.anzahlZeilen = len(self.loesung)
        self.anzahlSpalten = len(self.loesung[0])
        self.level = self.leeresLevelErstellen()
        self.levelKoordinaten = self.koordinatenBestimmen()
        self.hinweiseSpalten, self.hinweiseZeilen = self.hinweiseErstellen()
        self.gewonnen = False
        self.creatorModeAn = False
        self.hinweiseInZahlenZeilenSpalten = self.hinweiseInZahlenAendern()

        for i in range(self.anzahlZeilen):
            self.zeileabgeschlossen(i)
        for j in range(self.anzahlSpalten):
            self.spalteabgeschlossen(j)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.hinweiseInZahlenAendern()

        self.keyPressEvent = self.fn
        self.show()


    def paintEvent(self, event):
        painter = QPainter(self)

        ''' Hintergrund '''
        painter.fillRect(0, 0, self.wW, self.wH, QColor(205, 205, 205))
        if self.gewonnen:
            painter.fillRect(0, 0, self.wW, self.wH, QColor(155, 205, 155))
            self.gewinnAnimation()


        ''' Netz aufbauen '''
        painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))

        # vertikale Linien
        breite = (self.wW - 2 * self.nachRechts) // self.anzahlSpalten
        for verschiebung in range(self.anzahlSpalten + 1):
            if verschiebung == 0 or verschiebung == self.anzahlSpalten:
                painter.setPen(QPen(QColor(0, 0, 0), 4, Qt.SolidLine))
                painter.drawLine(self.nachRechts + breite * verschiebung,
                                 self.nachUnten // 2,
                                 self.nachRechts + breite * verschiebung,
                                 self.wH - self.nachUnten // 2)
                painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
            elif verschiebung % 5 == 0:
                painter.setPen(QPen(QColor(0,0,0), 3, Qt.SolidLine))
                painter.drawLine(self.nachRechts + breite * verschiebung,
                                 self.nachUnten // 2,
                                 self.nachRechts + breite * verschiebung,
                                 self.wH - self.nachUnten // 2)
                painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
            else:
                painter.drawLine(self.nachRechts + breite * verschiebung,
                                 self.nachUnten // 2,
                                 self.nachRechts + breite * verschiebung,
                                 self.wH - self.nachUnten // 2)

        # horizontale Linien
        hoehe = (self.wH - 2 * self.nachUnten) // self.anzahlZeilen
        for verschiebung in range(self.anzahlZeilen + 1):
            if verschiebung == 0 or verschiebung == self.anzahlZeilen:
                painter.setPen(QPen(QColor(0, 0, 0), 4, Qt.SolidLine))
                painter.drawLine(self.nachRechts // 2,
                                 self.nachUnten + hoehe * verschiebung,
                                 self.wW - self.nachRechts // 2,
                                 self.nachUnten + hoehe * verschiebung)
                painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
            elif verschiebung % 5 == 0:
                painter.setPen(QPen(QColor(0,0,0), 3, Qt.SolidLine))
                painter.drawLine(self.nachRechts // 2,
                                 self.nachUnten + hoehe * verschiebung,
                                 self.wW - self.nachRechts // 2,
                                 self.nachUnten + hoehe * verschiebung)
                painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
            else:
                painter.drawLine(self.nachRechts // 2,
                                self.nachUnten + hoehe * verschiebung,
                                self.wW - self.nachRechts // 2,
                                self.nachUnten + hoehe * verschiebung)


        """ Rechtecke einzeichnen """
        painter.setPen(QPen(QColor(200, 0, 0), 3, Qt.SolidLine))
        for i in range(self.anzahlZeilen):

            for j in range(self.anzahlSpalten):

                if self.level[i][j] == 1:
                    painter.fillRect(self.levelKoordinaten[i][j][0][0],
                                     self.levelKoordinaten[i][j][0][1],
                                     self.levelKoordinaten[i][j][1][0] - self.levelKoordinaten[i][j][0][0], # hoehe
                                     self.levelKoordinaten[i][j][1][1] - self.levelKoordinaten[i][j][0][1], # weite
                                     QColor(0,0,0))

                if self.level[i][j] == -1:
                    painter.setPen(QPen(QColor(200, 0, 0), 3, Qt.SolidLine))
                    painter.drawLine(self.levelKoordinaten[i][j][0][0],
                                     self.levelKoordinaten[i][j][0][1],
                                     self.levelKoordinaten[i][j][1][0],
                                     self.levelKoordinaten[i][j][1][1])
                    painter.drawLine(self.levelKoordinaten[i][j][0][0],
                                     self.levelKoordinaten[i][j][1][1],
                                     self.levelKoordinaten[i][j][1][0],
                                     self.levelKoordinaten[i][j][0][1])

                if self.level[i][j] == 2:
                    painter.setPen(QPen(QColor(100, 100, 100), 2, Qt.SolidLine))
                    painter.drawLine(self.levelKoordinaten[i][j][0][0],
                                     self.levelKoordinaten[i][j][0][1],
                                     self.levelKoordinaten[i][j][1][0],
                                     self.levelKoordinaten[i][j][1][1])
                    painter.drawLine(self.levelKoordinaten[i][j][0][0],
                                     self.levelKoordinaten[i][j][1][1],
                                     self.levelKoordinaten[i][j][1][0],
                                     self.levelKoordinaten[i][j][0][1])


        """ Hinweise einbringen """
        # Idee: an den gezeichneten Linien orientieren
        painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
        schriftgroesse = hoehe // 6
        painter.setFont(QFont("Arial", schriftgroesse))

        # Zeilen
        for zeile in range(self.anzahlZeilen):
            if self.hinweiseZeilen[zeile][1]:       # pruefen ob visible
                painter.drawText(0, self.nachUnten + hoehe * (zeile+0.5) - schriftgroesse // 2,
                                 self.nachRechts, hoehe, Qt.AlignHCenter, self.hinweiseZeilen[zeile][0])
            else:
                painter.setPen(QColor(180,180,180))
                painter.drawText(0, self.nachUnten + hoehe * (zeile + 0.5) - schriftgroesse // 2,
                                 self.nachRechts, hoehe, Qt.AlignHCenter, self.hinweiseZeilen[zeile][0])
                painter.setPen(QColor(0, 0, 0))


        # Spalten
        for spalte in range(self.anzahlSpalten):
            if self.hinweiseSpalten[spalte][1]:     # pruefen ob visible
                painter.drawText(self.nachRechts + breite * (spalte+0.5) - schriftgroesse // 2,
                                 self.nachUnten - schriftgroesse * 20,
                                 schriftgroesse * 3, schriftgroesse * 20, Qt.AlignBottom, self.hinweiseSpalten[spalte][0])
            else:
                painter.setPen(QColor(180,180,180))
                painter.drawText(self.nachRechts + breite * (spalte + 0.5) - schriftgroesse // 2,
                                 self.nachUnten - schriftgroesse * 20,
                                 schriftgroesse * 3, schriftgroesse * 20, Qt.AlignBottom, self.hinweiseSpalten[spalte][0])
                painter.setPen(QColor(0,0,0))



    def fn(self, e):
        # H druecken um Steuerung anzuzeigen
        if e.key() == Qt.Key_H:
            print("Steuerung: \n  Escape :  Fenster schliessen\n  L :  Loesung anzeigen\n  R :  Level neustarten")
            print("  C :  Creator-Mode anschalten\n  S :  Wenn der Creator-Mode an ist, wird das Level gespeichert")

        # R druecken um Level neuzustarten
        if e.key() == Qt.Key_R:
            self.levelReset()
            self.update()

        # L druecken um Loesung anzuzeigen
        if e.key() == Qt.Key_L:
            self.loesungAnzeigen()

        # esc druecken um Level zu schliessen
        if e.key() == Qt.Key_Escape:
            self.close()

        # C druecken um in Creator-Mode zu wechseln
        if e.key() == Qt.Key_C:
            if self.creatorModeAn:
                print("Bereits in Creator-Mode")
            else:
                self.creatorModeAn = True
                self.creatorModeWechseln()
                print("Creator-Mode aktiv")

        # S druecken um momentanes Level zu speichern
        if e.key() == Qt.Key_S and self.creatorModeAn:
            self.creatorModelevelSpeichern()
            print("Level abgespeichert")

        # K druecken um KI das Level loesen zu lassen
        if e.key() == Qt.Key_K:
            self.kiSchritt()
            self.update()

        if e.key() == Qt.Key_Q:
            self.alleMoeglichenLoesungenBerechnenZeile(5)
            #self.reiheUeberpruefenObMoeglicheLoesung(3, [0, 0, 0, 1, 1, 1, 1, 1, 1, 1], False)


    def mousePressEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        #print("               ", pos.x(), pos.y())     # zum ueberpruefen wo man klickt

        """ Eingaben moeglich machen """
        for i in range(self.anzahlZeilen):
            for j in range(self.anzahlSpalten):
                if ( self.levelKoordinaten[i][j][0][0] < pos.x() < self.levelKoordinaten[i][j][1][0] ) \
                and ( self.levelKoordinaten[i][j][0][1] < pos.y() < self.levelKoordinaten[i][j][1][1] ) \
                and (self.level[i][j] == 0 or self.level[i][j] == 2):

                    # Feld blocken
                    if QMouseEvent.button() == Qt.RightButton:
                        if self.level[i][j] == 0:
                            self.level[i][j] = 2
                        elif self.level[i][j] == 2:
                            self.level[i][j] = 0

                    # regulaer, wenn man was trifft und ungeblockt ist
                    if QMouseEvent.button() == Qt.LeftButton and self.level[i][j] == 0:
                        if self.loesung[i][j] == 0:     # falsches Feld
                            self.level[i][j] = -1
                        elif self.loesung[i][j] == 1:
                            self.level[i][j] = 1        # richtiges Feld
                            self.zeileabgeschlossen(i)
                            self.spalteabgeschlossen(j)

                        """ Ueberpruefen ob Level geschafft ist """
                        self.gewonnen = True
                        for i in range(self.anzahlZeilen):
                            for j in range(self.anzahlSpalten):
                                if self.loesung[i][j] == 1 and self.level[i][j] != 1:
                                    self.gewonnen = False

                    self.update()



    def leeresLevelErstellen(self):

        result = []
        for i in range(self.anzahlZeilen):
            zeile = []
            for j in range(self.anzahlSpalten):
                zeile.append(0)
            result.append(zeile)
        return result


    def koordinatenBestimmen(self):

        # Idee: Fuer jeden Eintrag jeweils linke obere und rechte untere Koordinate für ein Rechteck bestimmen.
        #       Diese als Tupel von zwei Tupeln (2 Punkte, also 4 Koordinaten) in geschachtelter Liste so platzieren,
        #       dass sie die gleichen Indizes haben, wie die zugehoerigen Werte
        result = []

        # reine Vorberechnung
        breite = (self.wW - 2 * self.nachRechts) // self.anzahlSpalten
        hoehe = (self.wH - 2 * self.nachUnten) // self.anzahlZeilen

        for i in range(self.anzahlZeilen):
            zeile = []
            for j in range(self.anzahlSpalten):

                punktLinksOben = (self.nachRechts + breite * j, self.nachUnten + hoehe * i)
                punktRechtsUnten = (self.nachRechts + breite * (j+1), self.nachUnten + hoehe * (i+1))

                zeile.append( ( punktLinksOben , punktRechtsUnten ) )
            result.append(zeile)
        return result


    def levelReset(self):
        self.level = self.leeresLevelErstellen()

        # alle Hinweise wieder schwarz machen
        # schnellere Alternative zu hinweisSichtbarkeitpruefen
        for i in range(len(self.hinweiseZeilen)):
            self.hinweiseZeilen[i][1] = True
        for i in range(len(self.hinweiseSpalten)):
            self.hinweiseSpalten[i][1] = True

        self.gewonnen = False       # hebt Sperre auf, die Verhindert, dass man neu zeichnen kann


    def loesungAnzeigen(self):
        self.level = copy.deepcopy(self.loesung)

        # alle Hinweise grau machen
        # schnellere Alternative zu hinweisSichtbarkeitpruefen
        for i in range(len(self.hinweiseZeilen)):
            self.hinweiseZeilen[i][1] = False
        for i in range(len(self.hinweiseSpalten)):
            self.hinweiseSpalten[i][1] = False

        self.update()


    def hinweiseErstellen(self):

        # Hinweise fuer Spalten erstellen
        obenHinweise = []
        for i in range(self.anzahlSpalten):
            zaehler = 0
            spalteHinweise = ""
            for j in range(self.anzahlZeilen):
                if self.loesung[j][i] == 1:
                    zaehler += 1
                else:
                    if zaehler != 0:
                        if spalteHinweise:
                            spalteHinweise += "\n" + str(zaehler)
                        else:
                            spalteHinweise = str(zaehler)

                    zaehler = 0
            if not spalteHinweise and zaehler == 0:  # wenn kein Feld schwarz ist
                spalteHinweise = "0"
            if zaehler != 0:  # wenn das letzte Feld schwarz ist
                if spalteHinweise:
                    spalteHinweise += "\n" + str(zaehler)
                else:
                    spalteHinweise = str(zaehler)
            obenHinweise.append([spalteHinweise, True])

        # Hinweise fuer Zeilen erstellen
        linksHinweise = []
        for i in range(self.anzahlZeilen):
            zaehler = 0
            zeileHinweise = ""
            for j in range(self.anzahlSpalten):
                if self.loesung[i][j] == 1:
                    zaehler += 1
                else:
                    if zaehler != 0:
                        if zeileHinweise:
                            zeileHinweise += "  " + str(zaehler)
                        else:
                            zeileHinweise = str(zaehler)

                    zaehler = 0
            if not zeileHinweise and zaehler == 0:   # wenn kein Feld schwarz ist
                zeileHinweise = "0"
            if zaehler != 0:       # wenn das letzte Feld schwarz ist
                if zeileHinweise:
                    zeileHinweise += "  " + str(zaehler)
                else:
                    zeileHinweise = str(zaehler)
            linksHinweise.append([zeileHinweise, True])

        return obenHinweise, linksHinweise


    def gewinnAnimation(self):
        print("Glueckwunsch, du hast es geschafft!")
        self.level = copy.deepcopy(self.loesung)


    def zeileabgeschlossen(self, zeile):
        # pruefen ob Zeile abgeschlossen ist, indem die schwarzen Felder der Loesung in der Zeile mit den
        # schwarzen Feldern des Levels verglichen wird
        for i in range(self.anzahlSpalten):
            if self.loesung[zeile][i] == 1:
                if self.level[zeile][i] != 1:
                    return False

        # unausgefuellter Rest der Zeile blocken
        for i in range(self.anzahlSpalten):
            if self.level[zeile][i] == 0:
                self.level[zeile][i] = 2

        # Hinweise ausgrauen
        self.hinweiseZeilen[zeile][1] = False

        return True


    def spalteabgeschlossen(self, spalte):
        # pruefen ob Spalte abgeschlossen ist mit analogem Verfahren zu zeileabgeschlossen
        for i in range(self.anzahlZeilen):
            if self.loesung[i][spalte] == 1:
                if self.level[i][spalte] != 1:
                    return False

        # unausgefuellter Rest der Spalte blocken
        for i in range(self.anzahlZeilen):
            if self.level[i][spalte] == 0:
                self.level[i][spalte] = 2

        # Hinweise ausgrauen
        self.hinweiseSpalten[spalte][1] = False

        return True


    def hinweisSichtbarkeitPruefen(self):
        for i in range(self.anzahlSpalten):
            self.spalteabgeschlossen(i)
        for i in range(self.anzahlZeilen):
            self.zeileabgeschlossen(i)


    def creatorModeWechseln(self):

        # Loesung mit nur schwarzen Feldern erstellen, damit man keinen Fehler machen kann und nicht vorher abbricht
        vollstaendigeLoesung = []
        for i in range(self.anzahlZeilen):
            zeile = []
            for j in range(self.anzahlSpalten):
                zeile.append(1)
            vollstaendigeLoesung.append(zeile)

        self.loesung = vollstaendigeLoesung

        # Level leeren
        self.level = self.leeresLevelErstellen()

        # Hinweise entfernen
        for i in range(self.anzahlZeilen):
            self.hinweiseZeilen[i][0] = ""
        for i in range(self.anzahlSpalten):
            self.hinweiseSpalten[i][0] = ""

        self.update()


    def creatorModelevelSpeichern(self):
        txtDatei = open("levelSpeicher.txt", "w")

        # alles ausser Einsen und Nullen aus der Datei entfernen
        for i in range(self.anzahlZeilen):
            for j in range(self.anzahlSpalten):
                if self.level[i][j] != 1:
                    self.level[i][j] = 0
        zuSpeicherndesLevel = "[\n"
        for i in self.level:
            zuSpeicherndesLevel += ("            " + str(i) + ",\n")
        zuSpeicherndesLevel += "           ]"
        txtDatei.write(zuSpeicherndesLevel)
        txtDatei.close()


    def neuesLevelErstellen(self):
        pass


    def hinweiseInZahlenAendern(self):
        neueHinweiseZeilen = []
        for liste in self.hinweiseZeilen:
            proZeile = []
            zahlR = ""
            for zeichen in liste[0]:
                if zeichen == " " and zahlR != "":
                    proZeile.append(int(zahlR))
                    zahlR = ""
                else:
                    zahlR += zeichen
            proZeile.append(int(zahlR))
            neueHinweiseZeilen.append(proZeile)

        neueHinweiseSpalten = []
        for liste in self.hinweiseSpalten:
            proSpalte = []
            zahlS = ""
            for zeichen in liste[0]:
                if zeichen == "\n" and zahlS != "":
                    proSpalte.append(int(zahlS))
                    zahlS = ""
                else:
                    zahlS += zeichen
            proSpalte.append(int(zahlS))
            neueHinweiseSpalten.append(proSpalte)

        return neueHinweiseZeilen, neueHinweiseSpalten


    def kiAktivieren(self):
        self.timer.start(1000)


    def kiSchritt(self):
        # eindeutige Zeilen vervollstaendigen
        for hinweisZeile in range(len(self.hinweiseInZahlenZeilenSpalten[0])):
            summeProZeile = -1
            for hinweisR in self.hinweiseInZahlenZeilenSpalten[0][hinweisZeile]:
                summeProZeile += 1 + hinweisR

            # wenn in einer Zeile kein schwarzes Feld vorhanden ist
            if summeProZeile == 0 and self.hinweiseZeilen[hinweisZeile][1]:
                self.hinweiseZeilen[hinweisZeile][1] = False
                for j in range(self.anzahlSpalten):
                    self.level[hinweisZeile][j] = 2
                return

            # wenn es in einer Zeile eine eindeutige Loesung an schwarzen Feldern gibt
            if summeProZeile == self.anzahlSpalten and self.hinweiseZeilen[hinweisZeile][1]:
                zaehlerR = 0
                for anzahlSchwarzeFelderR in self.hinweiseInZahlenZeilenSpalten[0][hinweisZeile]:
                    for schwarzesFeld in range(anzahlSchwarzeFelderR):
                        self.level[hinweisZeile][zaehlerR] = 1
                        zaehlerR += 1
                    if zaehlerR < self.anzahlSpalten:
                        self.level[hinweisZeile][zaehlerR] = 2
                        zaehlerR += 1
                self.hinweiseZeilen[hinweisZeile][1] = False
                for j in range(self.anzahlSpalten):
                    self.spalteabgeschlossen(j)
                return


        # eindeutige Spalten vervollstaendigen
        for hinweisSpalte in range(len(self.hinweiseInZahlenZeilenSpalten[1])):
            summeProSpalte = -1
            for hinweisS in self.hinweiseInZahlenZeilenSpalten[1][hinweisSpalte]:
                summeProSpalte += 1 + hinweisS

            # wenn in einer Spalte kein schwarzes Feld vorhanden ist
            if summeProSpalte == 0 and self.hinweiseSpalten[hinweisSpalte][1]:
                self.hinweiseSpalten[hinweisSpalte][1] = False
                for i in range(self.anzahlZeilen):
                    self.level[i][hinweisSpalte] = 2
                return

            # wenn es in einer Spalte eine eindeutige Loesung an schwarzen Feldern gibt
            if summeProSpalte == self.anzahlZeilen and self.hinweiseSpalten[hinweisSpalte][1]:
                zaehlerS = 0
                for anzahlSchwarzeFelderS in self.hinweiseInZahlenZeilenSpalten[1][hinweisSpalte]:
                    for schwarzesFeld in range(anzahlSchwarzeFelderS):
                        self.level[zaehlerS][hinweisSpalte] = 1
                        zaehlerS += 1
                    if zaehlerS < self.anzahlZeilen:
                        self.level[zaehlerS][hinweisSpalte] = 2
                        zaehlerS += 1
                self.hinweiseSpalten[hinweisSpalte][1] = False
                for i in range(self.anzahlZeilen):
                    self.zeileabgeschlossen(i)
                return

        print("nichts neues")


    def reiheUeberpruefenObMoeglicheLoesung(self, reihenNummer, reihe, istSpalte):
        if istSpalte:
            reiheLoesung = copy.copy(self.hinweiseInZahlenZeilenSpalten[1][reihenNummer])
        else:
            reiheLoesung = copy.copy(self.hinweiseInZahlenZeilenSpalten[0][reihenNummer])

        zaehler = 0
        for j in range(self.anzahlSpalten):
            if reihe[j] == 1:
                zaehler += 1
            elif reiheLoesung:
                if reiheLoesung[0] < zaehler:
                    #print("Reihe ist falsch, zu viele schwarze Felder nebeneinander.")
                    return False
                if reiheLoesung[0] > zaehler != 0:
                    #print("Reihe ist falsch, zu wenige schwarze Felder nebeneinander.")
                    return False
                elif reiheLoesung[0] == zaehler:
                    reiheLoesung.pop(0)
                    zaehler = 0

        if reiheLoesung:
            if reiheLoesung[0] == zaehler:
                reiheLoesung.pop(0)
                zaehler = 0

        if zaehler > 0:
            #print("Reihe ist falsch, zu viele schwarze Felder insgesamt")
            return False

        if not reiheLoesung:
            #print("Reihe kann richtig sein")
            return True

        if reiheLoesung == [0]:
            #print("Reihe ist richtig, da keine schwarzen Felder drin sein sollen.")
            return True

        #print("Reihe ist falsch, es ist noch kein schwarzes Feld eingetragen")
        return False


    def binaereKombinationen(self, anzahlStellen):
        result = []
        for integerZahl in range(2 ** anzahlStellen, 2 ** anzahlStellen * 2):
            binaereZahlInString = bin(integerZahl)
            zwischenergebnis = []
            for stelle in range(3, len(binaereZahlInString)):
                zwischenergebnis.append(int(binaereZahlInString[stelle]))
            result.append(zwischenergebnis)

        return result


    def alleMoeglichenLoesungenBerechnenZeile(self, reihenNummer):
        vorhandeneReihe = copy.copy(self.level[reihenNummer])

        anzahlFehlendeSchwarzeFelder = 0
        for zahl in self.hinweiseInZahlenZeilenSpalten[0][reihenNummer]:
            anzahlFehlendeSchwarzeFelder += zahl
        for feld in vorhandeneReihe:
            if feld == 1:
                anzahlFehlendeSchwarzeFelder -= 1

        # Indizies raussuchen, die unbelegt sind
        anzahlNochUnbelegteFelder = 0
        zuBelegendeFelderIndizes = []
        for feldIndex in range(len(vorhandeneReihe)):
            if vorhandeneReihe[feldIndex] == 0:
                anzahlNochUnbelegteFelder += 1
                zuBelegendeFelderIndizes.append(feldIndex)

        alleKombinationen = self.binaereKombinationen(anzahlNochUnbelegteFelder)

        alleMoeglichenLoesungen = []
        for kombiIndex in range(len(alleKombinationen)):
            for stelleIndex in range(len(alleKombinationen[kombiIndex])):
                vorhandeneReihe[zuBelegendeFelderIndizes[stelleIndex]] = alleKombinationen[kombiIndex][stelleIndex]
            if self.reiheUeberpruefenObMoeglicheLoesung(reihenNummer, vorhandeneReihe, False):
                alleMoeglichenLoesungen.append(tuple(vorhandeneReihe))

        print("moegliche Loesungen :  ", alleMoeglichenLoesungen)
        return alleMoeglichenLoesungen



app = QApplication(sys.argv)
ex = Window()
sys.exit(app.exec_())
