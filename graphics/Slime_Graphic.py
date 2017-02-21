from engine import GraphicEntity, Dirs
from spritesheet import SpriteStripAnim
from globalvars import ENTITIES_SPRITES, SIZE_ANIM

class Slime_Graphic(GraphicEntity):
    def __init__(self,entity):
        super(Slime_Graphic,self).__init__(entity)
        self.anims = {
                Dirs.EAST:SpriteStripAnim(ENTITIES_SPRITES,(5*SIZE_ANIM,3*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6),
                Dirs.NORTH:SpriteStripAnim(ENTITIES_SPRITES,(5*SIZE_ANIM,4*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6),
                Dirs.WEST:SpriteStripAnim(ENTITIES_SPRITES,(5*SIZE_ANIM,5*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6),
                Dirs.SOUTH:SpriteStripAnim(ENTITIES_SPRITES,(5*SIZE_ANIM,6*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),4,loop=True,frames=6),
                }

    def get_anim(self):
        return self.anims[self.entity.orientation]