#!/usr/bin/python3
from tkinter import *

def fire():
  print("FIREIFREFIRE")

v = 0

def settingswindow():
    toplevel = Toplevel()
    title = Label(toplevel, text="Centry Settings", font=('','16',''))
    title.pack()
    separator = Frame(toplevel,height=2, bd=1, relief=SUNKEN)
    separator.pack(side='top',fill=X, padx=5, pady=5)
    panic_heading = Label(toplevel, text="On Panic, Centry Will",font=('',10,'bold'))
    panic_heading.pack()
    truecryptlock = Checkbutton(toplevel, text="Lock Truecrypt Partitions and Wipe Cache")
    truecryptlock.pack(anchor='w')
    lockscreen = Checkbutton(toplevel, text="Lock screen")
    lockscreen.pack(anchor='w')
    clearmemory = Checkbutton(toplevel,text="Securely Overwrite RAM")
    clearmemory.pack(anchor='w')
    propogate = Checkbutton(toplevel, text="Broadcast the Signal to other Machines")
    propogate.pack(anchor='w')
    separator2= Frame(toplevel,height=2, bd=1, relief=SUNKEN)
    separator2.pack(side='top',fill=X, padx=5, pady=5)
    ecc = Frame(toplevel)
    ecc_heading = Label(ecc, text="RAM Type",font=('',10,'bold'))
    ecc_heading.pack()
    ecc_no = Radiobutton(ecc, text="Normal",variable=v,value=0)
    ecc_no.pack(side="left")
    ecc_yes = Radiobutton(ecc, text="Error Correcting (ECC)",variable=v, value=1)
    ecc_yes.pack(side='right')
    ecc.pack(fill='x')
    ecc_help = Label(toplevel,text="If unsure, select 'Normal'.\n Selecting 'ECC' will invoke a restart on panic instead of shutdown, as ECC DRAMs reset all capacitors when power-cycled.",wraplength=275).pack(pady=5)
    separator3= Frame(toplevel,height=2, bd=1, relief=SUNKEN)
    separator3.pack(side='top',fill=X, padx=5, pady=5)
    restart = Frame(toplevel)
    restart_heading = Label(restart,text='Select Shutdown Mode',font=('',10,'bold')).pack()
    restart_no = Radiobutton(restart, text="Soft",variable=v,value=0)
    restart_no.pack(side="left",anchor='e')
    restart_yes = Radiobutton(restart, text="Hard/ACPI",variable=v, value=1)
    restart_yes.pack(side='right', anchor='w')
    restart.pack(fill='x')
    restart_help = Label(toplevel,text="If unsure, select 'Soft'.\n ACPI shutdown garantees a quicker shutdown and should be used by more paranoid users, but may corrupt data.",wraplength=275).pack(pady=5)
    separator4= Frame(toplevel,height=2, bd=1, relief=SUNKEN)
    separator4.pack(side='top',fill=X, padx=5, pady=5)
    savebutton = Button(toplevel, text="Save",command=toplevel.quit)
    savebutton.pack(fill='x',padx=5,pady=5)

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
settings["command"] = settingswindow
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
