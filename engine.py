import random
from spritesheet import SpriteStripAnim

class Entity(object):
    clazz = 'generic'
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.orientation = 0
        
    def move(self,dir):
        assert dir in (0,1,2,3,4), "Invalid direction"
        if dir==0:
            self.x+=1
        elif dir==1:
            self.y-=1
        elif dir==2:
            self.x-=1
        elif dir==3:
            self.y+=1
        else:
            return
        self.orientation = dir
        
    def update(self):
        pass

    def __repr__(self):
        return "{},{}({})".format(self.x,self.y,self.orientation)
        
class GraphicEntity(object):
    def __init__(self,x,y,entity):
        self.x = x
        self.y = y
        self.entity = entity

    def get_anim(self):
        pass
        
    def update(self):
        x = self.entity.x
        y = self.entity.y
        self.x += abs(x-self.x)/(x-self.x)*0.03 if self.x!=x else 0
        self.y += abs(y-self.y)/(y-self.y)*0.03 if self.y!=y else 0


class Engine(object):
    def __init__(self,entities, graphic_store, frames):
        self._counter = 0
        self.frames = frames
        self.entities = entities
        self.graphic_entities = []
        for entity in self.entities:
            graphic_entity = graphic_store[entity.clazz](entity.x,entity.y,entity)
            self.graphic_entities.append(graphic_entity)
        
    def __iter__(self):
        return self
        
    def next(self):
        self._counter+=1
        for graphic_entity in self.graphic_entities:
            graphic_entity.update()
        if self._counter%self.frames==0:
            for entity in self.entities:
                entity.update()
        return self._counter
