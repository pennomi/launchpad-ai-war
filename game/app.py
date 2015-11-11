"""A generic Panda3D class that handles all windowing, lifecycle management,
and input management, then passes the relevant triggers to a game state class.

Chances are in the future that this will also provide the game state switcher.
"""
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d import core
from game.battle import BattleArena
from pandac.PandaModules import loadPrcFileData

# Window config
loadPrcFileData("", "window-title Launchpad AI War")


ORDER_DURATION = 1.0


class MainApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)  # Old-style classes. Ew.
        self.battle = BattleArena()
        self.taskMgr.doMethodLater(ORDER_DURATION, self.update_orders, 'orders')
        self.taskMgr.add(self.update, "update")
        base.setFrameRateMeter(True)
        self.build_lighting()

    def build_lighting(self):
        # Fog
        exp_fog = core.Fog("scene-wide-fog")
        exp_fog.setColor(0.0, 0.0, 0.0)
        exp_fog.setExpDensity(0.004)
        self.render.setFog(exp_fog)
        self.setBackgroundColor(0, 0, 0)

        # Lights
        spotlight = core.Spotlight("spotlight")
        spotlight.setColor(core.Vec4(1, 1, 1, 1))
        spotlight.setLens(core.PerspectiveLens())
        spotlight.setShadowCaster(True, 2048, 2048)
        spotlight_node = self.render.attachNewNode(spotlight)
        spotlight_node.setPos(10, 60, 50)
        spotlight_node.lookAt(5, 10, 0)
        self.render.setLight(spotlight_node)

        ambient_light = core.AmbientLight("ambientLight")
        ambient_light.setColor(core.Vec4(.25, .25, .25, 1))
        self.render.setLight(self.render.attachNewNode(ambient_light))

        # Enable the shader generator for the receiving nodes
        self.render.setShaderAuto()

    def update(self, task):
        dt = self.taskMgr.globalClock.getDt()
        self.battle.update_camera(dt)
        return Task.cont

    def update_orders(self, task):
        self.battle.update(ORDER_DURATION)
        return Task.again
