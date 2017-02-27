import random
from spritesheet import SpriteStripAnim
from collections import OrderedDict

class Dirs:
    SOUTH = 0
    WEST = 1
    NORTH = 2
    EAST = 3
    STILL = 4

class Lattice(object):
    def __init__(self,length,offset_x,offset_y):
        self._l = int(length)
        self._ox = int(offset_x)
        self._oy = int(offset_y)
        self._d = {}

    def _get_index(self,x,y):
        return int(x)/self._l+self._ox, int(y)/self._l+self._oy

    def get(self,x,y):
        return self._d.setdefault(self._get_index(x,y),set())

    def add(self,x,y,value):
        values = self._d.setdefault(self._get_index(x,y),set())
        values.add(value)

    def remove(self,x,y,value):
        values = self._d.setdefault(self._get_index(x,y),set())
        values.remove(value)

class MultiLattice(object):
    def __init__(self,*lattices):
        self.lattices = lattices

    def get(self,x,y):
        return set.union(*[l.get(x,y) for l in self.lattices])

    def add(self,x,y,value):
        for l in self.lattices:
            l.add(x,y,value)

    def remove(self,x,y,value):
        for l in self.lattices:
            l.remove(x,y,value)


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
        if dir==Dirs.SOUTH:
            self.x+=1
        elif dir==Dirs.WEST:
            self.y-=1
        elif dir==Dirs.NORTH:
            self.x-=1
        elif dir==Dirs.EAST:
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

class Camera(object):

    def __init__(self,engine,rect):
        self._engine = engine
        self.rect = rect

    def get_image(self):
        pass

class Map(object):
    def __init__(self):
        pass

def _is_point_in_rect(point,rect):
    if point[0]<rect[0]:
        return False
    if point[0]>rect[0]+rect[2]:
        return False
    if point[1]<rect[1]:
        return False
    if point[1]>rect[1]+rect[3]:
        return False
    return True

class Engine(object):
    """
    The engine is aware of entity classes and graphics. Provides methods for creation and deletion.

    """
    def __init__(self,entity_classes_dict,graphic_classes_dict,controler_class,frames,ratio_x,ratio_y,lattice_size=6):
        """
        Args:
        - entity_classes_dict: Dictionary of all the entity classes available to the engine
        - graphic_classes_dict: Dictionary of all the graphic classes available to the engine
        - controler_class: The controler class to be instantiated by the engine
        - frames: Integer, how many frames per game step
        - ratio_x, ratio_y: integers, how many pixels per game unit (in both directions).

        Kwargs:
        - lattice_size: Size of the lattices used for computing emtity neighbours, in game unit
        """
        self.ratio_x = ratio_x
        self.ratio_y = ratio_y
        self._counter = 0
        self.step = 0
        self.frames = frames
        self.entity_classes_dict = entity_classes_dict
        self.graphic_classes_dict = graphic_classes_dict
        self.entities = []
        self.graphic_entities = []

        self.position_to_entities = {}
        lattice1 = Lattice(lattice_size,0,0)
        lattice2 = Lattice(lattice_size,0,lattice_size/2)
        lattice3 = Lattice(lattice_size,lattice_size/2,0)
        lattice4 = Lattice(lattice_size,lattice_size/2,lattice_size/2)

        self.multi_lattice = MultiLattice(lattice1,lattice2,lattice3,lattice4)

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

        self.multi_lattice.add(x,y,entity)

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

        self.multi_lattice.remove(entity.x,entity.y,entity)
        self.multi_lattice.add(x,y,entity)


    def get_neighbours(self,entity):
        return self.multi_lattice.get(entity.x,entity.y)

    def _get_graphic_entities_in_rect(self,rect):
        return [graphic for graphic in self.graphic_entities if _is_point_in_rect((graphic.x,graphic.y),rect)]

    def get_surface(self,rect):
        #Problem: we need to solve the duality coordinates in game/coordinates on screen
        map_surface = self.map.get_surface(rect)
        for graphic in self._get_graphic_entities_in_rect(rect):
            screen.blit(graphic.get_anim().next(),(c_j,c_i))
            
