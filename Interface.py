
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from mutagen.mp3 import HeaderNotFoundError
from BuildCover import *
import logging

class Interface:

    rep=""
    root = Tk()
    root.title("PrintableMusicCoverGenerator v1.5")
    root.minsize(600, 500)
    root.geometry("600x500")
    ListeSongs=[]
    logging.basicConfig(format='%(asctime)s  %(levelname)s : %(funcName)s  %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    def __init__(self):
        logging.info("start")
        self.setup()

    def setup(self):
        logging.info("start")

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

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    # Bouton choisir un dossier
    def choixdir(self):
        logging.info("start")
        try:
            self.deleteListBoxFont()
            self.deleteLabelPathCD()
            self.deleteDisplayCDName()
            self.saveButton.destroy()
            self.deleteDisplayMp3Labels()
            self.deleteEntrySongs()
            self.labelwarning.destroy()
        except AttributeError:
            pass


        # La fenetre de selection de dossier apparait
        self.rep = filedialog.askdirectory(initialdir=getLastPath(), title='Choisir un repertoire') + "/"

        if len(self.rep) > 0:
            try:
                # Affichage du label du path complet
                self.path=StringVar()
                self.path.set(self.rep)
                self.displayLabelPathCD()

                # declaration des objets
                self.C = Mp3Processing(self.rep)
                self.B = BuildCover(self.C)

                # Affichage du nom du CD
                self.CDtitre = StringVar()
                self.CDtitre.set(self.C.getDefautCDName())
                self.displayCDName()

                # Afiichage de la liste des fontes disponibles
                self.displayListBoxFont()

                self.displayMp3Labels()

            except HeaderNotFoundError:
                print("Aucun fichier .mp3 trouvé !")



    # Affichage du label du path CD
    def displayLabelPathCD(self):
        logging.info("start")
        self.labelPathCD = Label(self.Paned1, textvariable=self.path, width=60)
        self.labelPathCD.pack()

    def deleteLabelPathCD(self):
        try:
            self.labelPathCD.destroy()
        except AttributeError:
            pass

    # Affichage du nom du CD
    def displayCDName(self):
        logging.info("start")
        self.entryTitreCD = Entry(self.Paned1, textvariable=self.CDtitre, width=20,justify=CENTER)
        self.entryTitreCD.pack()
        self.ListeSongs=[]

    def deleteDisplayCDName(self):
        logging.info("start")
        try:
            self.entryTitreCD.destroy()
        except AttributeError:
            pass

    # Affichage des Labels "title", "length", "key", "bpm"
    def displayMp3Labels(self):
        logging.info("start")

        # Déclaration des Labels
        i = 0
        self.labeltitre=Label(self.Paned2,text="Title")
        self.labeltitre.grid(row=i,column=0)
        self.labelduree = Label(self.Paned2, text="Length")
        self.labelduree.grid(row=i,column=3)
        self.labelbpm = Label(self.Paned2, text="Key")
        self.labelbpm.grid(row=i,column=1)
        self.labelkey=Label(self.Paned2,text="Tempo")
        self.labelkey.grid(row=i,column=2)

    def deleteDisplayMp3Labels(self):
        logging.info("start")
        try:
            self.labeltitre.destroy()
            self.labelbpm.destroy()
            self.labelduree.destroy()
            self.labelkey.destroy()
        except AttributeError:
            pass

    # Affichage des Entry de sons (arg : listMusicTitleFormat)
    def displayEntrySongs(self, mp3_dict):
        logging.info("start")
        print(mp3_dict)
        i=0
        for key, value in mp3_dict.items():
            ListeSong = []
            titre = StringVar(self.Paned2, value=value['display_title'])
            bpm = StringVar(self.Paned2, value=value['tempo'])
            key = StringVar(self.Paned2, value=value['key'])
            duree = StringVar(self.Paned2, value=value['length'])

            entryTitre = Entry(self.Paned2, textvariable=titre, width=60)

            if len(value["display_title"]) > self.B.title_limit:
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
        self.saveButton = Button(self.Paned2, text='Save', command=self.save, padx=5, pady=5)
        self.saveButton.grid(row=i, column=3)

        # # On fait aparaitre le warning si le titre est trop long
        # if len(elem["titre"]) > self.B.title_limit:
        #     self.labelwarning.grid(row=i, column=0)

    # Suppression des Entry de sons
    def deleteEntrySongs(self):
        logging.info("start")
        for sons in self.ListeSongs:
            for a in sons:
                print(a.get())
                print(a.destroy())

        # print(len(self.ListeSongs))

    # Affichage de la listBox de selection de fonte
    def displayListBoxFont(self):
        logging.info("start")

        self.varFont = StringVar(self.Paned2)
        self.varFont.set("standard")

        self.spinBoxFont=OptionMenu(self.Paned1, self.varFont, self.B.list_font)
        self.spinBoxFont.pack()

    # Suppression de la listBox de selection de fonte
    def deleteListBoxFont(self):
        logging.info("start")
        try:
            self.spinBoxFont.destroy()
        except AttributeError:
            pass

    def displayGridView(self):
        logging.info("start")

        self.displayEntrySongs(self.C.list_mp3)

    # Enregistre les valeurs des Entry
    def save(self):
        logging.info("start")
        # On recupere la fonte choisie (defaut : standard)
        self.C.default_font = self.varFont.get()

        # On récupere le Titre du CD
        self.C.cover_titre=self.CDtitre.get()

        # On recupere les titres des tracks fraichement edités
        songs=[]
        for elem in self.ListeSongs:
            song=[]
            for i in elem:
                song.append(i.get())
            songs.append(list(song))

        self.deleteEntrySongs()

        # Suppression du bouton save
        self.saveButton.destroy()
        # Supression du label "titre trop long"
        try:
            self.labelwarning.destroy()
        except AttributeError:
            pass
        # Suppression de l'entry titre du CD
        self.deleteDisplayCDName()
        self.C.list_music_title_format = songs
        self.displayGridView()
        self.C.buildCover()

    # Genere la cover
    def generate(self):
        logging.info("start")
        try:
            self.labelSucess.destroy()
        except AttributeError:
            pass
        print("Generate()")
        self.C.writeTemplate()
        self.labelSucess=Label(self.root,text="Sucess !")
        self.labelSucess.pack(side="bottom")

    def on_closing(self):
        logging.info("start")
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()



g=Interface()