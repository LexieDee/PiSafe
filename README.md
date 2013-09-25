# PiSafe

PiSafe is a project that aims to provide software and suggests hardware components to make **secure storage of sensitive media data** (i.e. raw footage, digital photographs and audio) **on the go** possible. At the center of this is a Raspberry Pi (hence the name PiSafe) running on a battery pack and a software that copies data from memory cards (e.g. SecureDigital and CompactFlash) to encrypted storage. 

At the current state of development, PiSafe is a rather crude and cludgy setup: Files from the memory cards are copied by issueing a `rsync` command and the full card is overwritten with zeroes using `dd`. All this is implemented by a python script that listens to dbus/UDisks2 events, a setup that works well with the [Pidora][http://pidora.ca/] distribution. The encryption of the storage is facilitated by using dm-crypt/luks

## Suggested Hardware

In the prototyping setup, the components are put inside a rugged crushproof outdoor case and a cable is routed through a drilled hole. That cable connects a card reader to the Raspberry Pi. The Raspberry Pi is powered by a battery pack designed to work with smartphones and tablets and it works wonderfully with the Pi. 

The encrypted storage can either on be the SD card from which the Raspberry Pi boots, a thumb drive or an external hard disk (which would be prone to damage due to impact). If the internal/boot SD card is used, one USB port would be free and it could e.g. house a 3G/4G internet stick for further expansion (I'm thinking of automatically uploading down-scaled photographs or videos securily to some server, or sending them encrypted via GnuPG/PGP and e-mail, etc.). 

## How it works (short version)

When in a safe environment, hook start the Raspberry Pi using the battery pack as a power source. Attach keyboard, mouse and external display. Now mount and decrypt the encrypted device and start the `pisafe.py` script (this requires root privileges, due to the usage of `dd`), using the path to the encrypted device as target path. Then lock the screen and detach mouse, keyboard and display. Put all the remaining pieces in a protective housing and attach the card reader. From now on, every time you insert a card, it copies the content and then overwrites the complete card. A card reader with status LED is recommended, otherwise it's next to impossible to know when copying and overwriting is finished (and removing the card before that point is not recommended, it messes up the complete setup).  

## Known Problems

Overwriting the cards using `dd` is a rather time-consuming process, especially if the cards are slow and/or have a high capacity. 

## Possible Improvements

Improve the **wiping speed**: 

* selectively run dd on the part of the memory card that contained the data or 
* copy the files differently and wipe after every single file. 
