import random
from engine import Entity
from globalvars import *

class Grass(Entity):
    clazz = 'grass'

    def init(self):
        self.growth = 0
    
    def update(self):
        if random.random()<GRASS_GROWTH_RATE:
            self.growth = min(self.growth+1,3)