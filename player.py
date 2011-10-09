from tank import Tank
from mini import miniPlayer
from util import pickle
from pyglet.window import key


class Player(Tank):

    def __init__(self, name, turret, base, x=100, y=100):
        self.keys = {}        
        super(Player, self).__init__(name, turret, base, x, y)
        self.mini = miniPlayer(name, self.keys)

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




    def render(self):

        self.mini.miniUpdate(health=self.health, score=self.score, keys=self.keys)
        super(Player, self).render()


    def send(self, command, **kwargs):
        """
        Send information to the server.

        command - A command string the server will accept.

        Depending upon the command, you will likely need additional named arguments.
        All named arguments will get passed through to the server.
        """
        cmd_dict = {
            'cmd':command,
            'player':pickle(self.mini)
        }
        cmd_dict.update(kwargs)
        if self.world.p1 == self:
            self.world.push_socket.send_pyobj(cmd_dict)

    
    def updateFromMini(self, mini):
        for a, value in mini.__dict__.iteritems():
            setattr(self, a, value)

