#!/usr/bin/python3
import sys, os
import argparse
import hashlib
import socket
import select
import csv
import gui
import multiprocessing

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
    panic_options = {}
    for key, val in csv.reader(open("centry.conf")):
      panic_options[key] = val
    return panic_options
  else:
    panic_options = {"screenlock":1,"passlock":1,"truecrypt":1,"ram":1,"swap":1,"ecc":1,"hardshutdown":1,"propogate":1}
    w = csv.writer(open("centry.conf", "w"))
    for key, val in panic_options.items():
      w.writerow([key, val])
    return panic_options

def panic():
  #TODO: Implement timeout
  if os.name == 'nt':
    if panic_options['truecrypt']:
      os.popen("truecrypt.exe /wipecache")

    if panic_options['screenlock']:
      winpath = os.environ["windir"]
      os.system(winpath + r'\system32\rundll32 user32.dll, LockWorkStation')
    if panic_options['ecc']:
      os.popen("shutdown /r /f /t 0")
    else:
      os.popen("shutdown /s /f /t 0")

  elif os.name == 'posix':
    if panic_options['truecrypt']:           
      os.popen("truecrypt /wipecache")
     
    if panic_options['ram']:            #TODO: does this lock disks? Mac?
      os.popen("sdmem -llf")

    if panic_options["swap"]:
      os.popen('swapoff')
      os.popen("sswap")

    if panic_options['screenlock']:          
      os.popen("gnome-screensaver-command -lock")

    if panic_options['hardshutdown']:
      if panic_opptions['ecc']:
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

def main():
  w = multiprocessing.Process(target = gui.start).start()
  m = multiprocessing.Process(target = listenbcast).start()
  r = multiprocessing.Process(target = listen).start()

#             When in trouble, 
#		when in doubt,
#		 run Centry,
#		  scream and shout

main()
