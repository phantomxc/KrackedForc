class miniPlayer(object):
    """
    This is really only for pickling an object to the server
    """

    def __init__(self, name, keys):

        self.name = name
        self.health = 100
        self.score = 0
        self.keys = keys

    def miniUpdate(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

