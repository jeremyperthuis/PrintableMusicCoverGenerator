from tkinter import filedialog
from tkinter import *
from tkinter import font
import time
from main import *

class Gui:

    rep=""
    root = Tk()


    def __init__(self):

        self.root.title("TextCoverSongTitle v1.0")
        self.root.minsize(300, 300)
        self.root.geometry("320x100")


        self.Paned1=PanedWindow(self.root, orient=HORIZONTAL)
        self.Paned1.pack(side=TOP, padx=5, pady=5)
        btnChoixDir = Button(self.Paned1, text='Choose directory', command=self.choixrep)
        btnChoixDir.pack()
        self.Paned2=PanedWindow(self.root, orient=HORIZONTAL)
        self.Paned2.pack()

        btnExit = Button(self.root, text='Exit', command=self.root.destroy)
        btnExit.pack(side="left",anchor="s",padx=5, pady=5)

        btnGenerate = Button(self.root, text='Generate', command="")
        btnGenerate.pack(side="right",anchor="s",padx=5,pady=5)


        self.root.mainloop()


    def choixrep(self):

        self.rep = filedialog.askdirectory(initialdir="/", title='Choisissez un repertoire')+"/"
        if len(self.rep) > 0:
            print("vous avez choisi le repertoire %s" % self.rep)
            value=StringVar()
            value.set(self.rep)
            tex2 = Entry(self.Paned1, textvariable=value, width=30)
            tex2.pack()
            self.C = Cover(self.rep)
            self.getListe(self.C.listMusicTitleFormat)


    def getListe(self,argLst):
        liste = Listbox(self.Paned2,width=60)
        i=1
        for elem in argLst:
            liste.insert(i, str(elem))
            i+=1
        liste.pack()

    # def Generate(self):
    #
    #     tex3=Label(self.Paned2,text="Sucess !")
    #     tex3.pack()

    def getLog(sel,log):
        print(log)


g=Gui()