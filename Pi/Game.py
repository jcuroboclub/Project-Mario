import serial, pygame, curses, threading, time, json, os
from pygame.locals import *
from InputDevice import InputDevice
from Zumo import Zumo
from CLI import CLI, CountdownTimer

class Game:
	"""Project Mario - Starts the Mario Kart style game.
	The C in MVC.
	"""
	__location__ = os.path.realpath(
    	os.path.join(os.getcwd(), os.path.dirname(__file__)));

	timer = CountdownTimer();
	cli = None;
	GAMETIME = 60 * 3; # seconds

	# Setup stuff
	setupState = 0;
	setupStep = [{
			"inst": 'Select configuration number',
			"opts": ['1', '2', '3']
		}];
	conf = {};
	@staticmethod
	def setup(c):
		"""Applies the setups required."""
		if not any(c in s for s in Game.setupStep[Game.setupState]["opts"]):
			Game.cli.log('invalid select from: %s' % 
				Game.setupStep[Game.setupState]["opts"])
			return;
		elif Game.setupState == 0:
			data = open("%s/%s.json" % (Game.__location__, c));
			Game.conf = json.load(data);
			Game.cli.log('loaded %s/%s.json - %s' % (
				Game.__location__, c, Game.conf["meta"]));
		Game.setupState += 1;

	@staticmethod
	def main(stdscr):
		"""The Main Game!!!"""
		# init pygame
		pygame.init();
		pygame.joystick.init();

		noPlayers = pygame.joystick.get_count();

		# no controllers, no game.
		if noPlayers == 0:
			raise(Exception('no controllers detected'))
			return

		# init CLI
		cli = CLI(stdscr, noPlayers);
		Game.cli = cli;
		cli.setEventHandler(Game.inputHandler);

		# run through setup steps
		Game.setupState = 0;
		while Game.setupState < len(Game.setupStep): # still setting up
			cli.log('Setup step %i of %i' % (Game.setupState + 1,
				len(Game.setupStep)));
			cli.instructions = Game.setupStep[Game.setupState]["inst"];
			cli.inputloop();
			time.sleep(0.2); # throttle
		cli.instructions = '(S)tart, (L)ist Serial or (Q)uit';

		# update timer thread
		def update():
			cli.updateTime(Game.timer.getTime());
			t = threading.Timer(0.1, update);
			t.daemon = True;
			t.start();
		update(); # start

		joystick = {};
		ser = {};
		zumo = {};
		# init each joystick
		for i in range(noPlayers):
			# joystick
			def playprint(str):
				cli.playerLog(i, str);
			joystick[i] = InputDevice(playprint);
			joystick[i].start(i);
			steeringAxis = Game.conf["controller"]["steeringAxis"];
			accBtn = Game.conf["controller"]["accBtn"];
			revBtn = Game.conf["controller"]["revBtn"];
			powBtn = Game.conf["controller"]["powBtn"];
			joystick[i].configure(steeringAxis, accBtn, revBtn,
				powBtn);

			# serial/Zumo
			try:
				port = Game.conf["zumoser"][i];
				ser[i] = serial.Serial(port, baudrate=9600);
				zumo[i] = Zumo(ser[i], 0.01);
				# 1 thread per zumo
				zumo[i].beginControlThrustSteer(joystick[i].getSpeed,
					joystick[i].getDir)
				cli.playerTrackXY(i, joystick[i].getDir,
					joystick[i].getSpeed)
				playprint('Initialised on %s' % port)
			except OSError:
				playprint('Could not initialise.')

		InputDevice.startReadThread(0.01); # 1 thread for all joysticks

		while cli.running:
			cli.inputloop();

	@staticmethod
	def inputHandler(win, c):
		"""Example event handler."""
		if 0 < c < 256:
			c = chr(c);
			Game.cli.log('%s > %s' % (Game.cli.instructions, c), 2);
			if Game.setupState < len(Game.setupStep): # setting up
				Game.setup(c)
			if c in 'Ss': # Start
				win.log('Starting');
				Game.timer.start(Game.GAMETIME);
			if c in 'Ll': # List Serial
				print_serial(Game.cli.log);
			if c in 'Qq': # Start
				win.log('Quitting, Goodbye', 3);
				time.sleep(1);
				win.end();

def print_serial(stream):
	stream("Detected available serial ports:")
	ports = InputDevice.serialPorts()
	for i in range(len(ports)):
		stream("{0}: {1}".format(i+1, ports[i]))
	"""
	while True:
		s = raw_input(">")
		try:
			return ports[int(s)-1]
		except ValueError:
			print("Select Port:")"""

if __name__ == '__main__':
	curses.wrapper(Game.main);