Centry
======
## Introduction ##
Centry is a panic button intended to protect users against Cold Boot Attacks, Direct Memory Access and other forms of live key retrival. Once installed on a computer, Centry employs extensive methods. Centry is most effective when deployed on systems with Full Disk Encryption.

## Features ##
* User-friendly GUI interface, 
* Upon hitting the Panic Button, Centry will:
  * Lock the screen
  * Unmount all Truecrypt disks and clear the password/keyfile cache
  * Umount all crypto disks under UNIX-like systems
  * Lock password manager
  * Write zeros to RAM
  * Clear out swap file
  * Force an ACPI shutdown (like holding down the power button)
  * Propogate the panic signal to all other nodes in the network
* Garanteed system shutdown within 5 seconds of recieving the panic signal.
* Compatable with Windows, Linux and Mac OS
* 100% Python Code

## Installation ##
TODO

## Contributors ##

- OxPoly - [twitter](https://twitter.com/OxPoly)
