#!/usr/bin/python3

import argparse
import hashlib

parser = argparse.ArgumentParser(prog="Centry",description='Pythonic Panic Program for the Security Minded',
                                 epilog='Version 0.1')
parser.add_argument("-d", "--daemon", help="Run as a daemon in the background", action='store_true')
parser.add_argument("--paranoid", help='Activates paranoid mode. Default: Off', action='store_true') 
#TODO: Elaborate on expalantion of paranoid mode
parser.add_argument("-k", "--key", help="Require key to start panic sequence",)
parser.add_argument('-p','--port', help='Specify port to listen on.')
args = parser.parse_args()

def panic():
	#TODO: Implement timeout
	if os.name == 'nt':                                        # Panic options for Windows Machines
		os.popen("truecrypt.exe /wipecache")
	elif os.name == 'posix':                                   #Panic Options for Linux and MacOS
		os.popen("truecrypt /wipecache")                   #Wipes all passwords and keyfiles from truecrypt cache 
                                                                   #TODO:IMPORTANT does this lock disks?
		os.popen("sdmem -llf")                             #Securly wipes the RAM with one run of all zeros.
		os.popen("swapoff")                                #Turns off swap.

	if parser.paranoid:
		os.popen("echo 1 > /proc/sys/kernel/sysrq")        #Enables system event overrides from commandline
		os.popen("echo o > /proc/sysrq-trigger")           #Forces shutdown. Equivilent to holding down power button.
	else:
		os.popen("shutdown -P now")

def hash():
	hash = hashlib.sha256(args.key.encode('UTF-8')).hexdigest()
	return hash

def main():
#	if parser.paranoid:
	print (hash())
main()
		
