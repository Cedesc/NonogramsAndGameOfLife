import picrossLevelBib

""" Spiel-Settings """
FENSTERBREITE = 1300
FENSTERHOEHE = 1000
ANZAHLREIHEN = 5
ANZAHLSPALTEN = 5
SCHWIERIGKEIT = -1000


ZUFAELLIGESLEVEL = picrossLevelBib.zufaelligesLevelMitSchwierigkeit(ANZAHLSPALTEN, ANZAHLREIHEN, SCHWIERIGKEIT)
VORGEFERTIGTESLEVEL = picrossLevelBib.nummer04

LEVEL = ZUFAELLIGESLEVEL
