import math
import pygame
from pygame.rect import Rect
import random
from spritesheet import SpriteStripAnim
from collections import OrderedDict
from event_handler import EventHandler

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

def _get_chunk_ids(rect,chunk_size):
    range_x = range(
        int(math.floor(rect[0]))/chunk_size,
        int(math.ceil(rect[0]+rect[2]))/chunk_size+1)
    range_y = range(
        int(math.floor(rect[1]))/chunk_size,
        int(math.ceil(rect[1]+rect[3]))/chunk_size+1)

    return [(x,y) for x in range_x for y in range_y]
    
def _get_chunk_rect(chunk_id,chunk_size):
    return (chunk_id[0]*chunk_size,chunk_id[1]*chunk_size,chunk_size,chunk_size)

def _aggregate_chunks_dict(chunks_dict,chunk_size,ratio_x,ratio_y,rect):
    ix = [i[0] for i in chunks_dict.keys()]
    iy = [i[1] for i in chunks_dict.keys()]

    size_x = (max(ix)-min(ix)+1)*chunk_size
    size_y = (max(iy)-min(iy)+1)*chunk_size
    
    surface = pygame.Surface(
        (int(rect[2]*ratio_x),int(rect[3]*ratio_y)),
        pygame.SRCALPHA,
        32).convert()
    for chunk_id,chunk in chunks_dict.items():
        surface.blit(
            chunk,
            (int(chunk_id[0]*chunk_size*ratio_x - rect[0]*ratio_x),
             int(chunk_id[1]*chunk_size*ratio_y - rect[1]*ratio_y))
        )
        
    return surface

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
    def __init__(self,entity,size):
        self.entity = entity
        self.x = entity.x
        self.y = entity.y
        self.size = size

    def get_anim(self):
        pass
        
    def update(self,dt):
        x = self.entity.x
        y = self.entity.y
        if self.x<x-dt or self.x>x+dt:
            self.x += abs(x-self.x)/(x-self.x)*dt
        else:
            self.x = x
        if self.y<y-dt or self.y>y+dt:
            self.y += abs(y-self.y)/(y-self.y)*dt
        else:
            self.y = y

class Camera(object):

    def __init__(self,engine,rect):
        self._engine = engine
        self._rect = rect

    @property
    def rect(self):
        return self._rect
    
    def move_abs(self,pos):
        self._rect = (pos[0],pos[1],self._rect[2],self._rect[3])

    def move_rel(self,dpos):
        self._rect = (
            self._rect[0]+dpos[0],
            self._rect[1]+dpos[1],
            self._rect[2],
            self._rect[3])

    def zoom(self,rzoom):
        rect_center = (self._rect[0]+self._rect[2]/2.,self._rect[1]+self._rect[3]/2.)
        new_w = rzoom*self._rect[2]
        new_h = rzoom*self._rect[3]
        self._rect = (
            rect_center[0]-new_w/2.,
            rect_center[1]-new_h/2.,
            new_w,
            new_h)
        
class Map(object):
    def __init__(self,engine,chunk_size=32):
        self.chunk_size = chunk_size
        self._chunks_cache = {}
        self._engine = engine
        self.init()

    def init(self):
        pass

    def get_surface(self,rect):
        raise NotImplemented
    
    def _get_surface(self,rect):
        chunk_ids = _get_chunk_ids(rect,self.chunk_size)
        surface_dict = {}
        for chunk_id in chunk_ids:
            if chunk_id not in self._chunks_cache:
                print("Generating chunk {}".format(chunk_id))
                chunk_rect = _get_chunk_rect(chunk_id,self.chunk_size)
                print("Chunk rect: {}".format(chunk_rect))
                chunk = self.get_surface(chunk_rect)
                self._chunks_cache[chunk_id] = chunk
            surface_dict[chunk_id] = self._chunks_cache[chunk_id]
        surface = _aggregate_chunks_dict(surface_dict,self.chunk_size,self._engine.ratio_x,self._engine.ratio_y,rect)
        return surface
        
class Engine(object):
    """
    The engine is aware of entity classes and graphics. Provides methods for creation and deletion.

    """
    def __init__(self,entity_classes_dict,graphic_classes_dict,controler_class,frames,ratio_x,ratio_y,map,event_handler,origin_rect,screen_size,lattice_size=6):
        """
        Args:
        - entity_classes_dict: Dictionary of all the entity classes available to the engine
        - graphic_classes_dict: Dictionary of all the graphic classes available to the engine
        - controler_class: The controler class to be instantiated by the engine
        - frames: Integer, how many frames per game step
        - ratio_x, ratio_y: integers, how many pixels per game unit (in both directions).
        - map: Any class that implements the Map class
        - event_handler: Any class that implements the EventHandler class
        - origin_rect: Initial rectangle for game camera
        - screen_size: size of the screen (width,height)

        Kwargs:
        - lattice_size: Size of the lattices used for computing emtity neighbours, in game unit
        """
        self.ratio_x = ratio_x
        self.ratio_y = ratio_y
        self.screen_size = screen_size
        self._counter = 0
        self.step = 0
        self.frames = frames
        self.entity_classes_dict = entity_classes_dict
        self.graphic_classes_dict = graphic_classes_dict
        self.entities = []
        self.graphic_entities = []
        self.map_ = map(self)
        self.event_handler = event_handler(self)
        self.camera = Camera(self,origin_rect)
        
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
        dt = 1./self.frames
        self._counter+=1

        for event in pygame.event.get():
#            print(event)
            self.event_handler.on_event(event)

        self.event_handler.key_pressed(pygame.key.get_pressed())

        self.event_handler.mouse_pressed(pygame.mouse.get_pressed(),pygame.mouse.get_pos())
        
        for graphic_entity in self.graphic_entities:
            graphic_entity.update(dt)
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

    def get_surface(self,rect=None):
        if rect is None:
            rect = self.camera.rect

        surface = self._get_surface(rect)
        scaled_surface = pygame.transform.scale(surface,self.screen_size)

        return scaled_surface
    
    def _get_surface(self,rect):
        map_surface = self.map_._get_surface(rect)
        for graphic in self._get_graphic_entities_in_rect((rect[0]-1,rect[1]-1,rect[2]+2,rect[3]+2)):
            x = self.ratio_x*(graphic.x-rect[0]) + self.ratio_x/2. - graphic.size[0]/2.
            y = self.ratio_y*(graphic.y-rect[1]) + self.ratio_y/2. - graphic.size[1]/2.
            map_surface.blit(graphic.get_anim().next(),(x,y))
        return map_surface

    def get_map(self,rect):
        return self.map_.get_map(rect)

    def get_controler(self):
        return self.controler
    
    def screen_to_game_coords(self,screen_pos):
        game_pos = (
            self.camera._rect[0] + float(screen_pos[1])/self.screen_size[0]*self.camera._rect[2],
            self.camera._rect[1] + float(screen_pos[0])/self.screen_size[1]*self.camera._rect[3]
            )
        return game_pos


