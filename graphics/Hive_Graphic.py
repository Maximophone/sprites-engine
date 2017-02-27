from engine import GraphicEntity
from spritesheet import SpriteStripAnim
from globalvars import ENTITIES_SPRITES, SIZE_ANIM
from generic import Generic_Graphic

class Hive_Graphic(Generic_Graphic):
    def __init__(self,entity):
        super(Hive_Graphic,self).__init__(entity)
        self.anim = SpriteStripAnim(ENTITIES_SPRITES,(11*SIZE_ANIM,0*SIZE_ANIM,SIZE_ANIM,SIZE_ANIM),1,loop=True,frames=6)

    def get_anim(self):
        return self.anim
