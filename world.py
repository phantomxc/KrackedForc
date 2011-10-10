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

        self.map_objects = []
        self.player_objects = []
        self.players = {}
        self.mini_objects = []
        self.window = Window(width=1300, height=768)
        self.stop_update = False



    def addPlayer(self, player, main=False):
        """
        add a player to the player list
        """
        if main:
            self.p1 = player
            self.p1.keys = key.KeyStateHandler()
            self.window.push_handlers(self.p1.keys)

        player.world = self

        self.players[player.name] = player
        self.mini_objects.append(player.mini)
        player.send('new')

    def addPlayerFromMini(self, mini):
        """
        what the title says
        """
        p = Player(mini.name, 'tanktop', 'tankbot')
        self.addPlayer(p)


    def gameUpdate(self, dt):
        """
        To be called every Tick
        """
        self.recvServer()
        rabbyt.add_time(dt)
        default_system.update(dt)
        

        for name, po in self.players.items():
            delete_keys=[]
            for k, k_pressed in po.keys.iteritems():
                if k_pressed and k in po.input:
                    action = po.input[k][0]
                    arg = po.input[k][1]
                    po.action(action, arg, dt)
                    if po == self.p1:
                        self.stop_update = True
                        self.p1.send('update')
                else:
                    delete_keys.append(k)
                    if self.stop_update:
                        self.stop_update = False
                        self.p1.send('update_stop')

            for k in delete_keys:
                del po.keys[k]
            
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
        print "Connected" 
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

            self.updatePlayers(foreign)


    def updatePlayers(self, foreign):

        for name, mini in foreign.items():
            p = self.getPlayer(mini)
            p.updateFromMini(mini)



    def getPlayer(self, mini):
        try:
            return self.players[mini.name]
        except:
            self.addPlayerFromMini(mini)
            return self.players[mini.name]
        
            








