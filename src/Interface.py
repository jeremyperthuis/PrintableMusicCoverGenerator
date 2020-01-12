# coding: utf8
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from mutagen.mp3 import HeaderNotFoundError
from src.BuildCover import *
import logging
import configparser
from pyfiglet import Figlet


class Interface:

    root = Tk()
    rep = ""
    edited_list_songs = []
    config = configparser.ConfigParser()
    count = 0

    def __init__(self):
        self.initLogging()
        self.initConfigParser()
        self.root.title("Cover CD v1.6")
        self.root.minsize(600, 500)
        self.root.config(background=self.config["color"]["rootBackground"])
        self.setup()

    def initLogging(self):
        logging.basicConfig(format='%(asctime)s  %(levelname)s : %(funcName)s  %(message)s')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    def initConfigParser(self):
        self.config.read("themes/default.ini")

    def setup(self):
        logging.info("start")
        self.displayMenuBar()

        # Panel Choix Dossier & Liste Mp3
        self.main_pane = PanedWindow(self.root, orient=HORIZONTAL,
                                                bg=self.config["color"]["paneBackground"])
        self.main_pane.pack(side=TOP)

        self.Paned2=PanedWindow(self.root, orient=HORIZONTAL,bg=self.config["color"]["paneBackground"])
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
            self.deleteFigletTitle()
            self.deletePathFolder()
            self.deleteNameFolder()
            self.deleteFontScrollableList()
            self.deleteSongsLabels()
            self.deleteSongsList()
            self.deleteSaveButton()
            self.labelwarning.destroy()
        except AttributeError:
            pass


        # La fenetre de selection de dossier apparait
        self.rep = filedialog.askdirectory(initialdir=getLastPath(), title='Choisir un repertoire') + "/"
        self.format_path = os.path.abspath(self.rep)

        if len(self.rep) > 0:
            try:
                # Affichage du label du path complet
                self.path=StringVar()
                self.path.set(self.rep)

                # declaration des objets
                self.C = Mp3Processing(self.format_path)
                self.B = BuildCover(self.C)

                # reinitialise les objets lors de l'ouverture d'un nouveau dossier
                if self.count > 0:
                    self.C.__init__(self.format_path)
                    self.B.__init__(self.C)
                self.count += 1

                self.displayFigletTitle()
                self.displayPathFolder()


                self.menu_fichier.entryconfig(1, state="active")

                self.displayNameFolder(self.C.getDefautCDName())
                self.displayFontScrollableList()
                self.displaySongsLabels()
                self.displaySongsList(self.C.list_mp3)
                self.displaySaveButton()
            except HeaderNotFoundError:
                print("Aucun fichier .mp3 trouvé !")

    def displayFigletTitle(self):
        f = Figlet(font=self.B.default_font)
        text = str(f.renderText(self.B.defaut_CD_title))
        self.figlet_title = Label(self.main_pane, text=text, font=self.config["font"]["FigletTitle"], justify=LEFT, bg= self.config["color"]["paneBackground"])
        self.figlet_title.pack()

    def deleteFigletTitle(self):
        try:
            self.figlet_title.destroy()
        except AttributeError:
            pass

    def displayPathFolder(self):
        logging.info("start")
        self.labelPathCD = Label(self.main_pane, textvariable=self.path, width=60,bg=self.config["color"]["paneBackground"])
        self.labelPathCD.pack()

    def deletePathFolder(self):
        try:
            self.labelPathCD.destroy()
        except AttributeError:
            pass

    def displayNameFolder(self,nameCD):
        logging.info("start")
        self.CDtitre = StringVar()
        self.CDtitre.set(nameCD)
        self.entryTitreCD = Entry(self.main_pane, textvariable=self.CDtitre, width=20, justify=CENTER,bg=self.config["color"]["paneBackground"],relief="solid")
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
        self.labeltitre=Label(self.Paned2,text="Title",bg=self.config["color"]["paneBackground"])
        self.labeltitre.grid(row=i,column=0)
        self.labelduree = Label(self.Paned2, text="Length",bg=self.config["color"]["paneBackground"])
        self.labelduree.grid(row=i,column=1)
        self.labelbpm = Label(self.Paned2, text="Key",bg=self.config["color"]["paneBackground"])
        self.labelbpm.grid(row=i,column=2)
        self.labelkey=Label(self.Paned2,text="Tempo",bg=self.config["color"]["paneBackground"])
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
            entryTitre = Entry(self.Paned2, textvariable=titre, width=60,bg=self.config["color"]["paneBackground"],relief="solid")
            if len(value["display_title"]) > self.B.title_limit:
                self.labelwarning = Label(self.Paned2, text="Title too long !", fg=self.config['color']['labelWarningColor'],bg=self.config["color"]["paneBackground"])
                entryTitre.configure(background="indianred1")
            entryTitre.grid(row=i, column=0)
            temp.append(entryTitre)

            entryDuree = Entry(self.Paned2, textvariable=duree, width=8, state='disabled',disabledbackground=self.config["color"]["paneBackground"],disabledforeground ="black",relief="solid")
            entryDuree.grid(row=i, column=1)
            temp.append(entryDuree)

            entryKey = Entry(self.Paned2, textvariable=key, width=8,bg=self.config["color"]["paneBackground"],relief="solid")
            entryKey.grid(row=i, column=2)
            temp.append(entryKey)

            entryBpm = Entry(self.Paned2, textvariable=bpm, width=8,bg=self.config["color"]["paneBackground"],relief="solid")
            entryBpm.grid(row=i, column=3)
            temp.append(entryBpm)

            self.edited_list_songs.append(list(temp))
            i += 1

        try:
            self.labelwarning.grid(row=i, column=0)
        except AttributeError:
            pass

    def displaySaveButton(self):
        logging.info("start")
        self.saveButton = Button(self.Paned2, text='Save', command=self.save, padx=5, pady=5,
                                 bg=self.config["color"]["paneBackground"], relief="solid")
        self.saveButton.grid()

    def deleteSaveButton(self):
        logging.info("start")
        try:
            self.saveButton.destroy()
        except AttributeError:
            pass

    def deleteSongsList(self):
        try:
            logging.info("start")
            for sons in self.edited_list_songs:
                for a in sons[1:]:
                    a.get()
                    a.destroy()
        except AttributeError:
            pass

        # print(len(self.ListeSongs))

    def displayFontScrollableList(self):
        logging.info("start")
        self.varFont = StringVar(self.Paned2)
        self.varFont.set(self.B.default_font)
        self.spinBoxFont = OptionMenu(self.main_pane, self.varFont, *self.B.list_font)
        self.spinBoxFont.config(bg=self.config["color"]["paneBackground"],
                                activebackground=self.config["color"]["paneBackground"],
                                padx=1,
                                pady=1,
                                relief="solid",
                                highlightthickness=0,
                                highlightcolor=self.config["border"]["scrollableList"],
                                borderwidth=1)
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
        self.B.default_font = self.varFont.get()
        # On récupere le Titre du CD
        self.B.defaut_CD_title = self.CDtitre.get()



        for elem in self.edited_list_songs:
            self.B.mp3_dict[elem[0]]["display_title"] = str(elem[1].get())
            self.B.mp3_dict[elem[0]]["length"] = str(elem[2].get())
            self.B.mp3_dict[elem[0]]["key"] = str(elem[3].get())
            self.B.mp3_dict[elem[0]]["tempo"] = str(elem[4].get())

        self.generate()
        try:
            self.saveButton.destroy()
            self.labelwarning.destroy()
        except AttributeError:
            pass

        # Suppression de l'entry titre du CD
        self.deleteFigletTitle()
        self.deleteNameFolder()
        self.deletePathFolder()
        self.deleteSongsLabels()
        self.deleteSongsList()
        self.deleteFontScrollableList()

        self.B.buildHeader()
        self.B.buildListSongs()

        self.displayFigletTitle()
        self.displayPathFolder()
        self.displayNameFolder(self.B.defaut_CD_title)
        self.displayFontScrollableList()
        self.displaySongsLabels()
        self.displaySongsList(self.B.mp3_dict)
        self.displaySaveButton()

    # Genere la cover
    def generate(self):
        logging.info("start")
        try:
            self.labelSucess.destroy()
        except AttributeError:
            pass
        self.B.buildListSongs()
        self.B.writeTemplate()
        self.labelSucess=Label(self.root,text="Tracklist générée", bg=self.config["label"]["generateBackground"])
        self.labelSucess.pack(side="bottom")

    def on_closing(self):
        logging.info("start")
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()



g=Interface()