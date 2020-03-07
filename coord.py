class coord:
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x ==  other.x and self.y == other.y:
            return True
        return False
