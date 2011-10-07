class miniPlayer(object):
    """
    This is really only for pickling an object to the server
    """

    def __init__(self, name, x, y):

        self.name = name
        self.x = y
        self.y = x
        self.trot = 0
        self.brot = 0
        self.health = 0
        self.score = 0

    def miniUpdate(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

