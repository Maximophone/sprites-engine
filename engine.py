import random
from spritesheet import SpriteStripAnim

class Controler(object):
    def __init__(self,engine):
        self.engine = engine
        self.init()

    def init(self):
        pass

    def update(self):
        pass

    def new_entity(self,*args,**kwargs):
        return self.engine.new_entity(*args,**kwargs)

    # def update(self):
    #     for entity in self.entities:
    #         entity.update()

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
    def __init__(self,entity):
        self.entity = entity
        self.x = entity.x
        self.y = entity.y

    def get_anim(self):
        pass
        
    def update(self):
        x = self.entity.x
        y = self.entity.y
        self.x += abs(x-self.x)/(x-self.x)*0.03 if self.x!=x else 0
        self.y += abs(y-self.y)/(y-self.y)*0.03 if self.y!=y else 0


class Engine(object):
    """
    The engine is aware of entity classes and graphics. Provides methods for creation and deletion.

    """
    def __init__(self,entities_dict,graphics_dict,controler_class,frames):
        self._counter = 0
        self.step = 0
        self.frames = frames
        self.entities_dict = entities_dict
        self.graphics_dict = graphics_dict
        self.entities = []
        self.graphic_entities = []
        self.controler = controler_class(self)
        # for entity in self.entities:
        #     graphic_entity = graphics_namespace[entity.clazz](entity.x,entity.y,entity)
        #     self.graphic_entities.append(graphic_entity)
        
    def __iter__(self):
        return self
        
    def next(self):
        self._counter+=1
        for graphic_entity in self.graphic_entities:
            graphic_entity.update()
        if self._counter%self.frames==0:
            self.step+=1
            self.controler.update()
            for entity in self.entities:
                entity.update()
        return self._counter

    def new_entity(self,clazz,*args,**kwargs):
        assert clazz in self.entities_dict, "Entity class {} is unknown to engine".format(clazz)
        entity_constructor = self.entities_dict[clazz]
        entity = entity_constructor(*args,**kwargs)
        self.entities.append(entity)
        graphic_clazz = clazz + "_Graphic"
        if graphic_clazz in self.graphics_dict:
            graphic_entity = self.graphics_dict[graphic_clazz](entity)
            self.graphic_entities.append(graphic_entity)
        return entity