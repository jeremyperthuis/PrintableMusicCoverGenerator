'''
    PrintableMusicCoverGenerator v1.1

    Perthuis Jeremy
'''


import os
from math import *
from mutagen.mp3 import MP3
import datetime
from Functions import *


class Cover :

    coverTitre="CD1"
    titleLimit=50
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
        #self.buildCover()
        #self.writeTemplate()


    # Stocke les titres dans l'ordre alaphabetique dans une liste
    def ScanFolder(self):
        liste = os.listdir(self.musicPath)
        for elem in liste:
            self.listMusicTitle.append(elem)
            print(elem)

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
        for elem in self.listMusicTitleFormat:
            try:
                print(elem[3])
            except IndexError:
                temp=elem[2]
                elem.pop(2)
                elem.append("xx")
                elem.append(temp)

            try:
                print(elem[4])
            except IndexError:
                temp = elem[3]
                elem.pop(3)
                elem.append("xx")
                elem.append(temp)

        for elem in self.listMusicTitleFormat:
            print(elem)

    # Construit le tableau avec les titres
    def buildCover(self):
        i=0
        lenTitle=24+self.titleLimit
        CdTitleCentre= floor(lenTitle/2)-floor(len(self.coverTitre)/2)
        # gere le decalage du titre
        if len(self.coverTitre)%2==0:
            ecart=0
        else:
            ecart=-1

        self.coverExport.append('╔' + (lenTitle)*'═' + '╗')
        self.coverExport.append('║' + (CdTitleCentre)*' ' + self.coverTitre +(CdTitleCentre+ecart)*' ' + '║')
        self.coverExport.append("╠═══╦"+(self.titleLimit)*'═'+'╦═══════╦═════╦═════╣')

        for elem in self.listMusicTitleFormat:
            i+=1
            if len(elem)==5:
                arg1 = lambda x: str(x) if len(str(x)) >= 2 else '0' + str(x)
                arg34 = lambda x: ' '+removeEndSpace(x) if len(removeEndSpace(x))==2 else removeEndSpace(x)

                self.coverExport.append('║{0} ║ {1} ║ {2} ║ {3} ║ {4} ║'.format(
                    arg1(i),
                    elem[0]+'-'+elem[1]+(self.titleLimit-len(elem[0]+'-'+elem[1])-2)*' ',
                    elem[4],
                    arg34(elem[2]),
                    arg34(elem[3])))

            else:
                print("{0} est mal formaté".format(elem))

            if i<len(self.listMusicTitleFormat):
                self.coverExport.append('╠═══╬' + (self.titleLimit)*'═' + '╬═══════╬═════╬═════╣')
            if i>=len(self.listMusicTitleFormat):
                self.coverExport.append('╚═══╩' + (self.titleLimit)*'═' + '╩═══════╩═════╩═════╝')




        print(self.coverExport)

    # Ecrit dans un fichier txt le cover final
    def writeTemplate(self):
        file = open("results/test.txt",'w', encoding="utf8")
        for elem in self.coverExport:
            file.write(elem + '\n')

        file.close()


#c=Cover("mp3/")
#print(c.listMusicTitleFormat)