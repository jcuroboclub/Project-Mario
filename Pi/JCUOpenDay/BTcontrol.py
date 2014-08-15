import sys, glob, time, serial, pygame.joystick
#import pygame.joystick
from pygame.locals import *

def serial_ports():
    """Returns all available COM ports
    http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    """
    if sys.platform.startswith('win'):
        result = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                s.close()
                result.append('COM' + str(i + 1))
            except serial.SerialException:
                pass
        return result

    elif sys.platform.startswith('linux'):
        return glob.glob('/dev/rf*')

    elif sys.platform.startswith('darwin'):
        return glob.glob('/dev/tty.*')

def choose_serial():
    print("Select port:")
    ports = serial_ports()
    for i in range(len(ports)):
        print("{0}: {1}".format(i+1, ports[i]))
    port = None
    while not port:
        s = raw_input(">")
        try:
            return ports[int(s)-1]
        except ValueError:
            print("Select Port:")

# http://robotics.stackexchange.com/questions/2011/how-to-calculate-the-right-and-left-speed-for-a-tank-like-rover
def control_steering(thrust, theta):
	# assumes theta in degrees and thrust = -1 (100% rev) to 1 (100% fwd)
	# returns a tuple of percentages: (left_thrust [-1,1], right_thrust [-1,1])
	theta = ((theta + 180) % 360) - 180  # normalize value to [-180, 180)
	thrust = min(max(-1, thrust), 2)              # normalize value to [-1, 1.5]

	left = thrust*(theta/90.0 + 0.5);
	left = abs(left+1)-1;
	left = -(abs(-left+1)-1);

	right = thrust*(-theta/90.0 + 0.5);
	right = abs(right+1)-1;
	right = -(abs(-right+1)-1);
	return left, right

def format_steering(left, right):
    """normalize and coerce [1,127]"""
    left = int(left * 64 + 64)
    right = int(right * 64 + 64)
    left = min(max(1, left), 127)
    right = min(max(1, right), 127)
    return left, right

class FakeSerial:
    """Fake Serial"""
    def write(self, str):
        print(str)       

class InputDevice:
    """"""
    devs = {}

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self._clock = pygame.time.Clock()
        self._speed = 0
        self._dir = 0
        self._boost = 1

    def start(self, id):
        """init joystick"""
        self._js = pygame.joystick.Joystick(id)
        self._js.init()
        InputDevice.devs[id] = self
        print("Using {0}: {1}".format(self._js.get_name(), self._js.get_id()))

    def configure(self):
        js = self._js
        """config joystick input"""
        print("Found {} axes".format(js.get_numaxes()))
        #print("Wiggle steering")
        #self._steeringAxis = -1
        #while self._steeringAxis < 0: # wait for config
        #    try:
        #        for e in pygame.event.get():
        #            if (e.type == JOYAXISMOTION) & (
        #                abs(js.get_axis(e.axis)) > 0.5): # if value is more than a half
        #                self._steeringAxis = e.axis # configure
        #    except Exception:
        #        None
        #    self._clock.tick(10)
	self._steeringAxis = 0 # configure
        print("Steering axis set as axis {}".format(self._steeringAxis))

        #print("Press go")
        #self._accBtn = -1
        #while self._accBtn < 0: # wait for config
        #    try:
        #        for e in pygame.event.get():
        #            if (e.type == JOYBUTTONDOWN):
        #                self._accBtn = e.button # configure
        #    except Exception:
        #        None
        #    self._clock.tick(10)
	self._accBtn = 2 # configure
        print("Acceleration button set as button {}".format(self._accBtn))

        #print("Press reverse")
        #self._revBtn = -1
        #while self._revBtn < 0: # wait for config
        #    try:
        #       for e in pygame.event.get():
        #            if (e.type == JOYBUTTONDOWN):
        #                self._revBtn = e.button # configure
        #    except Exception:
        #        None
        #    self._clock.tick(10)
	self._revBtn = 1 # configure
        print("Reverse button set as button {}".format(self._revBtn))

        #print("Press powerup activate")
        #self._powBtn = -1
        #while self._powBtn < 0: # wait for config
        #    try:
        #        for e in pygame.event.get():
        #            if (e.type == JOYBUTTONDOWN):
        #                self._powBtn = e.button # configure
        #    except Exception:
        #        None
        #    self._clock.tick(10)
	self._powBtn = 0 # configure
        print("Reverse button set as button {}".format(self._powBtn))

    def getSpeed(self):
        """Get fwd/rev direction"""
        return self._speed * self._boost

    def getDir(self):
        """Get turning value"""
        return self._dir

    @staticmethod
    def readInput():
        """Update input from controller (parse events)."""
        for e in pygame.event.get():
            try:
                id = e.joy
                print id
                dev = InputDevice.devs[id]
                if e.type == JOYBUTTONDOWN:
                    if e.button == dev._accBtn:
                        dev._speed = 1
                    elif e.button == dev._revBtn:
                        dev._speed = -1
                    elif e.button == dev._powBtn:
                        dev._boost = 2
                elif e.type == JOYBUTTONUP:
                    if e.button == dev._accBtn:
                        dev._speed = 0
                    elif e.button == dev._revBtn:
                        dev._speed = 0
                    elif e.button == dev._powBtn:
                        dev._boost = 1
                elif e.type == JOYAXISMOTION:
                    if e.axis == dev._steeringAxis:
                        dev._dir = dev._js.get_axis(dev._steeringAxis)
            except Exception:
                None

pygame.init()
pygame.joystick.init()
joystick = {}
ser = {}
for i in range(pygame.joystick.get_count()):
    joystick[i] = InputDevice()
    joystick[i].start(i)
    joystick[i].configure()
    port = choose_serial()
    ser[i] = serial.Serial(port, baudrate=9600)

while True:
    InputDevice.readInput()
    for i in range(pygame.joystick.get_count()):

        left, right = control_steering(
            joystick[i].getSpeed(), joystick[i].getDir()*30)
        left, right = format_steering(left, right)

        ser[i].write(
            str(chr(0)) + str(chr(left)) + str(chr(right)) + str(chr(1)) + "\n")
        print("Joystick " + str(i) + ": " + str(left) + " " + str(right) + \
            " " + str(0) + "\n")

    time.sleep(.05)
