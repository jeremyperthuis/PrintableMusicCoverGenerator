import os
from mutagen import File, mp3, MutagenError
import datetime
import logging
from utils import writeLastPath, isMP3, splitRawTitle

class Mp3Processing:
    version = 1.5

    def __init__(self, path):
        self.list_mp3 = dict()
        self.music_folder_path = os.path.abspath(path) if os.path.isdir(path) else "null"
        writeLastPath(path)
        self.scanFolder()
        self.addlength()
        self.addTitleArtist()


    def scanFolder(self):
        """
        store music titles in alphabetical order
        """
        for file in sorted(os.listdir(self.music_folder_path)):
            try:
                File(os.path.join(self.music_folder_path, file))
                if isMP3(file):
                    self.list_mp3[file] = dict()
                else:
                    logging.warning("  Is not mp3 file : {}".format(file))
            except MutagenError:
                logging.warning(" Mutagen Error unknown file  : {}".format(file))

        logging.info("OK : {} .mp3 file(s) processed".format(len(self.list_mp3)))

    # ajoute le noeud terminal du path (Nom pas défaut du CD)
    def getDefautCDName(self):
        logging.info("start")
        return os.path.basename(self.music_folder_path)


    # Stocke les durée dans list_mp3
    def addlength(self):
        logging.info("start")
        for elem in self.list_mp3:
            self.list_mp3[elem]["length"] = str(
                datetime.timedelta(seconds=mp3.MP3(os.path.join(self.music_folder_path, str(elem))).info.length))[2:7]
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
