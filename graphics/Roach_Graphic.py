from engine import GraphicEntity, Dirs
from spritesheet import SpriteStripAnim
from globalvars import ENTITIES_SPRITES, SIZE_ANIM
from generic import Generic_Graphic

class Roach_Graphic(Generic_Graphic):
    def __init__(self,entity):
        super(Roach_Graphic,self).__init__(entity)
        self.anims = {
                Dirs.SOUTH:SpriteStripAnim(ENTITIES_SPRITES,(13*SIZE_ANIM,3*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6,vertical=True),
                Dirs.WEST:SpriteStripAnim(ENTITIES_SPRITES,(14*SIZE_ANIM,3*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6,vertical=True),
                Dirs.NORTH:SpriteStripAnim(ENTITIES_SPRITES,(13*SIZE_ANIM,7*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6,vertical=True),
                Dirs.EAST:SpriteStripAnim(ENTITIES_SPRITES,(14*SIZE_ANIM,7*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6,vertical=True),
                }

    def get_anim(self):
        return self.anims[self.entity.orientation]
