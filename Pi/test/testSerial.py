#! /usr/bin/python
# http://blog.dawnrobotics.co.uk/2013/11/talking-to-a-bluetooth-serial-module-with-a-raspberry-pi/
 
import serial
 
bluetoothSerial = serial.Serial( "/dev/rfcomm1", baudrate=9600 )
 
a = None
while a == None:
    try:
        a = float( raw_input( "Please enter the first number: " ) )
    except:
        pass    # Ignore any errors that may occur and try again
 
b = None
while b == None:
    try:
        b = float( raw_input( "Please enter the second number: " ) )
    except:
        pass    # Ignore any errors that may occur and try again
 
bluetoothSerial.write( "{0} {1}".format( a, b ) )
print bluetoothSerial.readline()