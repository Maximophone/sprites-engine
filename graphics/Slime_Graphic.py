from engine import GraphicEntity, Dirs
from spritesheet import SpriteStripAnim
from globalvars import ENTITIES_SPRITES, SIZE_ANIM
from generic import Generic_Graphic

class Slime_Graphic(Generic_Graphic):
    def __init__(self,entity):
        super(Slime_Graphic,self).__init__(entity)
        ALIVE = 1
        DEAD = 0
        self.anims = {
            ALIVE:{
                Dirs.EAST:SpriteStripAnim(ENTITIES_SPRITES,(5,3),4,size=SIZE_ANIM,loop=True,frames=6),
                Dirs.NORTH:SpriteStripAnim(ENTITIES_SPRITES,(5,4),4,size=SIZE_ANIM,loop=True,frames=6),
                Dirs.WEST:SpriteStripAnim(ENTITIES_SPRITES,(5,5),4,size=SIZE_ANIM,loop=True,frames=6),
                Dirs.SOUTH:SpriteStripAnim(ENTITIES_SPRITES,(5,6),4,size=SIZE_ANIM,loop=True,frames=6),
                },
            DEAD:{
                Dirs.EAST:SpriteStripAnim(ENTITIES_SPRITES,(5,14),1,size=SIZE_ANIM,loop=True,frames=6),
                Dirs.NORTH:SpriteStripAnim(ENTITIES_SPRITES,(5,13),1,size=SIZE_ANIM,loop=True,frames=6),
                Dirs.WEST:SpriteStripAnim(ENTITIES_SPRITES,(5,12),1,size=SIZE_ANIM,loop=True,frames=6),
                Dirs.SOUTH:SpriteStripAnim(ENTITIES_SPRITES,(5,11),1,size=SIZE_ANIM,loop=True,frames=6),
                }
            }

    def get_anim(self):
        return self.anims[self.entity.alive][self.entity.orientation]
