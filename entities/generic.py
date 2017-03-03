from engine import Entity
from globalvars import *

class GenericEntity(Entity):
    def init(self,ground_map):
        self.controler = self._engine.get_controler()
        self.ground_map = ground_map

    def get_dirs(self):
        _,dirs = self.ground_map.get_val_and_direct_neighbours(self.x,self.y)
        possible_dirs = [i for i,x in enumerate(dirs) if x==1]
        if not possible_dirs:
            possible_dirs = [4]
        return possible_dirs
        
class GenericAging(GenericEntity):
    def init(self,ground_map,death_age,delete_age):
        super(GenericAging,self).init(ground_map)
        self.age=0
        self.death_age = death_age
        self.delete_age = delete_age
        self.alive = True

    def resolve_age(self):
        self.age+=AGING_RATE
        if self.age>self.death_age:
            self.alive = False
        if self.age>self.delete_age:
            self.controler.plan_remove_entity(self)
        
        
