import random
from engine import Entity
from globalvars import *

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
        self.controler = self._engine.get_controler()
        self.ground_map = ground_map
        self.state = S_EXPLORE(self)
        self.hp = 100
        self.age = 0
        self.death_age = random.randint(50,70)
        self.delete_age = self.death_age + 10
        self.alive = True
        self.hunger = 50
        
    def update(self):
        self.age+=AGING_RATE
        if self.age>self.death_age:
            self.alive=False
        if self.age>self.delete_age:
            self.controler.plan_remove_entity(self)
        if self.alive:
            new_state = self.state.update()
            if new_state is not None:
                self.state = new_state
        
