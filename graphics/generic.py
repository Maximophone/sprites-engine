from engine import GraphicEntity
from globalvars import SIZE_ANIM

class Generic_Graphic(GraphicEntity):
    def __init__(self,entity):
        super(Generic_Graphic,self).__init__(entity,(SIZE_ANIM,SIZE_ANIM))
