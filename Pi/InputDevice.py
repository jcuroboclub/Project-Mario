import sys, glob, pygame.joystick, unittest

class InputDevice:
    """Handles the joystick input."""
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
        self.js = pygame.joystick.Joystick(id)
        self.js.init()
        InputDevice.devs[id] = self

    def configure(self):
        js = self.js
        """config joystick input"""
        print("Found {} axes".format(js.get_numaxes()))
        print("Wiggle steering")
        self._steeringAxis = -1
        while self._steeringAxis < 0: # wait for config
            try:
                for e in pygame.event.get():
                    if (e.type == JOYAXISMOTION) & (
                        abs(js.get_axis(e.axis)) > 0.5): # if value is more than a half
                        self._steeringAxis = e.axis # configure
            except Exception:
                None
            self._clock.tick(10)
        print("Steering axis set as axis {}".format(self._steeringAxis))

        print("Press go")
        self._accBtn = -1
        while self._accBtn < 0: # wait for config
            try:
                for e in pygame.event.get():
                    if (e.type == JOYBUTTONDOWN):
                        self._accBtn = e.button # configure
            except Exception:
                None
            self._clock.tick(10)
        print("Acceleration button set as button {}".format(self._accBtn))

        print("Press reverse")
        self._revBtn = -1
        while self._revBtn < 0: # wait for config
            try:
                for e in pygame.event.get():
                    if (e.type == JOYBUTTONDOWN):
                        self._revBtn = e.button # configure
            except Exception:
                None
            self._clock.tick(10)
        print("Reverse button set as button {}".format(self._revBtn))

        print("Press powerup activate")
        self._powBtn = -1
        while self._powBtn < 0: # wait for config
            try:
                for e in pygame.event.get():
                    if (e.type == JOYBUTTONDOWN):
                        self._powBtn = e.button # configure
            except Exception:
                None
            self._clock.tick(10)
        print("Reverse button set as button {}".format(self._revBtn))

    def getSpeed(self):
        """Get fwd/rev direction"""
        return self._speed * self._boost

    def getDir(self):
        """Get turning value"""
        return self._dir

    @staticmethod
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
                        dev._dir = dev.js.get_axis(dev._steeringAxis)
            except Exception:
                None

class TestInputDevice(unittest.TestCase):
    def setUp(self):
        joystick1 = InputDevice()
        joystick1.start()
        joystick2 = InputDevice()
        joystick2.start()

