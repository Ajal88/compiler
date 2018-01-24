PB = []  # program block
ss = []  # semantic stack


class NameSpace:
    def __init__(self, parent):
        self.names = []
        self.parent = parent

