import rabbyt
from lepton import default_system
from pyglet.window import key, Window
from pyglet import resource, text
import zmq 
import sys 
import util
from player import Player


class World(object):

    def __init__(self):

        self.keys = key.KeyStateHandler()
        self.map_objects = []
        self.player_objects = []
        self.mini_objects = []
        self.input = {
            key.W : ('move', 'up'),
            key.A : ('rotate', 'left'),
            key.S : ('move', 'down'),
            key.D : ('rotate', 'right'),
            key.LEFT : ('turret', 'left'),
            key.RIGHT: ('turret', 'right'),
            key.SPACE: ('fire', ''),
            key._1: ('change', 0),
            key._2: ('change', 1),
            key._3: ('change', 2),
            key._4: ('change', 3)
        }

        self.window = Window(width=1300, height=768)
        self.window.push_handlers(self.keys)



    def addPlayer(self, player, main=False):
        """
        add a player to the player list
        """
        if main:
            self.p1 = player
        player.world = self
        self.player_objects.append(player)
        self.mini_objects.append(player.mini)
        player.send('new')

    def addPlayerFromMini(self, mini):
        """
        what the title says
        """
        p = Player(mini.name, 'tanktop', 'tankbot', mini.x, mini.y)
        self.addPlayer(p)


    def gameUpdate(self, dt):
        """
        To be called every Tick
        """
        self.recvServer()
        rabbyt.add_time(dt)
        default_system.update(dt)

        for k, k_pressed in self.keys.iteritems():
            if k_pressed and k in self.input:
                action = self.input[k][0]
                arg = self.input[k][1]
                self.p1.action(action, arg, dt)


    def displayScore(self):
        """
        Render the score for the players
        """
        x_start = 1200
        y_start = 750
        labels = []
        for p in self.mini_objects:
            y_start -= 25
            score = '%s : %s' % (p.name, p.score)
            label = text.Label(score,
                font_name='Times New Roman',
                font_size=12,
                x=x_start, y=y_start,
                )
            labels.append(label)
        for l in labels:
            l.draw()



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

    
    def connectServer(self):
        context = zmq.Context()

        # Socket to receive broadcasts from server
        self.sub_socket = context.socket(zmq.SUB)
        self.sub_socket.connect("tcp://localhost:5556")
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, "all")
        print "Connecting to server ...",
        sys.stdout.flush()
        self.sub_socket.recv()  # Will hang forever if no server.
        
        self.push_socket = context.socket(zmq.PUSH) 
        self.push_socket.connect("tcp://localhost:5555") 



    def recvServer(self):
        try:
            msg = self.sub_socket.recv(flags=zmq.core.NOBLOCK)
        except zmq.core.error.ZMQError:
            pass
        else:
            sep = msg.find(':')
            to = msg[0:sep]
            foreign = util.unpickle(msg[sep+1:])

            for n, obj in foreign.items():
                if n == self.p1.mini.name:
                    del foreign[n]

            self.moveOthers(foreign)


    def moveOthers(self, foreign):

        for name, mini in foreign.items():
            p = self.getPlayer(mini)
            p.updateFromMini(mini)



    def getPlayer(self, mini):
        player_names = [p.name for p in self.player_objects]
        if mini.name not in player_names:
            self.addPlayerFromMini(mini)
        for player in self.player_objects:
            if player.name == mini.name:
                return player
        
            








