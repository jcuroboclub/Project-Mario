import os, re, curses, threading, time, datetime, math
from collections import deque
from pyfiglet import figlet_format

class CLI:
	init = False;
	running = False;
	instructions = '';
	"""Command Line Interface for Project Mario.
	The V in MVC.
	"""
	def __init__(self, screen, noPlayers):
		"""Initialise the screen."""

		self.init = True; # initialising
		self.running = True;

		# Set up colours
		curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

		# General init stuff
		screen.clear();
		self._scr = screen;
		self._timertext = '0:00';
		self._noPlayers = noPlayers;
		(self._scrHeight, self._scrWidth) = screen.getmaxyx();
		self._colWidth = self._scrWidth / noPlayers;

		# set up log window
		self._logHeight = 20;
		self._logscr = screen.derwin(self._logHeight, self._scrWidth,
			self._scrHeight - self._logHeight, 0);
		self._log = deque(maxlen = self._logHeight - 3);
		self._log.append({'msg': 'Welcome to Project Mario'})
		self._log.append({
			'msg': 'Developed by JCU Robo Club, under the JCU IEEE Student Branch.',
			'col': 1})

		# find height of timer for later
		self._timerHeight = len(re.findall('\n', re.sub(' ' * 40 +
			'+\n', '', figlet_format('0:00', font='doh'))));
		self._plrHeight = (self._scrHeight - self._logHeight -
			self._timerHeight + 1);

		# set up player windows
		self._plrscrs = [];
		self._plrlogs = [];
		self._plrX = [];
		self._plrY = [];
		for i in range(noPlayers):
			self._plrscrs.append(screen.derwin(
				self._plrHeight,
				min(self._colWidth + 1, self._scrWidth - i * self._colWidth),
				self._timerHeight,
				i * self._colWidth));
			self._plrlogs.append(deque(
				maxlen = self._plrHeight - 3));
			self._plrX.append(lambda: 0);
			self._plrY.append(lambda: 0);
			self._plrlogs[i].append('Initialising Player %i...' % (i+1));

		self.printGameScreen();

	def updateTime(self, t):
		"""Update the timer value. 't' should be a timedelta object from
		the datetime module.
		"""
		mins, secs = divmod(t.seconds, 60)
		self._timertext = '%s:%02d' % (mins, secs);
		self.printGameScreen();

	def playerTrackXY(self, playerNo, xFun, yFun):
		"""Allow console tracking of input."""
		def intVal(fun):
			if abs(fun()) < 0.1:
				return 0;
			else:
				return int(math.copysign(1, fun()));
		self._plrX[playerNo] = lambda: intVal(xFun);
		self._plrY[playerNo] = lambda: intVal(yFun);

	def playerLog(self, playerNo, msg):
		"""Log a message, msg, for player playerNo."""
		self._plrlogs[playerNo-1].append(msg); # note: deque auto pops
		#self.printGameScreen();

	def log(self, msg, col=False):
		"""Log a message, msg. Optional argument col specified a colour
		as outlined in __init__.
		"""
		if col:
			self._log.append({'msg': msg, 'col': col});
		else:
			self._log.append({'msg': msg});
		#self.printGameScreen();

	def setEventHandler(self, func, *args):
		"""Function to call when user enters input.
		Format: func(char, *args)
		i.e. first argument must be the char entered, subsequent
		arguments may be specified.
		"""
		self._handleFunc = func;
		self._handleArgs = args;

	def printGameScreen(self):
		"""Refresh the screen."""
		# reset
		screen = self._scr
		logscr = self._logscr;
		logscr.clear();
		screen.clear();
		# Is this actually necessary? Haven't cleared plrscrs yet

		# setup timer
		timerAscii = figlet_format(self._timertext, font='doh',
			width=self._scrWidth, justify='center'); # recommend doh font
		timerAscii = re.sub(' ' * 40 +
			'+\n', '', timerAscii); # remove blank lines
		# print timer
		screen.addstr(1, 1, timerAscii, curses.color_pair(1));

		# player table
		for i in range(self._noPlayers):
			(h, w) = self._plrscrs[i].getmaxyx();
			self._plrscrs[i].addstr(1, 2, "Player %i" % (i + 1),
				curses.color_pair(2)); # title at the top
			for j in range(len(self._plrlogs[i])): # each log entry
				self._plrscrs[i].addstr(j + 2, 1, self._plrlogs[i][j]);

			# draw steering in top right
			if (self._plrX[i]() == 0) and (self._plrY[i]() == 0):
				c = '';
			elif self._plrX[i]() == 0:
				c = '|';
			elif self._plrY[i]() == 0:
				c = '-';
			elif self._plrX[i]() == self._plrY[i]():
				c = '/';
			else:
				c = '\\';
			self._plrscrs[i].addstr(2, w-3, 'X', curses.color_pair(1));
			self._plrscrs[i].addstr(2 - self._plrY[i](),
				w-3 + self._plrX[i](), c);

		# log
		for i in range(len(self._log)):
			if 'col' in self._log[i]: # if a colour is specified
				self._logscr.addstr(i + 1, 1, self._log[i]['msg'],
					curses.color_pair(self._log[i]['col']));
			else:
				self._logscr.addstr(i + 1, 1, self._log[i]['msg']);

		# debug colours (just shows colours in corner, no real purpose)
		for i in range(8):
			screen.addstr(2, self._scrWidth - 2,
				str(i), curses.color_pair(i));

		# cursor indicator
		screen.addstr(self._scrHeight - 2, 2, self.instructions);
		screen.addstr(' >', curses.A_BLINK);
		screen.move(self._scrHeight - 2, 3);

		# Update screens
		screen.border('|','|','-','-','+','+','+','+');
		screen.refresh();
		self._logscr.border('|','|','-','-','+','+','+','+');
		self._logscr.refresh();
		for i in range(self._noPlayers):
			self._plrscrs[i].border('|','|','-','-','+','+','+','+');
			self._plrscrs[i].refresh();

	def inputloop(self):
		"""Main program loop. Updates screen, gets input (blocking)."""
		self.printGameScreen();
		self._scr.nodelay(0); # blocking mode
		c = self._scr.getch();
		if self._handleFunc is not None:
			self._handleFunc(self, c, *self._handleArgs)

	def end(self):
		"""Close the interface."""
		self.running = False;

	def write(self, str):
		self.log(str);

class CountdownTimer:
	"""Simple countdown timer module.
	Probably should go in another file.
	"""
	def __init__(self):
		self.remaining = 0;

	def start(self, secs):
		"""Start countdown, of length secs seconds."""
		self.remaining = secs + 1;
		self._tick();

	def getTime(self):
		"""Get remaining time, as a deltatime object (datetime
		module).
		"""
		return datetime.timedelta(seconds = self.remaining);

	def onStop(self, func):
		"""Get remaining time, as a deltatime object (datetime
		module).
		"""
		self._onstop = func;

	def _tick(self):
		"""Calls itself every second until remaining <= 0."""
		if self.remaining > 0:
			#print(self.remaining)
			self.remaining -= 1;
			t = threading.Timer(1, self._tick);
			t.daemon = True;
			t.start();
		else:
			try:
				self._onstop();
			except:
				pass;

def dummyHandler(win, c):
	"""Example event handler."""
	if 0 < c < 256:
		c = chr(c);
		if c in 'Ss': # Start
			win.log('Starting');
		if c in 'Qq': # Start
			win.log('Quitting, Goodbye', 3);
			time.sleep(1);
			win.end();

def main(stdscr):
	## test code

	# setup
	cli = CLI(stdscr, 4);
	cli.setEventHandler(dummyHandler);
	cli.instructions = '(S)tart, (Q)uit ';
	timer = CountdownTimer();
	#time.sleep(1);
	#cli.updateTime(datetime.timedelta(seconds=500));

	# Throw some text out just for demo
	for i in range(20):
		cli.playerLog(1, str(i));
	for i in range(40):
		cli.playerLog(2, str(i));
	time.sleep(1);

	timer.start(60 * 3);
	cli.log('starting timer');

	# update timer thread
	def update():
		cli.updateTime(timer.getTime());
		t = threading.Timer(1, update);
		t.daemon = True;
		t.start();
	update(); # start

	while cli.running:
		cli.inputloop();

if __name__ == '__main__':
	curses.wrapper(main);
	#main(None)
