from spritesheet import BinMap, SpriteSheet, Tiler4bit, Tiler8bit, SpriteStripAnim
from engine import *
import pygame
import numpy as np
import random

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1200

N_PER_ROW = 8
SIZE = 32
SIZE_ANIM = 16
MAP_SIZE = 30

EARTH_DENSITY = 0.8

ENTITIES_SPRITES = "critters.png"

GRASS_GROWTH_RATE = 0.01
N_CRITTERS = 16
N_GRASS = 50

class Critter(Entity):
    clazz = 'critter'

    def __init__(self,x,y,ground_map):
        super(Critter,self).__init__(x,y)
        self.ground_map = ground_map

    def update(self):
        _,dirs = self.ground_map.get_val_and_direct_neighbours(self.x,self.y)
        possible_dirs = [i for i,x in enumerate(dirs) if x==1]
        if not possible_dirs:
            possible_dirs = [4]
        d = random.choice(possible_dirs)
        self.move(d)

class Grass(Entity):
    clazz = 'grass'

    def __init__(self,x,y):
        super(Grass,self).__init__(x,y)
        self.growth = 0
    
    def update(self):
        if random.random()<GRASS_GROWTH_RATE:
            self.growth = min(self.growth+1,3)

class Grass_Graphic(GraphicEntity):
    def __init__(self,x,y,entity):
        super(Grass_Graphic,self).__init__(x,y,entity)
        self.anims = {
            0:SpriteStripAnim(ENTITIES_SPRITES,(1*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6),
            1:SpriteStripAnim(ENTITIES_SPRITES,(2*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6),
            2:SpriteStripAnim(ENTITIES_SPRITES,(3*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6),
            3:SpriteStripAnim(ENTITIES_SPRITES,(4*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6)
            }

    def get_anim(self):
        return self.anims[self.entity.growth]

class Critter_Graphic(GraphicEntity):
    def __init__(self,x,y,entity):
        super(Critter_Graphic,self).__init__(x,y,entity)
        self.anims = {
                0:SpriteStripAnim(ENTITIES_SPRITES,(5*SIZE_ANIM,3*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6),
                1:SpriteStripAnim(ENTITIES_SPRITES,(5*SIZE_ANIM,4*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6),
                2:SpriteStripAnim(ENTITIES_SPRITES,(5*SIZE_ANIM,5*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6),
                3:SpriteStripAnim(ENTITIES_SPRITES,(5*SIZE_ANIM,6*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6),
                }

    def get_anim(self):
        return self.anims[self.entity.orientation]


graphic_store = {
    'grass':Grass_Graphic,
    'critter':Critter_Graphic
}


if __name__ == '__main__':

    ground_map = BinMap(np.random.uniform(size=(MAP_SIZE,MAP_SIZE))<EARTH_DENSITY)
    ground_map.arr[:,0] = np.zeros((MAP_SIZE,))
    ground_map.arr[:,-1] = np.zeros((MAP_SIZE,))
    ground_map.arr[0] = np.zeros((MAP_SIZE,))
    ground_map.arr[-1,:] = np.zeros((MAP_SIZE,))

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    critters = []
    grass_ = []

    possible_indices = ground_map.get_indices_ones()

    for _ in range(N_CRITTERS):
        start_x,start_y = random.choice(possible_indices)
        critter = Critter(start_x,start_y,ground_map)
        critters.append(critter)

    for _ in range(N_GRASS):
        start_x,start_y = random.choice(possible_indices)
        grass = Grass(start_x,start_y)
        grass_.append(grass)

    engine = Engine(grass_+critters,graphic_store,frames=30)

    clock = pygame.time.Clock()

    ss = SpriteSheet('./GroundMap.png')

    index_dict = { -1:47, 2:1, 8:2, 10:3, 11:4, 16:5, 18:6, 22:7, 24:8, 26:9, 27:10, 30:11, 31:12, 64:13, 66:14, 72:15, 74:16, 75:17, 80:18, 82:19, 86:20, 88:21, 90:22, 91:23, 94:24, 95:25, 104:26, 106:27, 107:28, 120:29, 122:30, 123:31, 126:32, 127:33, 208:34, 210:35, 214:36, 216:37, 218:38, 219:39, 222:40, 223:41, 248:42, 250:43, 251:44, 254:45, 255:0, 0:46 }

    ground_tiler = Tiler8bit(ss,N_PER_ROW,SIZE,index_dict=index_dict)

    ground_map_surface = ground_tiler.get_surface(ground_map)

    for step in engine:
        screen.fill(pygame.Color("black"))
      
        screen.blit(ground_map_surface,(0,0))

        for graphic in engine.graphic_entities:
            c_i = graphic.x*SIZE+SIZE_ANIM/2 - 1
            c_j = graphic.y*SIZE+SIZE_ANIM/2 - 1
            screen.blit(graphic.get_anim().next(),(c_j,c_i))

        pygame.display.flip()
        clock.tick(60)
        