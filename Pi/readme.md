# Project-Mario/Pi

The brains of the game. This module includes game logic, reading the joysticks, sending serial messages to varioud Arduino modules (RFID stations, Zumos), etc..

## Required Modules/Installation
If time allows, run "sudo apt-get update"

Python 2.7, PyGame, PySerial, Pip:
sudo apt-get install python python-pygame python-serial python-pip

PyFiglet:
sudo pip install git+https://github.com/pwaller/pyfiglet

You also must type "export COLUMNS" and "export LINES" for colorconsole.

Git:
sudo apt-get install pip

Bluetooth:
http://blog.dawnrobotics.co.uk/2013/11/talking-to-a-bluetooth-serial-module-with-a-raspberry-pi/

## Troubleshooting

### Bluetooth Issues
Try:
*$ sudo rfcomm release all*
*$ sudo rfcomm bind all*

*$ sudo hciconfig hci0 up*

Team: Ashley Gillman, Bryan Quill
