import random
from engine import Entity

class Critter(Entity):
    clazz = 'critter'

    def __init__(self,x,y,ground_map):
        super(Critter,self).__init__(x,y)
        self.ground_map = ground_map

    def update(self):
        _,dirs = self.ground_map.get_val_and_direct_neighbours(self.x,self.y)
        possible_dirs = [i for i,x in enumerate(dirs) if x==1]
        if not possible_dirs:
            possible_dirs = [4]
        d = random.choice(possible_dirs)
        self.move(d)