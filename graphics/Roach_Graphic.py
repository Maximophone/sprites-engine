from engine import GraphicEntity, Dirs
from spritesheet import SpriteStripAnim
from globalvars import ENTITIES_SPRITES, SIZE_ANIM
from generic import Generic_Graphic

class Roach_Graphic(Generic_Graphic):
    def __init__(self,entity):
        super(Roach_Graphic,self).__init__(entity)
        ALIVE = 1
        DEAD = 0
        self.anims = {
            ALIVE:{
                Dirs.EAST:SpriteStripAnim(ENTITIES_SPRITES,(13,3),4,size=SIZE_ANIM,loop=True,frames=6,vertical=True),
                Dirs.NORTH:SpriteStripAnim(ENTITIES_SPRITES,(14,3),4,size=SIZE_ANIM,loop=True,frames=6,vertical=True),
                Dirs.WEST:SpriteStripAnim(ENTITIES_SPRITES,(13,7),4,size=SIZE_ANIM,loop=True,frames=6,vertical=True),
                Dirs.SOUTH:SpriteStripAnim(ENTITIES_SPRITES,(14,7),4,size=SIZE_ANIM,loop=True,frames=6,vertical=True),
                },
            DEAD:{
                Dirs.EAST:SpriteStripAnim(ENTITIES_SPRITES,(13,3),1,size=SIZE_ANIM,loop=True,frames=6,vertical=True),
                Dirs.NORTH:SpriteStripAnim(ENTITIES_SPRITES,(14,3),1,size=SIZE_ANIM,loop=True,frames=6,vertical=True),
                Dirs.WEST:SpriteStripAnim(ENTITIES_SPRITES,(13,7),1,size=SIZE_ANIM,loop=True,frames=6,vertical=True),
                Dirs.SOUTH:SpriteStripAnim(ENTITIES_SPRITES,(14,7),1,size=SIZE_ANIM,loop=True,frames=6,vertical=True),
                }
            }
        
    def get_anim(self):
        return self.anims[self.entity.alive][self.entity.orientation]
