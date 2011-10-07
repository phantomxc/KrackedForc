from tank import Tank
from mini import miniPlayer
from util import pickle


class Player(Tank):

    def __init__(self, name, turret, base, x=100, y=100):
        
        super(Player, self).__init__(name, turret, base, x, y)
        self.mini = miniPlayer(name, x, y)



    def render(self):

        self.mini.miniUpdate(x=self.x, y=self.y, trot=self.t.rot, brot=self.b.rot, health=self.health, score=self.score)
        super(Player, self).render()
        self.send('update')



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
        self.updateFromPlayer()

