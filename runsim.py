from spritesheet import BinMap, SpriteSheet, Tiler4bit, Tiler8bit, SpriteStripAnim
from engine import *
import pygame
import numpy as np
import random

import entities
import graphics

from globalvars import *

from pygame.locals import FULLSCREEN,DOUBLEBUF

def gen_map():
    ground_map = BinMap(np.random.uniform(size=(MAP_SIZE,MAP_SIZE))<EARTH_DENSITY)
    ground_map.arr[:,0] = np.zeros((MAP_SIZE,))
    ground_map.arr[:,-1] = np.zeros((MAP_SIZE,))
    ground_map.arr[0] = np.zeros((MAP_SIZE,))
    ground_map.arr[-1,:] = np.zeros((MAP_SIZE,))

    return ground_map

def get_surface(ground_map):
    ground_map_surface = TILER.get_surface(ground_map)

    return ground_map_surface

class MyEventHandler(EventHandler):

    def on_lbutton_down(self,event):
        print("LBUTTON_DOWN")
        # import ipdb
        # ipdb.set_trace()
        position = (int(round(event.pos[0]))/self._engine.ratio_x,int(round(event.pos[1]))/self._engine.ratio_y)
        self._engine.get_controler().on_lbutton_down(position)

class MyMap(Map):
    
    def init(self):
        self.ground_map = gen_map()
        self.ground_map_surface = get_surface(self.ground_map)

    def get_map(self,rect):
        return self.ground_map
            
    def get_surface(self,rect):
        rect_arr = self.ground_map.arr[rect[0]:rect[0]+rect[2],rect[1]:rect[1]+rect[3]]
        temp_map = BinMap(rect_arr)
        return TILER.get_surface(temp_map)

class MyControler(Controler):

    def  init(self):

        self.ground_map = self.engine.get_map(None)
        possible_indices = self.ground_map.get_indices_ones()

        self.slimes = []
        self.grass_ = []
        self.roaches = []

        for _ in range(N_GRASS):
            start_x,start_y = random.choice(possible_indices)
            grass = self.new_entity("Grass",start_x,start_y)
            self.grass_.append(grass)

        for _ in range(N_ROACHES):
            start_x,start_y = random.choice(possible_indices)
            roach = self.new_entity("Roach",start_x,start_y,self.ground_map)
            self.roaches.append(roach)

        hive_x,hive_y = random.choice(possible_indices)
        self.hive = self.new_entity("Hive",hive_x,hive_y)


    def update(self):
        if self.engine.step in [x*15+1 for x in range(20)]:
            self.slimes.append(self.new_entity("Slime",self.hive.x,self.hive.y,self.ground_map))

    def on_lbutton_down(self,position):
        roach = self.new_entity("Roach",position[1],position[0],self.ground_map)
        self.roaches.append(roach)

if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    SS = SpriteSheet(GROUNDMAP_SPRITES)
    TILER = Tiler8bit(SS,N_PER_ROW,SIZE,index_dict=GROUNDMAP_TILES_DICT)

    engine = Engine(entities.classes,graphics.classes,MyControler,frames=30,ratio_x=SIZE,ratio_y=SIZE,map=MyMap,event_handler=MyEventHandler)

    clock = pygame.time.Clock()

    for step in engine:
        screen.fill(pygame.Color("black"))
      
        # screen.blit(engine.controler.ground_map_surface,(0,0))
        # screen.blit(get_surface(engine.controler.ground_map),(0,0))

        # for graphic in engine.graphic_entities:
        #     c_i = graphic.x*SIZE+SIZE_ANIM/2 - 1
        #     c_j = graphic.y*SIZE+SIZE_ANIM/2 - 1
        #     screen.blit(graphic.get_anim().next(),(c_j,c_i))

        surface = engine.get_surface((0,0,MAP_SIZE,MAP_SIZE))

        screen.blit(surface,(0,0))
        
        pygame.display.flip()
        clock.tick(60)
        
