import serial, pygame
from pygame.locals import *
from InputDevice import InputDevice
from Zumo import Zumo

def main():
	# TODO CLI
	pygame.init()
	pygame.joystick.init()
	joystick = {}
	ser = {}
	zumo = {}

	# init each joystick
	for i in range(pygame.joystick.get_count()):
		# joystick
		joystick[i] = InputDevice()
		joystick[i].start(i)
		steeringAxis, accBtn, revBtn, powBtn = getConfig(joystick[i])
		joystick[i].configure(steeringAxis, accBtn, revBtn, powBtn)

		# serial/Zumo
		port = choose_serial()
		ser[i] = serial.Serial(port, baudrate=9600)
		zumo[i] = Zumo(ser[i], 0.01)
		zumo[i].beginControlThrustSteer(joystick[i].getSpeed, joystick[i].getDir)
			# 1 thread per zumo

	InputDevice.startReadThread(0.01) # 1 thread for all joysticks

	print("q to exit")
	read = ""
	while read.lower() is not "q":
		read = raw_input('>')
		print joystick[0].getSpeed()

def getConfig(dev):
    """config joystick input"""
    print("Wiggle steering")
    steeringAxis = -1
    while steeringAxis < 0: # wait for config
        try:
            for e in pygame.event.get():
                if (e.type == JOYAXISMOTION) & (
                    abs(dev.js.get_axis(e.axis)) > 0.5): # if more than a half
                    steeringAxis = e.axis # configure
        except Exception as e:
    		print(e)
    print("Steering axis set as axis {}".format(steeringAxis))

    print("Press go")
    accBtn = -1
    while accBtn < 0: # wait for config
        try:
            for e in pygame.event.get():
                if (e.type == JOYBUTTONDOWN):
                    accBtn = e.button # configure
        except Exception:
            None
    print("Acceleration button set as button {}".format(accBtn))

    print("Press reverse")
    revBtn = -1
    while revBtn < 0: # wait for config
        try:
            for e in pygame.event.get():
                if (e.type == JOYBUTTONDOWN):
                    revBtn = e.button # configure
        except Exception:
            None
    print("Reverse button set as button {}".format(revBtn))

    print("Press powerup activate")
    powBtn = -1
    while powBtn < 0: # wait for config
        try:
            for e in pygame.event.get():
                if (e.type == JOYBUTTONDOWN):
                    powBtn = e.button # configure
        except Exception:
            None
    print("Powerup button set as button {}".format(powBtn))

    return steeringAxis, accBtn, revBtn, powBtn

def choose_serial():
    print("Select port:")
    ports = InputDevice.serialPorts()
    for i in range(len(ports)):
        print("{0}: {1}".format(i+1, ports[i]))
    while True:
        s = raw_input(">")
        try:
            return ports[int(s)-1]
        except ValueError:
            print("Select Port:")

if __name__ == '__main__':
	main()