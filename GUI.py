from tkinter import filedialog
from tkinter import *
import time
from main import *
import pprint
class Gui:


    rep=""
    root = Tk()
    root.title("PrintableMusicCoverGenerator v1.2")
    root.minsize(500, 400)
    root.geometry("520x400")


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
            global C
            C = Cover(self.rep)
            self.getListe(C.listMusicTitleFormat)
            #C.buildCover()
            #C.writeTemplate()




    ################################################
    # Affichage des Entry
    ################################################
    def getListe(self,argLst):
        print("getListe")
        # On cree une liste de dictionnaire pour stocker les sons
        listDict=[]
        songDict={}

        self.ListeSongs=[]
        for song in argLst:
            songDict["titre"]=song[0]
            songDict["bpm"]=song[1]
            songDict['key']=song[2]
            songDict['duree']=song[3]
            listDict.append(dict(songDict))

        i=0
        for elem in listDict:
            ListeSong = []
            limit=True
            titre= StringVar(self.Paned2,value=elem['titre'])
            bpm = StringVar(self.Paned2, value=elem['bpm'])
            key = StringVar(self.Paned2, value=elem['key'])
            duree = StringVar(self.Paned2, value=elem['duree'])



            entryTitre = Entry(self.Paned2,textvariable=titre, width=60)
            if len(elem["titre"])>C.titleLimit:
                entryTitre.configure(background="red")
            entryTitre.grid(column=0)
            ListeSong.append(entryTitre)

            entryBpm = Entry(self.Paned2,textvariable=bpm,width=8)
            entryBpm.grid(row=i,column=1)
            ListeSong.append(entryBpm)

            entryKey = Entry(self.Paned2,textvariable=key, width=8)
            entryKey.grid(row=i, column=2)
            ListeSong.append(entryKey)

            entryDuree = Entry(self.Paned2,textvariable=duree, width=8)
            entryDuree.grid(row=i, column=3)
            ListeSong.append(entryDuree)

            self.ListeSongs.append(list(ListeSong))
            i+=1

        self.saveButton=Button(self.Paned2,text='Save',command=self.getEditSong)
        self.saveButton.grid()


    def getEditSong(self):
        songs=[]
        for elem in self.ListeSongs:
            song=[]
            for i in elem:
                song.append(i.get())
                i.destroy()
            songs.append(list(song))
        self.saveButton.destroy()
        C.listMusicTitleFormat=songs
        print(C.listMusicTitleFormat)
        self.getListe(C.listMusicTitleFormat)
        C.buildCover()


    # Genere la cover
    def generate(self):
        C.writeTemplate()
        print("generate")
        tex3=Label(self.root,text="Sucess !")
        tex3.pack(side="bottom")


g=Gui()