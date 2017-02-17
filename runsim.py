from spritesheet import BinMap, SpriteSheet, Tiler4bit, Tiler8bit, SpriteStripAnim
from engine import *
import pygame
import numpy as np

N_PER_ROW = 16
SIZE = 48
SIZE_ANIM = 16


class Critter(Entity):
    clazz = 'critter'
    
    def update(self):
        self.move(random.randint(0,3))

class Grass(Entity):
    clazz = 'grass'
    
    def update(self):
        pass

class AnimsStore(object):
    @staticmethod
    def get_anim(clazz):
        if clazz == 'critter':
            return {
                0:SpriteStripAnim("./spritesheet.png",(5*SIZE_ANIM,3*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6),
                1:SpriteStripAnim("./spritesheet.png",(5*SIZE_ANIM,4*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6),
                2:SpriteStripAnim("./spritesheet.png",(5*SIZE_ANIM,5*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6),
                3:SpriteStripAnim("./spritesheet.png",(5*SIZE_ANIM,6*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6),
                }
        elif clazz == 'grass':
            return {
                0:SpriteStripAnim("./spritesheet.png",(3*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6),
                1:SpriteStripAnim("./spritesheet.png",(3*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6),
                2:SpriteStripAnim("./spritesheet.png",(3*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6),
                3:SpriteStripAnim("./spritesheet.png",(3*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6),
                }


if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((400,300))

    critter1 = Critter(5,5)
    critter2 = Critter(2,2)
    grass1 = Grass(4,4)

    engine = Engine([grass1, critter1, critter2],AnimsStore)

    clock = pygame.time.Clock()

    map = BinMap(np.random.randint(0,2,(10,10)))

    ss = SpriteSheet('./tileset-big.png')

    tiler1 = Tiler4bit(ss,N_PER_ROW,SIZE)
    
    i = 0
    while True:
        screen.fill(pygame.Color("black"))
        for ij,tile in enumerate(map):
            screen.blit(tiler1.get_tile(*tile),(ij/N_PER_ROW*SIZE,ij%N_PER_ROW*SIZE))
        
        if not i%30:
            engine.next()
        
        for entity,graphic in zip(engine.entities,engine.graphic_entities):
            graphic.update(entity.x,entity.y)
            screen.blit(graphic.anim[entity.orientation].next(),(graphic.x*SIZE_ANIM,graphic.y*SIZE_ANIM))
            
        pygame.display.flip()
        clock.tick(60)
        i+=1