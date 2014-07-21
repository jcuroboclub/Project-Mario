from colorconsole import terminal

class CLI:
	def __init__(self):
		self._screen = terminal.get_terminal()
		self._screen.clear()

	def startGameScreen(self, noPlayers):
		self._scrnWidth = self._screen.columns()
		self._scrnHeight = self._screen.lines()
		self._colWidth = self._scrnWidth / noPlayers

		self._screen.clear()

		for i in range(noPlayers):
			for j in range(self._scrnHeight):
				self._screen.print_at(i * self._colWidth + 1, j, "|")
			self._screen.print_at(
				i * self._colWidth + 2, 1, "Player {}".format(i + 1))

		self._screen.gotoXY(0, self._scrnHeight)

if __name__ == '__main__':
	cli = CLI()
	cli.startGameScreen(4)