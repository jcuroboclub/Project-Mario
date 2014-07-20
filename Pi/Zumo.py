import unittest, time
from threading import Thread, Event

class ControlThread(Thread):
	"""Handles communications. Is a continuous timer.
	http://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds
	"""
	def __init__(self, stopEvent, zumo, connection, time):
		Thread.__init__(self)
		self.daemon = True
		self.stopped = stopEvent
		self.zumo = zumo
		self.connection = connection
		self.tick = time

	def run(self):
		while not self.stopped.wait(self.tick):
				self.connection.write(str(chr(0)) + \
					str(self.zumo.getLeft()) + str(self.zumo.getRight()) + \
					str(self.zumo.getAux()) + "\n")

class TestControlThread(unittest.TestCase):
	def setUp(self):
		self.connection = _FakeConnection()
		self.zumo = Zumo(self.connection)
		self.stopFlag = Event()
		self.thread = ControlThread(self.stopFlag, self.zumo, self.connection, 0.01)
		self.thread.start()
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

class Zumo:
	"""Logic for Zumo."""
	NONE = 1

	def __init__(self, connection):
		self._connection = connection
		self._left = 64
		self._right = 64
		self._aux = Zumo.NONE

	def beginControl(self, updateTime):
		"""Begins a thread for controlling the Zumo."""
		self._tick = updateTime
		self._controlThread = Thread(target = self._control)
		self._controlThread.daemon = True
		self._controlThread.start()
		self._control

	def controlThrustSteer(self, thrust, steering):
		"""Provide updated control information from joystick."""
		left, right = self._controlSteering(thrust, steering)
		self._left, self._right = self._coerceSteering(left, right)

	def _controlSteering(self, thrust, theta):
		"""
		assumes theta in degrees and thrust = -1 (100% rev) to 1 (100% fwd)
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
		return chr(self._aux)

class _FakeConnection:
	def __init__(self):
		self.msg = ""
	def write(self, msg):
		self.msg = msg
		msgBytes = ""
		for char in msg:
			msgBytes += str(ord(char)) + " "
		print("conn send: " + msgBytes + " (" + str(len(msg)) + " bytes)")