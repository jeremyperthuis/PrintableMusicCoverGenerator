import tkinter as tk
root = tk.Tk()
num = 5

pairs = [""]

def my_funct(entry):
    var = pairs.get(entry)
    if var is not None:
        var.set(entry.get())

# r = 0
for _ in range(num):
    e = tk.StringVar()

    y = tk.Entry(root)
    y.bind("<Tab>", lambda event, y=y:my_funct(y))
    y.grid(row=_, column=1)

    z = tk.Entry(root, textvariable=e)
    z.grid(row=_, column=2)
    # r +=1

    pairs.update({y:e})

root.mainloop()