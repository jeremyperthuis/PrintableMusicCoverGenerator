'''
    PrintableMusicCoverGenerator v1.2

    Perthuis Jeremy
'''


import os
from math import *
from mutagen.mp3 import MP3
import datetime
from Functions import *
from pyfiglet import Figlet


class Cover :
    version=1.1
    coverTitre=""
    titleLimit=52
    musicPath=""
    listMusicTitle=[]
    listMusicTitleFormat=[]
    templateDetails=[]
    coverExport=[]

    def __init__(self,path):
        self.musicPath=path

        self.ScanFolder()
        self.titleProcessing()
        self.verification()
        self.formatListeMusic(self.listMusicTitleFormat)
        #self.buildCover()
        #self.writeTemplate()


    # Stocke les titres dans l'ordre alaphabetique dans une liste
    def ScanFolder(self):
        liste = os.listdir(self.musicPath)
        for elem in liste:
            self.listMusicTitle.append(elem)

    # Stocke les titre dans une liste avec leur duree
    def titleProcessing(self):

        for elem in self.listMusicTitle:
            audio = MP3(self.musicPath+str(elem))
            time=str(datetime.timedelta(seconds=audio.info.length))[2:7]

            elem = elem.replace('.mp3','')
            elem = elem + '-' + time
            self.listMusicTitleFormat.append(elem.split('-'))

    # Verifie la presence ou non dans le titre des données de ton et tempo
    def verification(self):
        print("TEST")
        for elem in self.listMusicTitleFormat:
            try:
                print(elem[3])
            except IndexError:
                temp=elem[2]
                elem.pop(2)
                elem.append("xxx")
                elem.append(temp)

            try:
                print(elem[4])
            except IndexError:
                temp = elem[3]
                elem.pop(3)
                elem.append("xxx")
                elem.append(temp)

    def formatListeMusic(self,arg):
        for elem in arg:
            elem[0]=removeEndSpace(elem[0])+' - '+removeEndSpace(elem[1])
            elem.pop(1)
            elem[1]=removeEndSpace(elem[1])
            elem[2]=removeEndSpace((elem[2]))
            print(elem)

    def buildHeader(self):
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


    # Construit le tableau avec les titres
    def buildCover(self):
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




        print(self.coverExport)

    # Ecrit dans un fichier txt le cover final
    def writeTemplate(self):
        file = open("results/test.txt",'w', encoding="utf8")
        for elem in self.coverExport:
            file.write(elem + '\n')
        file.close()


#c=Cover("mp3/")
#print(c.listMusicTitleFormat)