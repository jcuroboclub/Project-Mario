import unittest, time
from threading import Thread, Event
from Queue import Queue

class ControlThread(Thread):
	"""Handles communications. Is a continuous timer. Also implements protocol.
	http://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds
	"""
	def __init__(self, zumo, connection, time):
		"""zumo is the Zumo reference where the data is retrieved to be sent.
		connection is where the data is to be sent by calling the write(String)
		method.
		time is the period between messages, in seconds."""
		Thread.__init__(self)
		self.daemon = True
		self.stopped = Event()
		self.zumo = zumo
		self.connection = connection
		self.tick = time

	def run(self):
		while not self.stopped.wait(self.tick):
				self.connection.write(str(chr(0)) + \
					str(self.zumo.getLeft()) + str(self.zumo.getRight()) + \
					str(self.zumo.getAux()) + "\n")
		# Thread is killed when run() ends

	def stop(self):
		self.stopped.set()

class TestControlThread(unittest.TestCase):
	def setUp(self):
		self.connection = _FakeConnection()
		self.zumo = Zumo(self.connection, 0.01)
		self.zumo.beginControl()
		time.sleep(0.011)

	def test_init(self):
		self.assertEqual(chr(64), self.connection.msg[1], "Left Wheel Speed")
		self.assertEqual(chr(64), self.connection.msg[2], "Right Wheel Speed")

	def test_timing(self):
		self.zumo.controlThrustSteer(1,0)
		self.assertEqual(chr(64), self.connection.msg[1], \
			"Before Left Wheel Speed")
		self.assertEqual(chr(64), self.connection.msg[2], \
			"Before Right Wheel Speed")
		time.sleep(0.011)
		self.assertEqual(chr(96), self.connection.msg[1], \
			"After Left Wheel Speed")
		self.assertEqual(chr(96), self.connection.msg[2], \
			"After Right Wheel Speed")

	def test_continuing(self):
		self.zumo.controlThrustSteer(1,0)
		self.assertEqual(chr(64), self.connection.msg[1], \
			"Before Left Wheel Speed")
		self.assertEqual(chr(64), self.connection.msg[2], \
			"Before Right Wheel Speed")
		time.sleep(0.011)
		self.assertEqual(chr(96), self.connection.msg[1], \
			"After 1 Left Wheel Speed")
		self.assertEqual(chr(96), self.connection.msg[2], \
			"After 1 Right Wheel Speed")
		self.zumo.controlThrustSteer(0,0)
		time.sleep(0.011)
		self.assertEqual(chr(64), self.connection.msg[1], \
			"After 2 Left Wheel Speed")
		self.assertEqual(chr(64), self.connection.msg[2], \
			"After 2 Right Wheel Speed")

	def test_stop(self):
		# change
		self.zumo.controlThrustSteer(1,0)
		time.sleep(0.011)
		self.assertEqual(chr(96), self.connection.msg[1], \
			"After 1 Left Wheel Speed")
		self.assertEqual(chr(96), self.connection.msg[2], \
			"After 1 Right Wheel Speed")
		# stop and change again, expect it not to affect
		self.zumo._controlThread.stop()
		self.zumo.controlThrustSteer(0,0)
		time.sleep(0.011)
		self.assertEqual(chr(96), self.connection.msg[1], \
			"After stopping Left Wheel Speed")
		self.assertEqual(chr(96), self.connection.msg[2], \
			"After stopping Right Wheel Speed")

class Zumo:
	"""Logic for Zumo."""
	NO_AUX = 1

	# LED Aux
	BLACK = 2
	RED = 3
	YELLOW = 4
	GREEN = 5
	CYAN = 6
	BLUE = 7
	MAGENTA = 8
	WHITE = 9

	# Buzzer Aux
	POWERUP = 10
	POWERDOWN = 11

	QUEUE_SIZE = 10
	TURN_ANGLE = 30 # degrees turn corresponding to full turn

	def __init__(self, connection, time):
		"""Initialise a Zumo. Requires a connection, which can be anything
		that implements a write() method taking a string as an argument. The
		intention is for this to send messages to the physical Zumo.
		"""
		self._left = 64
		self._right = 64
		self._auxQueue = Queue(Zumo.QUEUE_SIZE)

		self._controlThread = ControlThread(self, connection, time)
		self._controlThread.daemon = True

	def beginControl(self):
		"""Begins a thread for controlling the Zumo."""
		self._controlThread.start()

	def endControl(self):
		"""Begins a thread for controlling the Zumo."""
		self._controlThread.stop()

	def controlThrustSteer(self, thrust, steering):
		"""Provide updated control information from joystick.
		Thrust and Steering expected domain: [-1,1]
		-1: left/rev
		1: right/fwd
		"""
		left, right = self._controlSteering(thrust, steering * Zumo.TURN_ANGLE)
		self._left, self._right = self._coerceSteering(left, right)

	def _controlSteering(self, thrust, theta):
		"""assumes theta in degrees and thrust = -1 (100% rev) to 1 (100% fwd)
		returns a tuple: (left_thrust [-1,1], right_thrust [-1,1])
		http://robotics.stackexchange.com/questions/2011/how-to-calculate-the-right-and-left-speed-for-a-tank-like-rover
		"""
		theta = ((theta + 180) % 360) - 180 # normalize value to [-180, 180)
		thrust = min(max(-1, thrust), 2) # normalize value to [-1, 1.5]

		left = thrust*(theta/90.0 + 0.5);
		left = abs(left+1)-1;
		left = -(abs(-left+1)-1);

		right = thrust*(-theta/90.0 + 0.5);
		right = abs(right+1)-1;
		right = -(abs(-right+1)-1);
		return left, right

	def _coerceSteering(self, left, right):
	    """normalize and coerce [1,127]"""
	    left = int(left * 64 + 64)
	    right = int(right * 64 + 64)
	    left = min(max(1, left), 127)
	    right = min(max(1, right), 127)
	    return left, right

	def getLeft(self):
		return chr(self._left)

	def getRight(self):
		return chr(self._right)

	def getAux(self):
		if self._auxQueue.empty():
			return chr(Zumo.NO_AUX)
		else:
			return chr(self._auxQueue.get())

	def setLED(self, state):
		self._auxQueue.put(state)

	def playSound(self, state):
		self._auxQueue.put(state)

class TestZumo(unittest.TestCase):
	def setUp(self):
		self.connection = _FakeConnection()
		self.zumo = Zumo(self.connection, 0.01)

	def test_Constructor(self):
		self.assertEqual(chr(64), self.zumo.getLeft(), "Init values")
		self.assertEqual(chr(64), self.zumo.getRight(), "Init values")
		self.assertEqual(chr(Zumo.NO_AUX), self.zumo.getAux(), "Init values")

	def test_Forwards(self):
		self.zumo.controlThrustSteer(1, 0)
		self.assertEqual(chr(96), self.zumo.getLeft())
		self.assertEqual(chr(96), self.zumo.getRight())

	def test_FwdLeft(self):
		self.zumo.controlThrustSteer(1, -1)
		self.assertEqual(chr(74), self.zumo.getLeft(), "Slower left")
		self.assertEqual(chr(117), self.zumo.getRight(), "Faster right")

	def test_FwdRight(self):
		self.zumo.controlThrustSteer(1, 1)
		self.assertEqual(chr(117), self.zumo.getLeft(), "Faster left")
		self.assertEqual(chr(74), self.zumo.getRight(), "Slower right")

	def test_Reverse(self):
		self.zumo.controlThrustSteer(-1, 0)
		self.assertEqual(chr(32), self.zumo.getLeft())
		self.assertEqual(chr(32), self.zumo.getRight())

	def test_LED_and_Sound(self):
		self.zumo.setLED(Zumo.WHITE)
		self.assertEqual(chr(Zumo.WHITE), self.zumo.getAux(), "Sets Aux")
		self.assertEqual(chr(Zumo.NO_AUX), self.zumo.getAux(), "Aux is once-off")
		self.zumo.playSound(Zumo.POWERUP)
		self.assertEqual(chr(Zumo.POWERUP), self.zumo.getAux(), "Sets Aux")
		self.assertEqual(chr(Zumo.NO_AUX), self.zumo.getAux(), "Aux is once-off")

	def test_begin(self):
		self.zumo.beginControl()
		time.sleep(0.011)
		self.zumo.controlThrustSteer(1,0)
		self.assertEqual(chr(64), self.connection.msg[1], \
			"Before Left Wheel Speed")
		self.assertEqual(chr(64), self.connection.msg[2], \
			"Before Right Wheel Speed")
		time.sleep(0.011)
		self.assertEqual(chr(96), self.connection.msg[1], \
			"After Left Wheel Speed")
		self.assertEqual(chr(96), self.connection.msg[2], \
			"After Right Wheel Speed")

	def test_stop(self):
		self.zumo.beginControl()
		time.sleep(0.011)
		# change
		self.zumo.controlThrustSteer(1,0)
		time.sleep(0.011)
		self.assertEqual(chr(96), self.connection.msg[1], \
			"After 1 Left Wheel Speed")
		self.assertEqual(chr(96), self.connection.msg[2], \
			"After 1 Right Wheel Speed")
		# stop and change again, expect it not to affect
		self.zumo.endControl()
		self.zumo.controlThrustSteer(0,0)
		time.sleep(0.011)
		self.assertEqual(chr(96), self.connection.msg[1], \
			"After stopping Left Wheel Speed")
		self.assertEqual(chr(96), self.connection.msg[2], \
			"After stopping Right Wheel Speed")

class _FakeConnection:
	def __init__(self):
		self.msg = ""
	def write(self, msg):
		self.msg = msg
		msgBytes = ""
		for char in msg:
			msgBytes += str(ord(char)) + " "
		print("conn send: " + msgBytes + " (" + str(len(msg)) + " bytes)")