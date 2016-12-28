import random
from game.bot import Bot, Actions
def getEnemies(bot):
      for v in bot.visible_objects:
          if  not v in bot.team:
              return v
class Thomas(Bot):
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
             if v.position == self.position + self.direction:
                 return Actions.Punch
             elif v.position == self.position + 15:
                 return Actions.TurnAround
             else:
                 return Actions.MoveForward


        if visible_objects:
            return Actions.TurnLeft
        elif visible_objects:
            return Actions.StrafeLeft

        return Actions.TurnRight



class SelfDestruct(Bot):
      def update(self, tick_number, visible_objects):
         return Actions.MoveBackward

      def update(self, tick_number, visible_objects):
         return Actions.TurnAround

