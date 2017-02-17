import random
from spritesheet import SpriteStripAnim

class Entity(object):
    clazz = 'generic'
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.orientation = 0
        
    def move(self,dir):
        assert dir in (0,1,2,3), "Invalid direction"
        if dir==0:
            self.x+=1
        elif dir==1:
            self.y-=1
        elif dir==2:
            self.x-=1
        else:
            self.y+=1
        self.orientation = dir
        
    def update(self):
        pass

    def __repr__(self):
        return "{},{}({})".format(self.x,self.y,self.orientation)
        
class GraphicEntity(object):
    def __init__(self,x,y,anim):
        self.x = x
        self.y = y
        self.anim = anim
        
    def update(self,x,y):
        self.x += abs(x-self.x)/(x-self.x)*0.03 if self.x!=x else 0
        self.y += abs(y-self.y)/(y-self.y)*0.03 if self.y!=y else 0
        

class Engine(object):
    def __init__(self,entities, anim_store):
        self.entities = entities
        self.graphic_entities = []
        for entity in self.entities:
            graphic_entity = GraphicEntity(entity.x,entity.y,anim_store.get_anim(entity.clazz))
            self.graphic_entities.append(graphic_entity)
        
    def __iter__(self):
        return self
        
    def next(self):
        for entity in self.entities:
            entity.update()
