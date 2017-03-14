import os
from spritesheet import BinMap, SpriteSheet, Tiler4bit, Tiler8bit, SpriteStripAnim
from engine import *
import pygame
import numpy as np
import random
from marching_squares import MSMap,MarchingSquaresTiler

import entities
import graphics

from globalvars import *

from pygame.locals import FULLSCREEN,DOUBLEBUF

from scipy.ndimage.filters import gaussian_filter

from mapgen import gen_map_arr

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1200,0)


def gen_map(size_x,size_y):
    arr = gen_map_arr(size_x,size_y,factor=MAP_INTERPOLATION_FACTOR)
    ground_map = MSMap(arr)

    return ground_map

def get_surface(ground_map):
    ground_map_surface = TILER.get_surface(ground_map.corners)

    return ground_map_surface

class MyEventHandler(EventHandler):

    def on_lbutton_down(self,event):
        position = self.engine.screen_to_game_coords(event.pos)
        self.engine.get_controler().on_lbutton_down((int(position[0]),int(position[1])))

    def on_mouse_wheel_up(self,event):
        if self.engine.camera.rect[2]<8:
            print "min zoom"
            return
        self.engine.camera.zoom(0.8)

    def on_mouse_wheel_down(self,event):
        if self.engine.camera.rect[2]>64:
            print "max zoom"
            return
        self.engine.camera.zoom(1.25)
        
    def key_pressed(self,keys):
        relative_move = self.engine.camera.rect[2]/60.
        if keys[pygame.K_DOWN]:
            self.engine.camera.move_rel(dpos=(0,relative_move))
        if keys[pygame.K_UP]:
            self.engine.camera.move_rel(dpos=(0,-relative_move))
        if keys[pygame.K_LEFT]:
            self.engine.camera.move_rel(dpos=(-relative_move,0))
        if keys[pygame.K_RIGHT]:
            self.engine.camera.move_rel(dpos=(relative_move,0))

class MyMap(Map):
    def init(self):
        self.ground_map = gen_map(MAP_SIZE,MAP_SIZE)

    def get_map(self,rect):
        return self.ground_map
            
    def get_surface(self,rect):
        rect_arr = np.take(
            np.take(
                self.ground_map.corners,
                range(rect[1],rect[1]+rect[3]+1),
                axis=0,
                mode='clip'),
            range(rect[0],rect[0]+rect[2]+1),
            axis=1,
            mode='clip')
        return TILER.get_surface(rect_arr)

def is_tile_passable(arr):
    return (arr >= 2) & (arr <= 5) 
    
class MyControler(Controler):

    def  init(self):
        self.to_remove = []
        self.ground_map = self.engine.get_map(None)
        possible_indices = self.ground_map.get_indices_filter(is_tile_passable)

        self.slimes = set()
        self.grass_ = set()
        self.roaches = set()

        for _ in range(N_GRASS):
            start_y,start_x = random.choice(possible_indices)
            grass = self.new_entity("Grass",start_x,start_y)
            self.grass_.add(grass)

        for _ in range(N_ROACHES):
            start_y,start_x = random.choice(possible_indices)
            roach = self.new_entity("Roach",start_x,start_y,self.ground_map)
            self.roaches.add(roach)

        hive_y,hive_x = random.choice(possible_indices)
        self.hive = self.new_entity("Hive",hive_x,hive_y)


    def update(self):
        for entity in self.to_remove:
            self.engine.delete_entity(entity)
            self.slimes.discard(entity)
            self.grass_.discard(entity)
            self.roaches.discard(entity)
        self.to_remove = []
            
        if self.engine.step in [x*15+1 for x in range(20)]:
            self.slimes.add(self.new_entity("Slime",self.hive.x,self.hive.y,self.ground_map))

    def on_lbutton_down(self,position):
        roach = self.new_entity("Roach",position[0],position[1],self.ground_map)
        self.roaches.add(roach)

    def plan_remove_entity(self,entity):
        self.to_remove.append(entity)
        
if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    SS = SpriteSheet(GROUNDMAP_SPRITES)
    #    TILER = Tiler8bit(SS,N_PER_ROW,SIZE,index_dict=GROUNDMAP_TILES_DICT)
    TILER = MarchingSquaresTiler(SS,0,SIZE)

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
        
        
