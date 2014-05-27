#!/usr/bin/python3
#
#     When in Fear,
#       When in Doubt,
#         Run Centry,
#          Scream and Shout
#
#               _( }
#      -=  _  <<  \
#         `.\__/`/\\
#    -=     '--'\\  `
#         -=    //
#               \)
#
#    Licensed under GPL v3 by 0xPoly
#       Inspired by panic_bcast

import sys, os
import time
import hashlib
import socket
import select
import csv
import multiprocessing
from tkinter import *

def configsave():
  if os.path.isfile('centry.conf'):
    panic = {}
    for key, val in csv.reader(open("centry.conf")):
      panic[key] = val
    return panic
  else:
    panic = {"screenlock":1,"passlock":1,"truecrypt":1,"ram":1,"swap":1,
"ecc":1,"hardshutdown":1,"propogate":1}
    w = csv.writer(open("centry.conf", "w"))
    for key, val in panic.items():
      w.writerow([key, val])
    return panic

def toggle(option):
   global panic
   if panic[option] == "1":
     panic[option] = "0"
   else:
     panic[option] = "1"
   w = csv.writer(open("centry.conf", "w"))
   for key, val in panic.items():
     w.writerow([key, val])
   update_settings()

def panic_now():
  if os.name == 'nt':
    try:
      if panic['truecrypt'] == "1":
        os.popen("truecrypt.exe /wipecache")

      if panic['screenlock'] == "1":
        winpath = os.environ["windir"]
        os.system(winpath + r'\system32\rundll32 user32.dll, LockWorkStation')
    except:
        print("something went wrong")
    if panic['ecc'] == "1":
        os.popen("shutdown /r /f /t 0")
    else:
        os.popen("shutdown /s /f /t 0")

  elif os.name == 'posix':
    try:
      if panic['truecrypt'] == "1":           
        os.popen("truecrypt /wipecache")
     
      if panic['ram'] == "1":            #TODO: does this lock disks? Mac?
        os.popen("sdmem -llf")

#      if panic["swap"] == "1":    #TODO find a better way to deal with swap
#        os.popen('swapoff')
#        os.popen("sswap")

      if panic['screenlock'] == "1":
        os.popen("gnome-screensaver-command -lock")

      if panic["propogate"] == "1":
        broadcast_panic()
    except:
      print("something went wrong")

    if panic['hardshutdown'] == "1":
      if panic['ecc'] == "1":
        os.popen("echo 1 > /proc/sys/kernel/sysrq")
        os.popen("echo b > /proc/sysrq-trigger")
      else:
        os.popen("echo 1 > /proc/sys/kernel/sysrq")
        os.popen("echo o > /proc/sysrq-trigger")
    else:
        os.popen("shutdown -P now")

def listentcp():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.bind(("",80))
  except:
    print("WARNING: FAILED TO BIND TO TCP SOCKET. ARE YOU RUNNING AS ROOT?")
    sys.exit()
  s.listen(1)
  conn, addr = s.accept()
  panic_now()

def listenbcast():
  bufferSize=256
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('<broadcast>',29899))
    s.setblocking(0)
  except:
    print("WARNING: FAILED TO BIND TO UDP SOCKET. ARE YOU RUNNING AS ROOT?")

  while True:
    result = select.select([s],[],[])
    msg = result[0][0].recv(bufferSize)
    if msg == b'panic\n':
      panic_now()
      break
    else:
      print("Incorrect Signal Recieved: " + str(msg))
def broadcast_panic():
  msg = b'panic\n'
  s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
  s.setsockopt( socket.SOL_SOCKET, socket.SO_BROADCAST, 1 )
  s.sendto(msg, ("<broadcast>", 29899 ) )
  s.close()

def settingswindow():
    toplevel = Toplevel()

    title = Label(toplevel, text="Centry Settings", font=('','16','')).pack()

    separator = Frame(toplevel,height=2, bd=1, relief=SUNKEN)
    separator.pack(side='top',fill=X, padx=5, pady=5)

    panic_heading = Label(toplevel, text="On Panic, Centry Will:",
                          font=('',10,'bold'))
    panic_heading.pack()
    global tc, ls, rm, sw, pw, ec, sd
    tc = Button(toplevel,command=lambda:toggle("truecrypt"))
    tc.pack(fill="both", padx=5, pady=2)
    ls = Button(toplevel,command=lambda:toggle("screenlock"))
    ls.pack(fill="both", padx=5, pady=2)
    rm = Button(toplevel,command=lambda:toggle("ram"))
    rm.pack(fill="both", padx=5, pady=2)
    sw = Button(toplevel,command=lambda:toggle("swap"))
    sw.pack(fill="both", padx=5, pady=2)
    pw = Button(toplevel,command=lambda:toggle("propogate"))
    pw.pack(fill="both", padx=5, pady=2)

    separator2= Frame(toplevel,height=2, bd=1, relief=SUNKEN)
    separator2.pack(side='top',fill=X, padx=5, pady=5)

    ecc = Frame(toplevel)
    ecc_heading = Label(ecc, text="RAM Type",font=('',10,'bold'))
    ecc_heading.pack()
    ec = Button(ecc, command=lambda:toggle("ecc"))
    ec.pack(fill="both", padx =5, pady=2)
    ecc.pack(fill='x')
    ecc_help = Label(toplevel,text="""If unsure, select 'Non-ECC'.\n Selecting \
'ECC RAM' will invoke a restart on panic instead of shutdown, as ECC DRAMs reset\
 all capacitors when power-cycled.""",wraplength=275).pack(pady=5)

    separator3= Frame(toplevel,height=2, bd=1, relief=SUNKEN)
    separator3.pack(side='top',fill=X, padx=5, pady=5)

    restart = Frame(toplevel)
    restart_heading = Label(restart,text='Shutdown Mode',
                            font=('',10,'bold')).pack()
    sd = Button(restart, command=lambda:toggle("hardshutdown"))
    sd.pack(fill="both", padx=5, pady=2)
    restart.pack(fill='x')
    restart_help = Label(toplevel,text="""If unsure, select 'Soft'.\n ACPI \
shutdown guarantee a quicker shutdown and should be used by more paranoid\
 users, but may corrupt data.""",wraplength=275).pack(pady=5)

    update_settings()

def update_settings():
    if panic["truecrypt"] == "1":
       tc.config(text="Lock Truecrypt Disks and Wipe Cache")
    else:
       tc.config(text="NOT Lock Truecrypt Disks or Wipe Cache")
    if panic["screenlock"] == "1":
       ls.config(text="Lock Screen")
    else:
       ls.config(text="NOT Lock Screen")
    if panic["swap"] == "1":
       sw.config(text="Securely Wipe Swap")
    else:
       sw.config(text="NOT Wipe Swap")
    if panic["ram"] == "1":
       rm.config(text="Securely erase RAM")
    else:
       rm.config(text="NOT Erase RAM")
    if panic["propogate"] == "1":
       pw.config(text="Propogate the Panic Signal")
    else:
       pw.config(text="NOT Propogate the Panic Signal")
    if panic["ecc"] == "1":
       ec.config(text="Error Correcting Code RAM")
    else:
       ec.config(text="Non-ECC RAM")
    if panic["hardshutdown"] == "1":
       sd.config(text="Hard/ACPI Shutdown")
    else:
       sd.config(text="Soft Shutdown")

def start():
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
  panic = Button(body, text="PANIC",font=('',28,''), bg="#db0303", fg="black"
                 ,activebackground="red", command=lambda:panic_now())
  panic.pack(side="bottom", fill='both',pady=5,padx=5)
  body.pack(fill="both")
  mainframe.pack(side='top',fill='both')
  app.title("Centry")
  app.geometry("400x125")
  app.iconbitmap("@icon.xbm")
  app.mainloop()

def main():
  global panic
  panic = configsave()
  m = multiprocessing.Process(target = listenbcast).start()
  r = multiprocessing.Process(target = listentcp).start()
  w = multiprocessing.Process(target = start).start()

main()
