
from tkinter import filedialog
from tkinter import *
from mutagen.mp3 import HeaderNotFoundError
from main import *

class Gui:

    rep=""
    root = Tk()
    root.title("PrintableMusicCoverGenerator v1.4")
    root.minsize(500, 400)
    root.geometry("520x400")
    ListeSongs=[]


    def __init__(self):
        print("init()")
        self.setup()

    def setup(self):
        print("setup()")

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
        print("choixdir()")
        try:
            self.DeleteListBoxFont()
            self.DeleteLabelPathCD()
            self.DeleteEntryCDTitle()
            self.saveButton.destroy()
            self.DeleteLabelSongs()
            self.DeleteEntrySongs()
            self.labelwarning.destroy()
        except AttributeError:
            pass


        # La fenetre de selection de dossier apparait
        self.rep = filedialog.askdirectory(initialdir="/", title='Choisir un repertoire')+"/"

        if len(self.rep) > 0:
            try:
                self.path=StringVar()
                self.path.set(self.rep)
                self.DisplayLabelPathCD()

                self.CDtitre=StringVar()
                self.CDtitre.set(self.rep.split('/')[-2])

                self.C = Cover(self.rep)
                self.DisplayListBoxFont()

                self.getListe()
                # try :
                #     print(len(self.C.listMusicTitleFormat))
                # except:
                #     pass
            except HeaderNotFoundError:
                print("pas de son !")



    # Affichage du label du path CD
    def DisplayLabelPathCD(self):
        print(" -> DisplayLabelPathCD()")
        self.labelPathCD = Label(self.Paned1, textvariable=self.path, width=60)
        self.labelPathCD.pack()

    def DeleteLabelPathCD(self):
        try:
            self.labelPathCD.destroy()
        except AttributeError:
            pass

    # Affichage de l'entry du titre du CD
    def DisplayEntryCdTitle(self):
        print(" -> DisplayEntryCDTitle()")
        self.entryTitreCD = Entry(self.Paned1, textvariable=self.CDtitre, width=20,justify=CENTER)
        self.entryTitreCD.pack()
        self.ListeSongs=[]

    def DeleteEntryCDTitle(self):
        try:
            self.entryTitreCD.destroy()
        except AttributeError:
            pass

    # Affichage des Labels "title", "length", "key", "bpm"
    def DisplayLabelSongs(self):
        print(" -> DisplayLabelSongs()")

        # Déclaration des Labels
        i = 0
        self.labeltitre=Label(self.Paned2,text="Title")
        self.labeltitre.grid(row=i,column=0)
        self.labelduree = Label(self.Paned2, text="Length")
        self.labelduree.grid(row=i,column=3)
        self.labelbpm = Label(self.Paned2, text="BPM")
        self.labelbpm.grid(row=i,column=1)
        self.labelkey=Label(self.Paned2,text="Key")
        self.labelkey.grid(row=i,column=2)

    def DeleteLabelSongs(self):
        try:
            self.labeltitre.destroy()
            self.labelbpm.destroy()
            self.labelduree.destroy()
            self.labelkey.destroy()
        except AttributeError:
            pass

    # Affichage des Entry de sons (arg : listMusicTitleFormat)
    def DisplayEntrySongs(self,argLst):
        print(" -> DisplayEntrySongs()")
        # On cree une liste de dictionnaire pour stocker les sonsf
        listDict = []
        songDict = {}

        self.ListeSongs.clear()
        # print("ListeSongs {0}: {1}".format(len(self.ListeSongs),self.ListeSongs))
        # print("ArgLst {0}: {1}".format(len(argLst),argLst))

        # Affectation dans le dictionnaire
        for song in argLst:
            songDict["titre"] = song[0]
            songDict["bpm"] = song[1]
            songDict['key'] = song[2]
            songDict['duree'] = song[3]
            listDict.append(dict(songDict))

        i = 1

        # Déclaration des Entry

        for elem in listDict:
            ListeSong = []
            titre = StringVar(self.Paned2, value=elem['titre'])
            bpm = StringVar(self.Paned2, value=elem['bpm'])
            key = StringVar(self.Paned2, value=elem['key'])
            duree = StringVar(self.Paned2, value=elem['duree'])

            entryTitre = Entry(self.Paned2, textvariable=titre, width=60)
            if len(elem["titre"]) > self.C.titleLimit:
                self.labelwarning = Label(self.Paned2, text="Title too long !")
                entryTitre.configure(background="red")
            entryTitre.grid(column=0)
            ListeSong.append(entryTitre)

            entryBpm = Entry(self.Paned2, textvariable=bpm, width=8)
            entryBpm.grid(row=i, column=1)
            ListeSong.append(entryBpm)

            entryKey = Entry(self.Paned2, textvariable=key, width=8)
            entryKey.grid(row=i, column=2)
            ListeSong.append(entryKey)

            entryDuree = Entry(self.Paned2, textvariable=duree, width=8, state='disabled')
            entryDuree.grid(row=i, column=3)
            ListeSong.append(entryDuree)

            self.ListeSongs.append(list(ListeSong))
            i += 1

        # print("ListeSongs {0}: {1}".format(len(self.ListeSongs), self.ListeSongs))
        # print("ArgLst {0}: {1}".format(len(argLst), argLst))


        # Déclaration du bouton 'Save'
        self.saveButton = Button(self.Paned2, text='Save', command=self.Save, padx=5, pady=5)
        self.saveButton.grid(row=i, column=3)

        # On fait aparaitre le warning si le titre est trop long
        if len(elem["titre"]) > self.C.titleLimit:
            self.labelwarning.grid(row=i, column=0)

    # Suppression des Entry de sons
    def DeleteEntrySongs(self):
        print("DeleteEntrySongs()")
        for sons in self.ListeSongs:
            for a in sons:
                print(a.get())
                print(a.destroy())

        # print(len(self.ListeSongs))

    # Affichage de la listBox de selection de fonte
    def DisplayListBoxFont(self):
        print(" -> DisplayListBoxFont()")

        self.varFont = StringVar(self.Paned2)
        self.varFont.set("standard")

        self.spinBoxFont=OptionMenu(self.Paned1,self.varFont,*self.C.listFont)
        self.spinBoxFont.pack()

    # Suppression de la listBox de selection de fonte
    def DeleteListBoxFont(self):
        try:
            self.spinBoxFont.destroy()
        except AttributeError:
            pass

    def getListe(self):
        print("getListe()")
        self.DisplayEntryCdTitle()
        self.DisplayLabelSongs()
        self.DisplayEntrySongs(self.C.listMusicTitleFormat)

    # Enregistre les valeurs des Entry
    def Save(self):
        print("Save()")
        # On recupere la fonte choisie (defaut : standard)
        self.C.usedFont = self.varFont.get()

        # On récupere le Titre du CD
        self.C.coverTitre=self.CDtitre.get()

        # On recupere les titres des tracks fraichement edités
        songs=[]
        for elem in self.ListeSongs:
            song=[]
            for i in elem:
                song.append(i.get())
            songs.append(list(song))

        self.DeleteEntrySongs()

        # Suppression du bouton save
        self.saveButton.destroy()
        # Supression du label "titre trop long"
        try:
            self.labelwarning.destroy()
        except AttributeError:
            pass
        # Suppression de l'entry titre du CD
        self.DeleteEntryCDTitle()
        self.C.listMusicTitleFormat = songs
        self.getListe()
        self.C.buildCover()

    # Genere la cover
    def generate(self):
        try:
            self.labelSucess.destroy()
        except AttributeError:
            pass
        print("Generate()")
        self.C.writeTemplate()
        self.labelSucess=Label(self.root,text="Sucess !")
        self.labelSucess.pack(side="bottom")


g=Gui()