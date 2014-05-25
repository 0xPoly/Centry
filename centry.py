#!/usr/bin/python3
import sys, os
import argparse
import hashlib
import socket
import select
import csv
import multiprocessing
from tkinter import *

parser = argparse.ArgumentParser(prog="Centry",description="""Panic Button for
                                    the Security Minded""",epilog="Version 0.1")
parser.add_argument("-d", "--daemon", help="Run as a daemon in the background",
                                                            action='store_true')
parser.add_argument("--paranoid", help='Activates paranoid mode. Default: Off',
                                                            action='store_true') 
parser.add_argument("-e","--ecc", help="""Specify this option if running on a
                                         system with Error Correcting Memory""")
parser.add_argument("-k", "--key", help="Require key to start panic sequence",)
parser.add_argument('-p','--port', help='Specify port to listen on.',type=int)
args = parser.parse_args()

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

def panic():
  #TODO: Implement timeout
  if os.name == 'nt':
    if panic['truecrypt']:
      os.popen("truecrypt.exe /wipecache")

    if panic['screenlock']:
      winpath = os.environ["windir"]
      os.system(winpath + r'\system32\rundll32 user32.dll, LockWorkStation')
    if panic['ecc']:
      os.popen("shutdown /r /f /t 0")
    else:
      os.popen("shutdown /s /f /t 0")

  elif os.name == 'posix':
    if panic['truecrypt']:           
      os.popen("truecrypt /wipecache")
     
    if panic['ram']:            #TODO: does this lock disks? Mac?
      os.popen("sdmem -llf")

    if panic["swap"]:
      os.popen('swapoff')
      os.popen("sswap")

    if panic['screenlock']:          
      os.popen("gnome-screensaver-command -lock")

    if panic['hardshutdown']:
      if panic['ecc']:
        os.popen("echo 1 > /proc/sys/kernel/sysrq")
        os.popen("echo b > /proc/sysrq-trigger")
      else:
        os.popen("echo 1 > /proc/sys/kernel/sysrq")
        os.popen("echo o > /proc/sysrq-trigger")
      os.popen("shutdown -P now")

def listentcp():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.bind(("",80))
  except:
    print("Binding socket Failed. Got root?")
    sys.exit()
  s.listen(1)
  conn, addr = s.accept()
  print("TCP PANIC PANIC PANIC")

def listenbcast():
  bufferSize=256  
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.bind(('<broadcast>',29899))
  s.setblocking(0)

  while True:
    result = select.select([s],[],[])
    msg = result[0][0].recv(bufferSize)
    if msg == b'panic\n':
      print("UDP PANIC PANIC PANIC")
      break
    else:
      print("Incorrect Signal Recieved: " + str(msg))
def broadcast_panic():
  s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
  s.setsockopt( socket.SOL_SOCKET, socket.SO_BROADCAST, 1 )
  s.sendto(hash(), ("<broadcast>", 29899 ) )
  s.close()

def hash():
  hash = hashlib.sha256(args.key.encode('UTF-8')).hexdigest()
  return hash

def fire():
  print("FIREIFREFIRE")

def settingswindow():
    v=0
    toplevel = Toplevel()

    title = Label(toplevel, text="Centry Settings", font=('','16','')).pack()

    separator = Frame(toplevel,height=2, bd=1, relief=SUNKEN)
    separator.pack(side='top',fill=X, padx=5, pady=5)

    panic_heading = Label(toplevel, text="On Panic, Centry Will:",
                          font=('',10,'bold'))
    panic_heading.pack()
    global tc, ls, rm, sw, pw
    tc = Button(toplevel,command=lambda:toggle("truecrypt"))
    tc.pack(fill="both", padx=5, pady=5)
    ls = Button(toplevel,command=lambda:toggle("screenlock"))
    ls.pack(fill="both", padx=5, pady=5)
    rm = Button(toplevel,command=lambda:toggle("ram"))
    rm.pack(fill="both", padx=5, pady=5)
    sw = Button(toplevel,command=lambda:toggle("swap"))
    sw.pack(fill="both", padx=5, pady=5)
    pw = Button(toplevel,command=lambda:toggle("propogate"))
    pw.pack(fill="both", padx=5, pady=5)

    separator2= Frame(toplevel,height=2, bd=1, relief=SUNKEN)
    separator2.pack(side='top',fill=X, padx=5, pady=5)

    ecc = Frame(toplevel)
    ecc_heading = Label(ecc, text="RAM Type",font=('',10,'bold'))
    ecc_heading.pack()
    ecc_no = Radiobutton(ecc, text="Normal",variable=v,value=0)
    ecc_no.pack(side="left")
    ecc_yes = Radiobutton(ecc, text="Error Correcting (ECC)",variable=v,
                          value=1)
    ecc_yes.pack(side='right')
    ecc.pack(fill='x')
    ecc_help = Label(toplevel,text="""If unsure, select 'Normal'.\n Selecting \
'ECC' will invoke a restart on panic instead of shutdown, as ECC DRAMs reset\
 all capacitors when power-cycled.""",wraplength=275).pack(pady=5)

    separator3= Frame(toplevel,height=2, bd=1, relief=SUNKEN)
    separator3.pack(side='top',fill=X, padx=5, pady=5)

    restart = Frame(toplevel)
    restart_heading = Label(restart,text='Select Shutdown Mode',
                            font=('',10,'bold')).pack()
    restart_no = Radiobutton(restart, text="Soft",variable=v,value=0)
    restart_no.pack(side="left",anchor='e')
    restart_yes = Radiobutton(restart, text="Hard/ACPI",variable=v, value=1)
    restart_yes.pack(side='right', anchor='w')
    restart.pack(fill='x')
    restart_help = Label(toplevel,text="""If unsure, select 'Soft'.\n ACPI \
shutdown garantees a quicker shutdown and should be used by more paranoid\
 users, but may corrupt data.""",wraplength=275).pack(pady=5)

    separator4= Frame(toplevel,height=2, bd=1, relief=SUNKEN)
    separator4.pack(side='top',fill=X, padx=5, pady=5)
    savebutton = Button(toplevel, text="Save",command=toplevel.quit)
    savebutton.pack(fill='x',padx=5,pady=5)
    print(panic)
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

  status=Label(body)
  status["text"] = "Status: Armed (Paranoid)"
  status['font'] = ('', 14,'')
  status.pack(fill="both")
  body.pack(fill="both")

  mainframe.pack(side='top', fill="both")

  panicf = Frame()
  panic = Button(panicf, text="PANIC",font=('',28,''), bg="#db0303", fg="black"
                 ,activebackground="red", command=fire)
  panic.pack(side="bottom", fill='both')
  panicf.pack(fill=X, padx=5, pady=5,side='bottom')

  app.title("Centry")
  app.geometry("400x165")
  app.iconbitmap("@icon.xbm")
  app.mainloop()

def main():
  global panic
  panic = configsave()
  w = multiprocessing.Process(target = start).start()
  m = multiprocessing.Process(target = listenbcast).start()
  r = multiprocessing.Process(target = listentcp).start()

main()
