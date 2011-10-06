import rabbyt
from lepton import default_system
from pyglet.window import key, Window
from pyglet import resource


class World(object):

    def __init__(self, player1):

        self.p1 = player1
        self.keys = key.KeyStateHandler()
        self.map_objects = []
        self.player_objects = []
        self.input = {
            key.W : ('move', 'up'),
            key.A : ('rotate', 'left'),
            key.S : ('move', 'down'),
            key.D : ('rotate', 'right'),
            key.LEFT : ('turret', 'left'),
            key.RIGHT: ('turret', 'right'),
            key.SPACE: ('fire', '')
        }

        self.window = Window(width=1280, height=768)
        self.window.push_handlers(self.keys)

        self.addPlayer(player1)



    def addPlayer(self, player):
        """
        add a player to the player list
        """
        player.world = self
        self.player_objects.append(player)



    def gameUpdate(self, dt):
        """
        To be called every Tick
        """
        rabbyt.add_time(dt)
        default_system.update(dt)
        for k, k_pressed in self.keys.iteritems():
            if k_pressed and k in self.input:
                action = self.input[k][0]
                arg = self.input[k][1]
                self.p1.action(action, arg, dt)



    def selectLevel(self, name):
        """
        Maybe add more levels?
        """
        self.bgimage = resource.image('images/'+name+'.jpg')
        map = self.buildMap(name)
        for building in map:
            b = rabbyt.Sprite(None, building[0])
            b.xy = building[1]
            self.map_objects.append(b)



    def buildMap(self, name):
        """
        Need to DOC this
        """
         
        city1 = [
            ((-75, 24, 75, -24),(490, 373)), ((-24, 24, 24, -24),(590, 373)), ((-24, 24, 24, -24),(590, 325)),
            ((-24, 24, 24, -24),(838, 373)), ((-24, 24, 24, -24),(738, 275)), ((-24, 24, 24, -24),(488, 525)),
            ((-24, 24, 24, -24),(938, 525)), ((-24, 24, 24, -24),(988, 525)), ((-49, 49, 49, -49),(563, 549)),
            ((-49, 49, 49, -49),(763, 549)), ((-49, 49, 49, -49),(863, 549)), ((-49, 49, 49, -49),(763, 349))
        ]
        
        levels = {'city1':city1}
        return levels[name]

