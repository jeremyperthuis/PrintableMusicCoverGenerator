'''
    PrintableMusicCoverGenerator v1.5

    Perthuis Jeremy
'''

import os
from math import *
import mutagen
import datetime
from Functions import *
from pyfiglet import Figlet
import logging

class Mp3Processing:
    version = 1.5
    music_folder_path = ""
    cover_titre = ""
    title_limit = 52
    list_font = ["straight", "stop", "starwars", "standard", "small", "roman", "puffy", "doom", "big"]
    default_font = "standard"
    list_music_title = []
    list_music_title_format = []
    list_mp3 = dict()
    template_details = []
    cover_export = []
    logging.basicConfig(format='%(asctime)s  %(levelname)s : %(funcName)s  %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def __init__(self, path):

        self.music_folder_path = path
        writeLastPath(path)
        self.scanFolder()
        self.addlength()
        self.addTitleArtist()
        # self.verification()
        # self.formatListeMusic(self.list_music_title_format)

    # Stocke les titres dans l'ordre alphabetique dans listMusicTitle
    def scanFolder(self):
        logging.info("start")
        self.list_music_title.clear()
        for file in os.listdir(self.music_folder_path):
            try:
                mutagen.File(self.music_folder_path + "\\" + file)
                if isMP3(file):
                    self.list_mp3[file] = dict()
                else:
                    logging.warning("  {0} n'est pas un fichier .mp3".format(file))
            except mutagen.MutagenError:
                logging.warning(" {0} n'est pas un fichier compatible".format(file))
        logging.info("end : {0} fichiers .mp3 traité(s)".format(len(self.list_mp3)))

    # Stocke les durée dans list_mp3
    def addlength(self):
        logging.info("start")
        for elem in self.list_mp3:
            self.list_mp3[elem]["length"] = str(
                datetime.timedelta(seconds=mutagen.mp3.MP3(self.music_folder_path + "\\" + str(elem)).info.length))[
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

    # Construit le Header titre du tableau imprimable dans coverExport
    def buildHeader(self):
        logging.info("start")
        lenTitle = 69
        f = Figlet(font=self.default_font)
        bigtext = str(f.renderText(self.cover_titre))
        bigtextFrag = bigtext.split("\n")
        CdTitleCentre = floor(lenTitle / 2) - floor(len(bigtextFrag[0]) / 2)

        # gere le decalage du titre
        if len(bigtextFrag[0]) % 2 == 1:
            ecart = 0
        else:
            ecart = 1
        self.cover_export.append('╔' + (lenTitle) * '═' + '╗')
        for ligne in bigtextFrag:
            if len(ligne) > 0:
                self.cover_export.append('║' + (CdTitleCentre) * ' ' + ligne + (CdTitleCentre + ecart) * ' ' + '║')
        self.cover_export.append("╠══╦" + (self.title_limit) * '═' + '╦═════╦═══╦═══╣')

    # Construit le tableau avec les titres
    def buildCover(self):
        logging.info("start")
        self.cover_export = []
        self.buildHeader()
        i = 0
        for elem in self.list_music_title_format:
            i += 1
            if len(elem) == 4:
                # Formate le numero (1ere colonne)
                arg0 = lambda x: str(x) if len(str(x)) >= 2 else '0' + str(x)
                # Formate le tempo et la tonalité
                arg34 = lambda x: ' ' + x if len(x) == 2 else x

                self.cover_export.append('║{0}║{1}║{2}║{3}║{4}║'.format(
                    arg0(i),
                    elem[0] + (self.title_limit - len(elem[0])) * ' ',
                    elem[3],
                    arg34(elem[1]),
                    arg34(elem[2])))

            else:
                print("{0} est mal formaté".format(elem))

            if i < len(self.list_music_title_format):
                self.cover_export.append('╠══╬' + (self.title_limit) * '═' + '╬═════╬═══╬═══╣')
            if i >= len(self.list_music_title_format):
                self.cover_export.append('╚══╩' + (self.title_limit) * '═' + '╩═════╩═══╩═══╝')
        print("     buildCover() ok")

    # Ecrit dans un fichier txt le cover final dans le dossier d'origine
    def writeTemplate(self):
        logging.info("start")
        file = open(self.music_folder_path + "\\tracklist.txt", 'w', encoding="utf8")
        for elem in self.cover_export:
            file.write(elem + '\n')
        file.close()
        print("     ok")

if __name__ == '__main__':
    M=Mp3Processing("F:\\Users\\Jeremy\\Developpement\\PrintableMusicCoverGenerator\\testCD")