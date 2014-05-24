#!/usr/bin/python3
import sys
import argparse
import hashlib
import socket
import select
import os
import csv

parser = argparse.ArgumentParser(prog="Centry",description="""Panic Button for
                                    the Security Minded""",epilog="Version 0.1")
parser.add_argument("-d", "--daemon", help="Run as a daemon in the background",
                                                            action='store_true')
parser.add_argument("--paranoid", help='Activates paranoid mode. Default: Off',
                                                            action='store_true') 
parser.add_argument("-e","--ecc", help="""Specify this option if running on a
                                         system with Error Correcting Memory""")
#TODO: Elaborate on expalantion of paranoid mode
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
  #TODO: Implement timeout
  if os.name == 'nt':                       # Panic options for Windows
    os.popen("truecrypt.exe /wipecache")
    winpath = os.environ["windir"]
    os.system(winpath + r'\system32\rundll32 user32.dll, LockWorkStation')
  elif os.name == 'posix':                  # Panic Options for Linux and MacOS
    os.popen("truecrypt /wipecache")        # Wipes passwds/keyfiles in TC cache 
                                            #TODO: does this lock disks? Mac?
    os.popen("sdmem -llf")
    os.popen('swapoff')        # Avoid crash due to random overwrititng of swap
    os.popen("sswap")          
    os.popen("gnome-screensaver-command -lock")
  if args.paranoid:
    os.popen("echo 1 > /proc/sys/kernel/sysrq")
    os.popen("echo o > /proc/sysrq-trigger")  #Forces shutdown.
  else:
    os.popen("shutdown -P now")

def listen():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.bind(("",args.port))
  except:
    print("Binding socket Failed. Got root?")
    sys.exit()
  s.listen(1)
  conn, addr = s.accept()
  return 1

def listenbcast():
  bufferSize=256  
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.bind(('<broadcast>',29899))
  s.setblocking(0)

  while True:
    result = select.select([s],[],[])
    msg = result[0][0].recv(bufferSize)
    print(msg)
    break
  return 1

def broadcast_panic():
  s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
  s.setsockopt( socket.SOL_SOCKET, socket.SO_BROADCAST, 1 )
  s.sendto(hash(), ("<broadcast>", 9999 ) )
  s.close()

def wait():
  threading.Thread(target = listen).start()
  threading.Thread(target = listenbcast).start()
  while True:
    if threading.activeCount() < 2:
      break
  return 1
 
def hash():
  hash = hashlib.sha256(args.key.encode('UTF-8')).hexdigest()
  return hash

def main():
  if wait() == 1:
    print("PANIC PANIC PANIC")

#             When in trouble, 
#		when in doubt,
#		 run Centry,
#		  scream and shout

print(configsave())
