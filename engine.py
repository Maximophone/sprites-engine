import random
from spritesheet import SpriteStripAnim
from collections import OrderedDict

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
    def __init__(self,engine,x,y):
        self._id = random.randint(0,1e9)
        self._engine = engine
        self._x = x
        self._y = y
        self.orientation = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self,value):
        self._engine.update_position(self,value,self._y)
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self,value):
        self._engine.update_position(self,self._x,value)
        self._y = value
        
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

    def get_neighbours(self):
        return self._engine.get_neighbours(self)
        
    def update(self):
        pass

    def __repr__(self):
        return "{},{}({})".format(self.x,self.y,self.orientation)

    def __hash__(self):
        return self._id

    def __eq__(self,other):
        return self._id == other._id
        
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
    def __init__(self,entity_classes_dict,graphic_classes_dict,controler_class,frames,lattice_size=6):
        self._counter = 0
        self.step = 0
        self.frames = frames
        self.entity_classes_dict = entity_classes_dict
        self.graphic_classes_dict = graphic_classes_dict
        self.entities = []
        self.graphic_entities = []

        self.lattice_size = lattice_size

        self.position_to_entities = {}
        self.lattice1 = {}
        self.lattice2 = {}

        self.controler = controler_class(self)
        
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

    def new_entity(self,clazz,x,y,*args,**kwargs):
        assert clazz in self.entity_classes_dict, "Entity class {} is unknown to engine".format(clazz)

        entity_constructor = self.entity_classes_dict[clazz]
        entity = entity_constructor(self,x,y)

        self.entities.append(entity)
        self.position_to_entities.setdefault((x,y),set())
        self.position_to_entities[(x,y)].add(entity)

        self.lattice1.setdefault((int(x)/self.lattice_size,int(y)/self.lattice_size),set())
        self.lattice1[(int(x)/self.lattice_size,int(y)/self.lattice_size)].add(entity)

        self.lattice2.setdefault((int(x)/self.lattice_size+self.lattice_size/2,int(y)/self.lattice_size+self.lattice_size/2),set())
        self.lattice2[(int(x)/self.lattice_size+self.lattice_size/2,int(y)/self.lattice_size+self.lattice_size/2)].add(entity)

        entity.init(*args,**kwargs)

        graphic_clazz = clazz + "_Graphic"
        if graphic_clazz in self.graphic_classes_dict:
            graphic_entity = self.graphic_classes_dict[graphic_clazz](entity)
            self.graphic_entities.append(graphic_entity)
        return entity

    def update_position(self,entity,x,y):

        self.position_to_entities[(entity.x,entity.y)].remove(entity)

        self.position_to_entities.setdefault((x,y),set())
        self.position_to_entities[(x,y)].add(entity)

        self.lattice1[(int(entity.x)/self.lattice_size,int(entity.y)/self.lattice_size)].remove(entity)

        self.lattice1.setdefault((int(x)/self.lattice_size,int(y)/self.lattice_size),set())
        self.lattice1[(int(x)/self.lattice_size,int(y)/self.lattice_size)].add(entity)

        self.lattice2[
            (
                int(entity.x)/self.lattice_size+self.lattice_size/2,
                int(entity.y)/self.lattice_size+self.lattice_size/2
                )
            ].remove(entity)

        self.lattice2.setdefault((int(x)/self.lattice_size+self.lattice_size/2,int(y)/self.lattice_size+self.lattice_size/2),set())
        self.lattice2[(int(x)/self.lattice_size+self.lattice_size/2,int(y)/self.lattice_size+self.lattice_size/2)].add(entity)

    def get_neighbours(self,entity):
         n1 = self.lattice1[(int(entity.x)/self.lattice_size,int(entity.y)/self.lattice_size)]
         n2 = self.lattice2[(int(entity.x)/self.lattice_size+self.lattice_size/2,int(entity.y)/self.lattice_size+self.lattice_size/2)]
         return n1.union(n2)

