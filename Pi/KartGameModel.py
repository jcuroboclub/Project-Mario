import unittest

class KartGameModel:
	"""Model for the overall game logic.

	Example usage might be:
	kgm = KartGameModel(4);
	kgm.setFinishLine(Checkpoint(0))
	kgm.addCheckpoint(Checkpoint(1))
	for (i=2; i<5; i++):
		kgm.addPowerupPoint(Checkpoint(i))
	"""
	def __init__(self, noPlayers, noLaps):
		"""Initialise the Kart race.
		noPlayers: int, number of game players.
		noLaps: int, number of laps to win race.
		"""
		self.noPlayers = noPlayers
		self.noLaps = noLaps
		self.players = []
		self.laps = dict()
		for pNo in range(0, noPlayers-1):
			player = Player()
			self.players.append(player)
			self.laps[id(player)] = 0

	def setFinishLine(self, checkpoint):
		"""Set which checkpoint will act as the finish line.
		checkpoint: Checkpoint, the finish line.
		"""
		self.finishLine = checkpoint
		checkpoint.setAction(self.crossFinishLine)

	def addCheckpoint(self, checkpoint):
		self.checkpoints.append(checkpoint)
		checkpoint.setAction(self.crossCheckpoint)
		self.passedPoints[checkpoint] = false

	def crossFinishLine(self, player):
		passedAll = true
		for cp in self.checkpoints:
			passedAll = passedAll & self.passedPoints[cp]
		if passedAll:
			self.laps[player] += 1;

	def crossCheckpoint(self, checkpoint, player):
		self.passedPoints[checkpoint] = true

	def getNoLaps(self):
		return self.noLaps

	def getLaps(self, player):
		return self.laps[player]

class Checkpoint:
	"""A reference to a physical station."""
	def setAction(self, func):
		"""What should happen when a player passes this point?"""
		self.action = func

class Player:
	"""A reference to a player."""

class TestKartGameModel(unittest.TestCase):
	"""Test suite for TestKartGameModel."""
	def test_lap_counters(self):
		kgm = KartGameModel(4, 3)
		self.assertEqual(3, kgm.getNoLaps())
		