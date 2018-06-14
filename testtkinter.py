from tkinter import *
tk=Tk()


defaut=["ok", "cool", "1234"]

def TakeInput():
    for entry in entries:
        print(entry.get())

entries=[]
for elem in defaut:
    mot = StringVar(tk, value=elem)
    entry=Entry(tk, textvariable=mot)
    entry.grid(column=0)
    entries.append(entry)


#Button
b=Button(tk,text="PrintInput",command= TakeInput)
b.grid(column=0)
tk.mainloop()