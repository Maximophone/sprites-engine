from engine import Entity

class Hive(Entity):

    def __init__(self,x,y):
        super(Hive,self).__init__(x,y)
        self.food = 0

    def update(self):
        pass