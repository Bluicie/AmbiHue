AmbiHue
=======

Python script to intgratePhilips Hue lights with Philips Ambilight TV's for a room wide Ambilight effect.

Installation
============

Install simplejson
Install phue
git clone AmbiHue in preferred directory


Configuration
=============

Configure IP adress of Ambilight TV
Configure IP adress of HUE bridge
Attach HUE lights to zones of Ambilight TV

The HUE light nr's can be found in the official HUE app
              top
         0     1     2
        _______________
     2 |               | 0
       |               |
left 1 |               | 1 right
       |               |
     0 |_______________| 2

         2     1     0
             bottom
             
Running
=======

Press the connect button of the Hue bridge (only the first time you run this script)
run ./AmbiHue.py

Enjoy your Ambilight room
