Centry
======
## Introduction ##
Centry is a panic button intended to protect users against [Cold Boot Attacks](http://www1.cs.fau.de/filepool/projects/coldboot/fares_coldboot.pdf), [Direct Memory Access Attacks](http://www.breaknenter.org/projects/inception/) and other live system threats. Centry is most effective when deployed on systems with Full Disk Encryption and without a swap/page file. The panic function can be activated through the GUI or through a network request (through browser, smartphone, etc). Upon recieving the panic instruction, Centry will attempt to remove sensitive keys from memory, securily overwrite the RAM and then force a shutdown.

![screenshot](/screenshot.png)
## Features ##
* User-friendly GUI interface
* When in panic mode, Centry can:
  * Lock the screen
  * Unmount all Truecrypt disks and clear the password/keyfile cache
  * Write zeros to RAM using sdmem (on UNIX-like systems)
  * Force an ACPI shutdown (equivilent holding down the power button)
  * Propogate the panic signal to all other nodes in the network
* Settings to improve security on ECC-enabled systems
* Extensively customizable
* Compatable with Windows, Linux and Mac OS; with significantly more security in Linux.

## Installation ##
####Windows####
* Install `python 3.4` from the [here](https://www.python.org/ftp/python/3.4.1/python-3.4.1.msi)
* Download the [Windows-optimized version](http://darkdepths.net/centry-windows.zip)
* Unzip the archive
* Double click on "Centry.py"

####Linux####
For significantly improved security install the `secure-delete` package. On Ubuntu/Debian:

     sudo apt-get install secure-delete

Then download and run Centry as root:

     git clone https://github.com/0xPoly/Centry.git
     sudo python centry.py

## Contributors and License ##
- 0xPoly - [twitter](https://twitter.com/0xPoly)

This is a free open-source program distirbuted under the [GNU General Public License](/LICENSE). Comments, suggestions and pull requests are all heartily encouraged.
