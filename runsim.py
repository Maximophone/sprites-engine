from spritesheet import BinMap, SpriteSheet, Tiler4bit, Tiler8bit, SpriteStripAnim
from engine import *
import pygame
import numpy as np
import random

import entities
import graphics

from globalvars import *

def gen_map():
    ground_map = BinMap(np.random.uniform(size=(MAP_SIZE,MAP_SIZE))<EARTH_DENSITY)
    ground_map.arr[:,0] = np.zeros((MAP_SIZE,))
    ground_map.arr[:,-1] = np.zeros((MAP_SIZE,))
    ground_map.arr[0] = np.zeros((MAP_SIZE,))
    ground_map.arr[-1,:] = np.zeros((MAP_SIZE,))

    return ground_map

def get_surface(ground_map):
    ss = SpriteSheet(GROUNDMAP_SPRITES)
    ground_tiler = Tiler8bit(ss,N_PER_ROW,SIZE,index_dict=GROUNDMAP_TILES_DICT)
    ground_map_surface = ground_tiler.get_surface(ground_map)

    return ground_map_surface

class MyControler(Controler):

    def  init(self):

        self.ground_map = gen_map()
        self.ground_map_surface = get_surface(self.ground_map)

        possible_indices = self.ground_map.get_indices_ones()

        self.critters = []
        self.grass_ = []

        for _ in range(N_GRASS):
            start_x,start_y = random.choice(possible_indices)
            grass = self.new_entity("Grass",start_x,start_y)
            self.grass_.append(grass)

        hive_x,hive_y = random.choice(possible_indices)
        self.hive = self.new_entity("Hive",hive_x,hive_y)


    def update(self):
        if self.engine.step in [x*15+1 for x in range(20)]:
            self.critters.append(self.new_entity("Critter",self.hive.x,self.hive.y,self.ground_map))

if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    engine = Engine(entities.classes,graphics.classes,MyControler,frames=30)

    clock = pygame.time.Clock()

    for step in engine:
        screen.fill(pygame.Color("black"))
      
        screen.blit(engine.controler.ground_map_surface,(0,0))

        for graphic in engine.graphic_entities:
            c_i = graphic.x*SIZE+SIZE_ANIM/2 - 1
            c_j = graphic.y*SIZE+SIZE_ANIM/2 - 1
            screen.blit(graphic.get_anim().next(),(c_j,c_i))

        pygame.display.flip()
        clock.tick(60)
        