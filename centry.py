#!/usr/bin/python3
import sys
import argparse
import hashlib
import socket
import select

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

def panic():
  #TODO: Implement timeout
  if os.name == 'nt':                       # Panic options for Windows
    os.popen("truecrypt.exe /wipecache")
  elif os.name == 'posix':                  # Panic Options for Linux and MacOS
    os.popen("truecrypt /wipecache")        # Wipes passwds/keyfiles in TC cache 
                                            #TODO: does this lock disks? Mac?
    os.popen("sdmem -llf")
    os.popen('swapoff')        # Avoid crash due to random overwrititng of swap
    os.popen("sswap")          

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
  s.bind(('<broadcast>', 9999))
  s.setblocking(0)

  while True:
    result = select.select([s],[],[])
    msg = result[0][0].recv(bufferSize)
    print(msg)
    break
  return 1
def hash():
  hash = hashlib.sha256(args.key.encode('UTF-8')).hexdigest()
  return hash

def main():
  if listenbcast()==1:
    print("PANIC PANIC PANIC")

#             When in trouble, 
#		when in doubt,
#		 run Centry,
#		  scream and shout

main()
