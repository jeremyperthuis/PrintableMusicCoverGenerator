
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from mutagen.mp3 import HeaderNotFoundError
from BuildCover import *
import logging
import copy

class Interface:

    rep=""
    root = Tk()
    root.title("PrintableMusicCoverGenerator v1.5")
    root.minsize(600, 500)
    root.geometry("600x500")
    edited_list_songs=[]
    logging.basicConfig(format='%(asctime)s  %(levelname)s : %(funcName)s  %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    def __init__(self):
        logging.info("start")
        self.setup()

    def setup(self):
        logging.info("start")

        self.displayMenuBar()

        # Panel Choix Dossier & Liste Mp3
        self.main_pane = PanedWindow(self.root, orient=HORIZONTAL, borderwidth=4, bd=15)
        self.main_pane.pack(side=TOP, padx=5, pady=5)

        self.Paned2=PanedWindow(self.root, orient=HORIZONTAL)
        self.Paned2.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def displayMenuBar(self):

        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        self.menu_fichier = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Fichier", menu=self.menu_fichier)
        self.menu_fichier.add_command(label="Ouvrir dossier", command=self.openDirectory)
        self.menu_fichier.add_command(label="Générer tracklist", command=self.generate, state="disabled")
        self.menu_fichier.add_separator()
        self.menu_fichier.add_command(label="Quitter", command=self.root.destroy)

    # Bouton choisir un dossier
    def openDirectory(self):
        logging.info("start")
        try:
            self.deleteFontScrollableList()
            self.deletePathFolder()
            self.deleteNameFolder()
            self.saveButton.destroy()
            self.deleteSongsLabels()
            self.deleteSongsList()
            self.labelwarning.destroy()
        except AttributeError:
            pass

        # La fenetre de selection de dossier apparait
        self.rep = filedialog.askdirectory(initialdir=getLastPath(), title='Choisir un repertoire') + "/"
        self.format_path = self.rep.replace('/','\\')

        if len(self.rep) > 0:
            try:
                # Affichage du label du path complet
                self.path=StringVar()
                self.path.set(self.rep)
                self.displayPathFolder()

                # declaration des objets
                self.C = Mp3Processing(self.format_path)
                self.B = BuildCover(self.C)

                self.menu_fichier.entryconfig(1, state="active")

                self.displayNameFolder()
                self.displayFontScrollableList()
                self.displaySongsLabels()
                self.displaySongsList(self.C.list_mp3)
            except HeaderNotFoundError:
                print("Aucun fichier .mp3 trouvé !")

    def displayPathFolder(self):
        logging.info("start")
        self.labelPathCD = Label(self.main_pane, textvariable=self.path, width=60)
        self.labelPathCD.pack()

    def deletePathFolder(self):
        try:
            self.labelPathCD.destroy()
        except AttributeError:
            pass

    def displayNameFolder(self):
        logging.info("start")
        self.CDtitre = StringVar()
        self.CDtitre.set(self.C.getDefautCDName())
        self.entryTitreCD = Entry(self.main_pane, textvariable=self.CDtitre, width=20, justify=CENTER)
        self.entryTitreCD.pack()
        self.edited_list_songs=[]

    def deleteNameFolder(self):
        logging.info("start")
        try:
            self.entryTitreCD.destroy()
        except AttributeError:
            pass

    def displaySongsLabels(self):
        logging.info("start")
        # Déclaration des Labels
        i = 0
        self.labeltitre=Label(self.Paned2,text="Title")
        self.labeltitre.grid(row=i,column=0)
        self.labelduree = Label(self.Paned2, text="Length")
        self.labelduree.grid(row=i,column=1)
        self.labelbpm = Label(self.Paned2, text="Key")
        self.labelbpm.grid(row=i,column=2)
        self.labelkey=Label(self.Paned2,text="Tempo")
        self.labelkey.grid(row=i,column=3)

    def deleteSongsLabels(self):
        logging.info("start")
        try:
            self.labeltitre.destroy()
            self.labelbpm.destroy()
            self.labelduree.destroy()
            self.labelkey.destroy()
        except AttributeError:
            pass

    def displaySongsList(self, mp3_dict):
        logging.info("start")
        i=1
        self.edited_list_songs.clear()

        for key, value in mp3_dict.items():
            temp = []
            temp.append(list(mp3_dict.keys())[i-1])
            titre = StringVar(self.Paned2, value=value['display_title'])
            bpm = StringVar(self.Paned2, value=value['tempo'])
            key = StringVar(self.Paned2, value=value['key'])
            duree = StringVar(self.Paned2, value=value['length'])

            # Affichage des titres
            entryTitre = Entry(self.Paned2, textvariable=titre, width=60)

            if len(value["display_title"]) > self.B.title_limit:
                self.labelwarning = Label(self.Paned2, text="Title too long !", fg="indianred1")
                entryTitre.configure(background="indianred1")
            entryTitre.grid(row=i, column=0)
            temp.append(entryTitre)

            entryDuree = Entry(self.Paned2, textvariable=duree, width=8, state='disabled')
            entryDuree.grid(row=i, column=1)
            temp.append(entryDuree)

            entryKey = Entry(self.Paned2, textvariable=key, width=8)
            entryKey.grid(row=i, column=2)
            temp.append(entryKey)


            entryBpm = Entry(self.Paned2, textvariable=bpm, width=8)
            entryBpm.grid(row=i, column=3)
            temp.append(entryBpm)

            self.edited_list_songs.append(list(temp))
            i += 1

        self.labelwarning.grid(row=i, column=0)

        # Déclaration du bouton 'Save'
        self.saveButton = Button(self.Paned2, text='Save', command=self.save, padx=5, pady=5)
        self.saveButton.grid(row=i, column=3)


    def deleteSongsList(self):
        logging.info("start")
        for sons in self.edited_list_songs:
            for a in sons[1:]:
                a.get()
                a.destroy()

        # print(len(self.ListeSongs))

    def displayFontScrollableList(self):
        logging.info("start")
        self.varFont = StringVar(self.Paned2)
        self.varFont.set(self.B.default_font)
        print(self.B.list_font)
        self.spinBoxFont = OptionMenu(self.main_pane, self.varFont, *self.B.list_font)
        self.spinBoxFont.pack()

    def deleteFontScrollableList(self):
        logging.info("start")
        try:
            self.spinBoxFont.destroy()
        except AttributeError:
            pass

    # Enregistre les valeurs des Entry
    def save(self):
        logging.info("start")
        # On recupere la fonte choisie (defaut : standard)
        self.C.default_font = self.varFont.get()
        # On récupere le Titre du CD
        self.C.cover_titre = self.CDtitre.get()


        for elem in self.edited_list_songs:
            self.B.mp3_dict[elem[0]]["display_title_edited"] = str(elem[1].get())
            self.B.mp3_dict[elem[0]]["tempo_edited"] = str(elem[2].get())
            self.B.mp3_dict[elem[0]]["key_edited"] = str(elem[3].get())
            self.B.mp3_dict[elem[0]]["length_edited"] = str(elem[4].get())

        try:
            self.saveButton.destroy()
            self.labelwarning.destroy()
        except AttributeError:
            pass

        # Suppression de l'entry titre du CD
        self.deleteNameFolder()
        self.deletePathFolder()
        self.deleteSongsLabels()
        self.deleteSongsList()
        self.B.buildCover()

    # Genere la cover
    def generate(self):
        logging.info("start")
        try:
            self.labelSucess.destroy()
        except AttributeError:
            pass

        self.B.writeTemplate()
        self.labelSucess=Label(self.root,text="Sucess !")
        self.labelSucess.pack(side="bottom")

    def on_closing(self):
        logging.info("start")
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()



g=Interface()