import logging
from pyfiglet import Figlet
from math import *
from Mp3Processing import *

class BuildCover:

    list_font = ["straight", "stop", "starwars", "standard", "small", "roman", "puffy", "doom", "big"]
    default_font = "standard"
    title_limit = 52
    template_details = []
    cover_export = []
    logging.basicConfig(format='%(asctime)s  %(levelname)s : %(funcName)s  %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    defaut_CD_title = ""

    def __init__(self, mp3Processing):
        self.defaut_CD_title = mp3Processing.getDefautCDName()
        self.complete_path = mp3Processing.music_folder_path
        self.mp3_dict = mp3Processing.list_mp3

    # Construit le Header titre du tableau imprimable dans coverExport
    def buildHeader(self):
        logging.info("start")
        lenTitle = 69
        f = Figlet(font=self.default_font)
        bigtext = str(f.renderText(self.defaut_CD_title))
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

    def displayCover(self):
        for line in self.cover_export:
            print(line)
    # Construit le tableau avec les titres
    def buildListSongs(self):
        logging.info("start")
        self.cover_export = []
        self.buildHeader()
        i = 0
        for key, value in self.mp3_dict.items():
            i += 1

            # Formate le numero (1ere colonne)
            arg0 = lambda x: str(x) if len(str(x)) >= 2 else '0' + str(x)
            # Formate le tempo et la tonalité
            arg34 = lambda x: ' ' + x if len(x) == 2 else x

            self.cover_export.append('║{0}║{1}║{2}║{3}║{4}║'.format(
                arg0(i),
                value["display_title"] + (self.title_limit - len(value["display_title"])) * ' ',
                value["length"],
                arg34(value["key"]),
                arg34(value["tempo"])))

            if i < len(self.mp3_dict):
                self.cover_export.append('╠══╬' + (self.title_limit) * '═' + '╬═════╬═══╬═══╣')

            if i >= len(self.mp3_dict):
                self.cover_export.append('╚══╩' + (self.title_limit) * '═' + '╩═════╩═══╩═══╝')


    # Ecrit dans un fichier txt le cover final dans le dossier d'origine
    def writeTemplate(self):
        logging.info("start")
        file = open(os.path.join(self.complete_path,"tracklist.txt"), 'w', encoding="utf8")
        for elem in self.cover_export:
            file.write(elem + '\n')
        file.close()
        print("     ok")


if __name__ == '__main__':
    M = Mp3Processing("F:\\Users\\Jeremy\\Developpement\\PrintableMusicCoverGenerator\\testCD")
    B = BuildCover(M)
    B.buildHeader()
    B.buildListSongs()
    B.displayCover()
    B.writeTemplate()