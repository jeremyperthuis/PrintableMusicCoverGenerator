from tkinter import filedialog
from tkinter import *
import time
from main import *

class Gui:

    rep=""
    root = Tk()
    root.title("PrintableMusicCoverGenerator v1.0")
    root.minsize(300, 300)
    root.geometry("320x100")
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

    # Action quand on clic sur 'Choose directory'
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


    # Affiche les titres dans une listbox
    def getListe(self,argLst):
        print("getListe")
        liste = Listbox(self.Paned2,width=80)
        i=1
        for elem in argLst:
            liste.insert(i, str(elem))
            i+=1
        liste.pack()

    # Genere la cover
    def generate(self):
        print("generate")
        tex3=Label(self.root,text="Sucess !")
        tex3.pack(side="bottom")


g=Gui()