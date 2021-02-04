from utils import *


def analyzeHyphenTest():
    regexKey = "^[\s]*[\d]{1,2}[A-B,a-b]{1}[\s]*$"
    regexTempo = "^[\s]*[\d]{1,3}[\s]*$"
    regexLength = "^[\s]*[\d]{1,3}[:][\d]{1,2}[\s]*$"

    str1 = "Gatekeeper - Forgotten - 8A - 120"
    str2 = "Jean-Luc - Le Sabbat - 10A - 84"
    print(splitRawTitle(str1))
    print(str2.split("-")[-2])
    print(splitRawTitle(str2))


def lastPathTest():
    #WriteLastPath("F:\\Users\\Jeremy\\OneDrive\\In Da Hood\\PLAYLISTS")
    print(getLastPath())


