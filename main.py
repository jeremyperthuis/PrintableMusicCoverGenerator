'''
    PrintableMusicCoverGenerator v1.3

    Perthuis Jeremy
'''


import os
from math import *
import mutagen
import datetime
from Functions import *
from pyfiglet import Figlet
from pprint import pprint


class Cover :

    version=1.2
    pathMusicDirectory = ""
    coverTitre=""
    titleLimit=52
    listMusicTitle=[]
    listMusicTitleFormat=[]
    templateDetails=[]
    coverExport=[]

    def __init__(self,path):

        self.pathMusicDirectory=path

        self.ScanFolder()
        self.titleProcessing()
        self.verification()
        self.formatListeMusic(self.listMusicTitleFormat)
        #self.buildCover()
        #self.writeTemplate()


    # Stocke les titres dans l'ordre alaphabetique dans listMusicTitle
    def ScanFolder(self):
        print(" ScanFolder()")
        self.listMusicTitle.clear()
        for file in os.listdir(self.pathMusicDirectory):
            try:
                mutagen.File(self.pathMusicDirectory+"\\"+file)
                if ".mp3" in file:
                    self.listMusicTitle.append(file)
                else:
                    print("     WARNING ! {0} n'est pas un fichier mp3".format(file))
            except mutagen.MutagenError:
                print("     WARNING ! {0} n'est pas un fichier compatible".format(file))

    # Stocke les titre avec leur durée dans listMusicTitleFormat
    def titleProcessing(self):
        print(" titleProcessing()")
        self.listMusicTitleFormat.clear()
        for elem in self.listMusicTitle:
            time=str(datetime.timedelta(seconds=mutagen.mp3.MP3(self.pathMusicDirectory +"\\"+str(elem)).info.length))[2:7]
            elem = elem.replace('.mp3','')
            elem = elem + '-' + time
            self.listMusicTitleFormat.append(elem.split('-'))
        print("     ok")

    # Verifie la presence ou non dans le titre des données de ton et tempo
    def verification(self):
        print(" verification()")
        for elem in self.listMusicTitleFormat:
            try:
                a=elem[3]
            except IndexError:
                temp=elem[2]
                elem.pop(2)
                elem.append("___")
                elem.append(temp)

            try:
                b=elem[4]
            except IndexError:
                temp = elem[3]
                elem.pop(3)
                elem.append("___")
                elem.append(temp)
        print("     ok")

    # Retire les espaces blanc pour chaque champs titre, tempo, clé
    def formatListeMusic(self,arg):
        print(" formatListMusic()")
        for elem in arg:
            elem[0]=removeEndSpace(elem[0])+' - '+removeEndSpace(elem[1])
            elem.pop(1)
            elem[1]=removeEndSpace(elem[1])
            elem[2]=removeEndSpace((elem[2]))
        print("     ok")

    # Construit le Header titre du tableau imprimable dans coverExport
    def buildHeader(self):
        print(" buildHeader()")
        lenTitle = 69
        f = Figlet(font='standard')
        bigtext = str(f.renderText(self.coverTitre))
        bigtextFrag=bigtext.split("\n")
        CdTitleCentre = floor(lenTitle / 2) - floor(len(bigtextFrag[0]) / 2)

        # gere le decalage du titre
        if len(bigtextFrag[0]) % 2 == 1:
            ecart = 0
        else:
            ecart = 1
        self.coverExport.append('╔' + (lenTitle) * '═' + '╗')
        for ligne in bigtextFrag:
            if len(ligne)>0:
                self.coverExport.append('║' + (CdTitleCentre) * ' ' + ligne + (CdTitleCentre + ecart) * ' ' + '║')
        self.coverExport.append("╠══╦" + (self.titleLimit) * '═' + '╦═════╦═══╦═══╣')
        print("     ok")

    # Construit le tableau avec les titres
    def buildCover(self):
        print(" buildCover()")
        self.coverExport=[]
        self.buildHeader()
        i = 0
        for elem in self.listMusicTitleFormat:
            i+=1
            if len(elem)==4:
                # Formate le numero (1ere colonne)
                arg0 = lambda x: str(x) if len(str(x)) >= 2 else '0' + str(x)
                # Formate le tempo et la tonalité
                arg34 = lambda x: ' '+ x if len(x)==2 else x

                self.coverExport.append('║{0}║{1}║{2}║{3}║{4}║'.format(
                    arg0(i),
                    elem[0]+(self.titleLimit-len(elem[0]))*' ',
                    elem[3],
                    arg34(elem[1]),
                    arg34(elem[2])))

            else:
                print("{0} est mal formaté".format(elem))

            if i<len(self.listMusicTitleFormat):
                self.coverExport.append('╠══╬' + (self.titleLimit)*'═' + '╬═════╬═══╬═══╣')
            if i>=len(self.listMusicTitleFormat):
                self.coverExport.append('╚══╩' + (self.titleLimit)*'═' + '╩═════╩═══╩═══╝')
        print("     buildCover() ok")

    # Ecrit dans un fichier txt le cover final dans le dossier d'origine
    def writeTemplate(self):
        print(" writeTemplate()")
        file = open(self.pathMusicDirectory+"\\tracklist.txt",'w', encoding="utf8")
        for elem in self.coverExport:
            file.write(elem + '\n')
        file.close()
        print("     ok")


# c=Cover("C:\\Users\jpu\Desktop\CD6")
# print(c.pathMusicDirectory)
# pprint(c.coverExport)