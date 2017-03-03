import random
from engine import Entity
from globalvars import *
from generic import GenericAging

class State(object):
    def __init__(self,entity):
        self.entity = entity
        
class S_EXPLORE(State):
    def update(self):
        possible_dirs = self.entity.get_dirs()
        d = random.choice(possible_dirs)        
        self.entity.move(d)
        
class S_COMEBACK(State):
    pass
    

class Slime(GenericAging):
    clazz = 'slime'

    def init(self,ground_map):
        death_age = random.randint(50,70)
        delete_age = death_age + 10
        self.state = S_EXPLORE(self)
        self.hp = 100
        self.hunger = 50
        super(Slime,self).init(ground_map,death_age,delete_age)
        
    def update(self):
        self.resolve_age()
        if self.alive:
            new_state = self.state.update()
            if new_state is not None:
                self.state = new_state
        
