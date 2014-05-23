#!/usr/bin/python3
import sys
import argparse
import hashlib
import socket

parser = argparse.ArgumentParser(prog="Centry",description='Pythonic Panic Program for the Security Minded',
                                 epilog='Version 0.1')
parser.add_argument("-d", "--daemon", help="Run as a daemon in the background", action='store_true')
parser.add_argument("--paranoid", help='Activates paranoid mode. Default: Off', action='store_true') 
#TODO: Elaborate on expalantion of paranoid mode
parser.add_argument("-k", "--key", help="Require key to start panic sequence",)
parser.add_argument('-p','--port', help='Specify port to listen on.',type=int)
args = parser.parse_args()

def panic():
	#TODO: Implement timeout
	if os.name == 'nt':                                        # Panic options for Windows Machines
		os.popen("truecrypt.exe /wipecache")
	elif os.name == 'posix':                                   # Panic Options for Linux and MacOS
		os.popen("truecrypt /wipecache")                   # Wipes all passwords and keyfiles from truecrypt cache 
                                                                   #TODO:IMPORTANT does this lock disks? Mac?
		os.popen("sdmem -llf")
		os.popen("sswap")                                  # need parameters

		if args.paranoid:
			os.popen("echo 1 > /proc/sys/kernel/sysrq")
			os.popen("echo o > /proc/sysrq-trigger")           #Forces shutdown.
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
	

def hash():
	hash = hashlib.sha256(args.key.encode('UTF-8')).hexdigest()
	return hash

def main():
	if listen()== 1:
		print("PANIC PANIC PANIC")

		''' When in trouble, 
			when in doubt,
			 run in circles,
			  scream and shout'''
main()
