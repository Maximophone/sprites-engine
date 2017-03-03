import random
from engine import Entity
from generic import GenericAging

class Roach(GenericAging):
    clazz = 'roach'

    def init(self,ground_map):
        death_age = random.randint(120,150)
        delete_age = death_age + 10
        super(Roach,self).init(ground_map,death_age,delete_age)

    def update(self):
        self.resolve_age()
        if self.alive:
            possible_dirs = self.get_dirs()
            d = random.choice(possible_dirs)
            self.move(d)
