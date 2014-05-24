#!/usr/bin/python3
from tkinter import *

def fire():
  print("FIREIFREFIRE")
app = Tk()

mainframe = Frame()

header = Frame(mainframe)
title=Label(header)
title["text"] = "Centry"
title["font"] = ('',32,'bold')
title.pack(side="left", anchor='e',padx=90)
photo = PhotoImage(file="settings.gif")
settings = Button(header)
settings["image"] = photo
settings.pack(side="right",fill='both', anchor="e",pady=5,padx=5)
header.pack(side="top",fill=X)

body = Frame(mainframe)

separator = Frame(body,height=2, bd=1, relief=SUNKEN)
separator.pack(side='top',fill=X, padx=5, pady=5)

status=Label(body)
status["text"] = "Status: Armed (Paranoid)"
status['font'] = ('', 14,'')
status.pack(fill="both")
body.pack(fill="both")

mainframe.pack(side='top', fill="both")

panicf = Frame()
panic = Button(panicf, text="PANIC",font=('',28,''), bg="#db0303", fg="black",activebackground="red", command=fire)
panic.pack(side="bottom", fill='both')
panicf.pack(fill=X, padx=5, pady=5,side='bottom')

app.title("Centry")
app.geometry("400x165")
app.iconbitmap("@icon.xbm")
app.mainloop()
