import os, re, curses, threading, time, datetime
#from colorconsole import terminal
from pyfiglet import figlet_format

class CLI:
	def __init__(self, screen, noPlayers):
		self._scr = screen;
		screen.clear();
		self._timertext = '0:00';
		self._noPlayers = noPlayers
		self._players = [];
		for i in range(noPlayers):
			self._players.append(Player());

		(self._scrHeight, self._scrWidth) = screen.getmaxyx();
		self._colWidth = self._scrWidth / noPlayers;

		self._logHeight = 0;
		#self._logPanel = Panel(0, self._scrHeight - self._logHeight,
		#	self._scrWidth, self._logHeight, self._scr);

		self.printGameScreen();

	def updateTime(self, t):
		mins, secs = divmod(t.seconds, 60)
		self._timertext = '%s:%02d' % (mins, secs);
		self.printGameScreen();

	def printGameScreen(self):
		# reset
		screen = self._scr
		screen.clear();

		# setup timer
		timerAscii = figlet_format(self._timertext, font='doh',
			width=self._scrWidth, justify='center'); # recommend doh font
		timerAscii = re.sub(' ' * 40 +
			'+\n', '', timerAscii); # remove blank lines
		timerHeight = len(re.findall('\n', timerAscii));

		# print timer
		screen.addstr(1, 1, timerAscii, curses.color_pair(2));

		# player table
		for i in range(self._noPlayers):
			for j in range(timerHeight + 2,
				self._scrHeight - self._logHeight - 1):
				screen.addstr(j, i * self._colWidth + 1, "|");
			screen.addstr(
				timerHeight + 2, i * self._colWidth + 2,
				"Player {}".format(i + 1));

		#self._logPanel.update();

		# debug colours
		for i in range(8):
			screen.addstr(self._scrHeight - 9 + i, self._scrWidth - 1,
				str(i), curses.color_pair(i));

		screen.move(self._scrHeight - 1, 0);
		screen.refresh();

class Player:
	NONE = 0;
	MUSHROOM = 1;
	def __init__(self):
		self.powerup = 0;

class Timer:
	def __init__(self):
		self.remaining = 0;

	def start(self, secs):
		self.remaining = secs;
		self._tick();

	def getTime(self):
		return datetime.timedelta(seconds = self.remaining);

	def _tick(self):
		if self.remaining > 0:
			print(self.remaining)
			self.remaining -= 1;
			t = threading.Timer(1, self._tick);
			t.daemon = True;
			t.start();


class Panel:
	"""Panel for logging, etc."""
	def __init__(self, x, y, width, height, screen):
		self._x = x;
		self._y = y;
		self._width = width;
		self._height = height;
		self._scr = screen;
		self._Borderfg = 7;
		self._Borderbg = 0;
		self._msgs = collections.deque(maxlen=height - 2);
		self.update();

	def update(self):
		x = self._x;
		y = self._y;
		width = self._width;
		height = self._height;
		screen = self._scr;

		# msgs
		for msg in self._msgs:
			None #TODO

		# border
		screen.set_color(self._Borderfg, self._Borderbg);
		for i in range(x + 1, x + width - 1):
			screen.print_at(i, y, '-');
			screen.print_at(i, y + height - 1, '-');
		for i in range(y + 1, y + height - 1):
			screen.print_at(x, i, '|');
			screen.print_at(x + width - 1, i, '|');
		screen.print_at(x, y, '+')
		screen.print_at(x + width - 1, y, '+')
		screen.print_at(x, y + height - 1, '+')

	def log(self, msg, fg=7, bg=0):
		if len(msg) > self._width - 2:
			None#TODO

		if (self._msgs.full()):
			self._msgs.get();
		self._msgs.put({
			'msg': msg,
			'fg': fg,
			'bg': bg
			});

def main(stdscr):
	curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

	cli = CLI(stdscr, 4);
	timer = Timer();
	time.sleep(1);
	cli.updateTime(datetime.timedelta(seconds=500));
	time.sleep(1);

	timer.start(60*3);

	def update():
		cli.updateTime(timer.getTime());
		t = threading.Timer(1, update);
		t.daemon = True;
		t.start();

	update();

	while True:
		None;

if __name__ == '__main__':
	curses.wrapper(main);
	#main(None)
