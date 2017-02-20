from engine import GraphicEntity
from spritesheet import SpriteStripAnim
from globalvars import ENTITIES_SPRITES, SIZE_ANIM

class Grass_Graphic(GraphicEntity):
    def __init__(self,entity):
        super(Grass_Graphic,self).__init__(entity)
        self.anims = {
            0:SpriteStripAnim(ENTITIES_SPRITES,(1*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6),
            1:SpriteStripAnim(ENTITIES_SPRITES,(2*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6),
            2:SpriteStripAnim(ENTITIES_SPRITES,(3*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6),
            3:SpriteStripAnim(ENTITIES_SPRITES,(4*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6)
            }

    def get_anim(self):
        return self.anims[self.entity.growth]