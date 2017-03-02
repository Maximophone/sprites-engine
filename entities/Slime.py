import random
from engine import Entity

class State(object):
    def __init__(self,entity):
        self.entity = entity
        
    def get_dirs(self):
        _,dirs = self.entity.ground_map.get_val_and_direct_neighbours(self.entity.x,self.entity.y)
        possible_dirs = [i for i,x in enumerate(dirs) if x==1]
        if not possible_dirs:
            possible_dirs = [4]
        return possible_dirs
        
class S_EXPLORE(State):
    def update(self):
        possible_dirs = self.get_dirs()
        d = random.choice(possible_dirs)        
        self.entity.move(d)
        
class S_COMEBACK(State):
    pass
    

class Slime(Entity):
    clazz = 'slime'

    def init(self,ground_map):
        self.ground_map = ground_map
        self.state = S_EXPLORE(self)
        
    def update(self):
        new_state = self.state.update()
        if new_state is not None:
            self.state = new_state
