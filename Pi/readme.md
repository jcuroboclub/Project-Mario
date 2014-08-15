# Project-Mario/Pi

The brains of the game. This module includes game logic, reading the joysticks, sending serial messages to varioud Arduino modules (RFID stations, Zumos), etc..

## Required Modules/Installation
If time allows, run "sudo apt-get update"

Python 2.7:
sudo apt-get install python

PyGame:
sudo apt-get install python-pygame

PySerial:
sudo apt-get install python-pyserial

Pip:
sudo apt-get install python-pip

ColorConsole:
sudo pip install colorconsole

You also must type "export COLUMNS" and "export LINES" for colorconsole.

Git:
sudo apt-get install pip

Bluetooth:
http://blog.dawnrobotics.co.uk/2013/11/talking-to-a-bluetooth-serial-module-with-a-raspberry-pi/

## Discussion

Joystick input could be implemented using the pygame API, joystick module.
  - Docs: http://www.pygame.org/docs/ref/joystick.html
  - e.g. Usage: http://yameb.blogspot.com.au/2013/01/gamepad-input-in-python.html

Pygame may also be a useful GUI tool? Its only issue is that it is fiddly to install, can't just use pip.

Team: Ashley Gillman, Bryan Quill
