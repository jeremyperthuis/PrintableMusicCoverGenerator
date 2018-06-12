from tkinter import filedialog
from tkinter import *
import time
from main import *
import pprint

class Gui:

    rep=""
    root = Tk()
    root.title("PrintableMusicCoverGenerator v1.1")
    root.minsize(500, 400)
    root.geometry("520x400")
    global C

    def __init__(self):
        print("init")
        self.setup()

    def setup(self):
        print("setup")

        # Panel Choix Dossier & Liste Mp3
        self.Paned1=PanedWindow(self.root, orient=HORIZONTAL)
        self.Paned1.pack(side=TOP, padx=5, pady=5)
        btnChoixDir = Button(self.Paned1, text='Choose directory', command=self.choixdir)
        btnChoixDir.pack()
        self.Paned2=PanedWindow(self.root, orient=HORIZONTAL)
        self.Paned2.pack()

        # Boutons Exit & Generate
        btnExit = Button(self.root, text='Exit', command=self.root.destroy)
        btnExit.pack(side="left",anchor="s",padx=5, pady=5)

        btnGenerate = Button(self.root, text='Generate', command=self.generate)
        btnGenerate.pack(side="right",anchor="s",padx=5,pady=5)
        self.root.mainloop()

    ################################################
    # Fonction 'Choose directory'
    ################################################
    def choixdir(self):

        # La fenetre de selection de dossier apparait
        self.rep = filedialog.askdirectory(initialdir="/", title='Choisir un repertoire')+"/"
        if len(self.rep) > 0:
            value=StringVar()
            value.set(self.rep)
            tex2 = Entry(self.Paned1, textvariable=value, width=30)
            tex2.pack()
            C = Cover(self.rep)
            self.getListe(C.listMusicTitleFormat)
            C.buildCover()
            C.writeTemplate()

    ################################################
    # Affichage des Entry
    ################################################
    def getListe(self,argLst):
        print("getListe")
        # On cree une liste de dictionnaire pour stocker les sons
        listDict=[]
        songDict={}
        for song in argLst:
            songDict["titre"]=song[0]+"-"+song[1]
            songDict["bpm"]=song[2]
            songDict['key']=song[3]
            songDict['duree']=song[4]
            listDict.append(dict(songDict))

        i=0
        for elem in listDict:
            print(elem)
            titre= StringVar(self.Paned2,value=elem['titre'])
            bpm = StringVar(self.Paned2, value=elem['bpm'])
            key = StringVar(self.Paned2, value=elem['key'])
            duree = StringVar(self.Paned2, value=elem['duree'])

            entryTitre = Entry(self.Paned2,textvariable=titre, width=50).grid(column=0)
            entryBpm = Entry(self.Paned2,textvariable=bpm,width=10).grid(row=i,column=1)
            entryKey = Entry(self.Paned2,textvariable=key, width=10).grid(row=i, column=2)
            entryDuree = Entry(self.Paned2,textvariable=duree, width=10).grid(row=i, column=3)
            i+=1


    # Genere la cover
    def generate(self):
        print("generate")
        tex3=Label(self.root,text="Sucess !")
        tex3.pack(side="bottom")


g=Gui()