import os
from spritesheet import BinMap, SpriteSheet, Tiler4bit, Tiler8bit, SpriteStripAnim
from engine import *
import pygame
import numpy as np
import random

import entities
import graphics

from globalvars import *

from pygame.locals import FULLSCREEN,DOUBLEBUF

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1200,0)

def gen_map(size_x,size_y):
    ground_map = BinMap(np.random.uniform(size=(size_x,size_y))<EARTH_DENSITY)
    ground_map.arr[:,0] = np.zeros((size_x,))
    ground_map.arr[:,-1] = np.zeros((size_x,))
    ground_map.arr[0] = np.zeros((size_y,))
    ground_map.arr[-1,:] = np.zeros((size_y,))

    return ground_map

def get_surface(ground_map):
    ground_map_surface = TILER.get_surface(ground_map)

    return ground_map_surface

class MyEventHandler(EventHandler):

    def on_lbutton_down(self,event):
        position = self.engine.screen_to_game_coords(event.pos)
        self.engine.get_controler().on_lbutton_down((int(position[0]),int(position[1])))

    def on_mouse_wheel_up(self,event):
        self.engine.camera.zoom(1.25)

    def on_mouse_wheel_down(self,event):
        self.engine.camera.zoom(0.8)
        
    def key_pressed(self,keys):
        if keys[pygame.K_DOWN]:
            self.engine.camera.move_rel(dpos=(0,0.2))
        if keys[pygame.K_UP]:
            self.engine.camera.move_rel(dpos=(0,-0.2))
        if keys[pygame.K_LEFT]:
            self.engine.camera.move_rel(dpos=(-0.2,0))
        if keys[pygame.K_RIGHT]:
            self.engine.camera.move_rel(dpos=(0.2,0))

class MyMap(Map):
    def init(self):
        self.ground_map = gen_map(MAP_SIZE,MAP_SIZE)

    def get_map(self,rect):
        return self.ground_map
            
    def get_surface(self,rect):
        rect_arr = np.take(
            np.take(
                self.ground_map.arr,
                range(rect[1],rect[1]+rect[3]),
                axis=1,
                mode='clip'),
            range(rect[0],rect[0]+rect[2]),
            axis=0,
            mode='clip')
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

    engine = Engine(
        entities.classes,
        graphics.classes,
        MyControler,
        frames=30,
        ratio_x=SIZE,
        ratio_y=SIZE,
        map=MyMap,
        event_handler=MyEventHandler,
        origin_rect=ORIGIN_CAMERA,
        screen_size=(WINDOW_WIDTH,WINDOW_HEIGHT))

    clock = pygame.time.Clock()

    for step in engine:
        screen.fill(pygame.Color("black"))
      
        surface = engine.get_surface()
        screen.blit(surface,(0,0))
        
        pygame.display.flip()
        clock.tick(60)
        
        
