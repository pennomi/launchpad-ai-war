import random
from game.bot import Bot,  Actions


class Haydenbot (Bot):
	def update(self, tick_number, visible_objects):
		if tick_number % 3:
			return Actions.MoveForward
		return Actions.TurnLeft
		