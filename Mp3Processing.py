'''
    PrintableMusicCoverGenerator v1.5

    Perthuis Jeremy
'''

import os

import mutagen
import datetime
from Functions import *

import logging

class Mp3Processing:
    version = 1.5
    music_folder_path = ""

    list_mp3 = dict()

    logging.basicConfig(format='%(asctime)s  %(levelname)s : %(funcName)s  %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def __init__(self, path):

        self.music_folder_path = os.path.abspath(path) if os.path.isdir(path) else "null"
        writeLastPath(path)
        self.scanFolder()
        self.addlength()
        self.addTitleArtist()

    # Stocke les titres dans l'ordre alphabetique dans listMusicTitle
    def scanFolder(self):
        logging.info("start")
        for file in os.listdir(self.music_folder_path):
            try:
                mutagen.File(os.path.join(self.music_folder_path, file))
                if isMP3(file):
                    self.list_mp3[file] = dict()
                else:
                    logging.warning("  {0} n'est pas un fichier .mp3".format(file))
            except mutagen.MutagenError:
                logging.warning(" {0} n'est pas un fichier compatible".format(file))
        logging.info("end : {0} fichiers .mp3 traité(s)".format(len(self.list_mp3)))

    # ajoute le noeud terminal du path (Nom pas défaut du CD)
    def getDefautCDName(self):
        logging.info("start")
        return os.path.basename(self.music_folder_path)


    # Stocke les durée dans list_mp3
    def addlength(self):
        logging.info("start")
        for elem in self.list_mp3:
            self.list_mp3[elem]["length"] = str(
                datetime.timedelta(seconds=mutagen.mp3.MP3(os.path.join(self.music_folder_path, str(elem))).info.length))[
                   2:7]
        logging.info("end")

    # Stocke les titres, artistes, clés et tempo dans list_mp3
    def addTitleArtist(self):
        logging.info("start")

        for key,value in self.list_mp3.items():
            value["raw_title"]=key.replace(".mp3","")
            datas_dict = splitRawTitle(value["raw_title"])
            value["artist"]=datas_dict["artist"]
            value["title"] = datas_dict["title"]
            value["key"] = datas_dict["key"]
            value["tempo"] = datas_dict["tempo"]
            value["display_title"] = datas_dict["display_title"]

if __name__ == '__main__':
    M=Mp3Processing("F:\\Users\\Jeremy\\Developpement\\PrintableMusicCoverGenerator\\testCD")