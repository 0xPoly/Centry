Centry v0.1
======
## Introduction ##
Centry is a panic button intended to protect users against Cold Boot Attacks, Direct Memory Access and other forms of live key retrival. Centry is most effective when deployed on systems with Full Disk Encryption. The panic function can be activated through the GUI or through a network request (through browser, smartphone, etc). Upon recieving the panic instruction, Centry will attempt to remove sensitive keys from memory, securily overwrite the RAM and then force a shutdown.
![screenshot](/screenshot.png)
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

## Contributors and License ##
- 0xPoly - [twitter](https://twitter.com/0xPoly)

This is a free open-source program distirbuted under the [GNU General Public License](/LICENSE). Comments, suggestions and pull requests are all heartily encouraged.
