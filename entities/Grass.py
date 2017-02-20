import random
from engine import Entity
from globalvars import *

class Grass(Entity):
    clazz = 'grass'

    def __init__(self,x,y):
        super(Grass,self).__init__(x,y)
        self.growth = 0
    
    def update(self):
        if random.random()<GRASS_GROWTH_RATE:
            self.growth = min(self.growth+1,3)