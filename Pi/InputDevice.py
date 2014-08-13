import sys, glob, time, pygame.joystick, unittest
from threading import Thread, Event

class InputDevice:
    """Handles the joystick input."""
    devs = {}
    _updateThread = None

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self._clock = pygame.time.Clock()
        self._speed = 0
        self._dir = 0

    def start(self, id):
        """init joystick"""
        self.js = pygame.joystick.Joystick(id)
        self.js.init()
        InputDevice.devs[id] = self

    def configure(self, steeringAxis, accBtn, revBtn, powBtn):
        """Configure axis and button IDs for the current joystick."""
        self._steeringAxis = steeringAxis
        self._accBtn = accBtn
        self._revBtn = revBtn
        self._powBtn = powBtn

    def getSpeed(self):
        """Get fwd/rev direction"""
        return self._speed

    def getDir(self):
        """Get turning value"""
        return self._dir

    @staticmethod
    def serialPorts():
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
        while True:
            for e in pygame.event.get():
                try:
                    id = e.joy
                    dev = InputDevice.devs[id]
                    if e.type == 10: # JOYBUTTONDOWN
                        #print("Player {0} Pressed {1}".format(id, e.button))
                        if e.button == dev._accBtn:
                            dev._speed = 1
                        elif e.button == dev._revBtn:
                            dev._speed = -1
                        elif e.button == dev._powBtn:
                            dev._boost = 2
                    elif e.type == 11: # JOYBUTTONUP
                        if e.button == dev._accBtn:
                            dev._speed = 0
                        elif e.button == dev._revBtn:
                            dev._speed = 0
                        elif e.button == dev._powBtn:
                            dev._boost = 1
                    elif e.type == 7: # JOYAXISMOTION
                        if e.axis == dev._steeringAxis:
                            dev._dir = dev.js.get_axis(dev._steeringAxis)
                except Exception:
                    None
            time.sleep(0.01) # throttle

    @staticmethod
    def startReadThread(time):
        if InputDevice._updateThread is None: # check not already running
            InputDevice._updateThread = Thread(target = InputDevice.readInput)
            InputDevice._updateThread.daemon = True
            InputDevice._updateThread.start()

class TestInputDevice(unittest.TestCase):
    """Note: For these tests to pass there must be two controllers
    plugged in.
    """
    def setUp(self):
        self.joystick1 = InputDevice()
        self.joystick1.start(0)
        self.joystick2 = InputDevice()
        self.joystick2.start(1)

    def test_initial(self):
        self.assertEqual(0, self.joystick1.getSpeed(), "Init speed")
        self.assertEqual(0, self.joystick1.getDir(), "Init direction")

    def test_noInput(self):
        InputDevice.readInput()
        self.assertEqual(0, self.joystick1.getSpeed(), "Init speed")
        self.assertEqual(0, self.joystick1.getDir(), "Init direction")
