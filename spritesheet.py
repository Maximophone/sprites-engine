import pygame
import numpy as np

class SpriteSheet(object):
    def __init__(self, filename, offset=(0,0), interval=False):
        self.offset = offset
        self.interval = interval
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error, message:
            print("Unable to load spritesheet image: ",filename)
            raise SystemExit, message

        self._cache = {}

    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+w,y+h"
        if rectangle in self._cache:
            return self._cache[rectangle]
        rect = pygame.Rect(
            rectangle[0]+self.offset[0],
            rectangle[1]+self.offset[1],
            rectangle[2],
            rectangle[3])
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0,0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        self._cache[rectangle] = image
        return image

    def images_at(self, rects, colorkey = None):
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]) 
            for x in range(image_count)]
        return self.images_at(tups, colorkey)

class SpriteStripAnim(object):

    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1):
        self.filename = filename
        ss = SpriteSheet(filename)
        self.images = ss.load_strip(rect, count, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames

    def iter(self):
        self.i = 0
        self.f = self.frames
        return self

    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image

    def __add__(self, ss):
        self.images.extend(ss.images)
        return self

class Tiler(object):
    def __init__(self, spritesheet,n_per_row,size,offset=(0,0),index_dict=None,colorkey=None):
        if index_dict is None:index_dict = {}
        self.spritesheet = spritesheet
        self.n_per_row = n_per_row
        self.size = size
        self.offset = offset
        self.index_dict = index_dict
        self.colorkey = colorkey
        
    def calc_ss_index(self,center,nw,n,ne,w,e,sw,s,se):
        raise NotImplemented
        
    def index_to_coords(self,index):
        new_i = self.index_dict.get(index,index)
        return ((new_i%self.n_per_row)*(self.size+self.offset[0]), (new_i/self.n_per_row)*(self.size+self.offset[1]))
        
    def get_tile(self,center,neighbours):
        nw,n,ne,w,e,sw,s,se = neighbours
        index = self.calc_ss_index(center,nw,n,ne,w,e,sw,s,se)
        coords = self.index_to_coords(index)
        return self.spritesheet.image_at((coords[0],coords[1],self.size,self.size),colorkey=self.colorkey)

    def get_surface(self,bin_map):

        surface = pygame.Surface((bin_map.arr.shape[0]*self.size,bin_map.arr.shape[1]*self.size), pygame.SRCALPHA, 32).convert_alpha()

        c_i = 0
        c_j = 0
        for i,row in enumerate(bin_map.arr):
            for j,val in enumerate(row):
                val,neighbours = bin_map.get_val_and_neighbours(i,j)
                image = self.get_tile(val,neighbours)
                surface.blit(image, (c_j,c_i))
                c_j+=self.size
            c_i+=self.size
            c_j = 0
        return surface

class Tiler8bit(Tiler):
    
    def calc_ss_index(self,center,nw,n,ne,w,e,sw,s,se):
        if not center:
            return -1
        vals = [
            (nw&n&w)<<0,
            n<<1,
            (ne&n&e)<<2,
            w<<3,
            e<<4,
            (sw&s&w)<<5,
            s<<6,
            (se&s&e)<<7
        ]
        return sum(vals)
        
class Tiler4bit(Tiler):
    
    def calc_ss_index(self,center,nw,n,ne,w,e,sw,s,se):
        if not center:
            return -1
        vals = [
            n<<0,
            w<<1,
            e<<2,
            s<<3,
        ]
        return sum(vals)

class BinMap(object):
    def __init__(self,arr):
        self.arr = arr
        self.w = len(arr)
        self.h = len(arr[0]) if self.w else 0
        
    def get_val_and_neighbours(self,i,j):
        arr,h,w = self.arr,self.h,self.w
        n = arr[(i-1)%w][j]
        e = arr[i][(j+1)%h]
        s = arr[(i+1)%w][j]
        w_ = arr[i][(j-1)%h]
        ne = arr[(i-1)%w][(j+1)%h]
        se = arr[(i+1)%w][(j+1)%h]
        nw = arr[(i-1)%w][(j-1)%h]
        sw = arr[(i+1)%w][(j-1)%h]
        return arr[i][j],[nw,n,ne,w_,e,sw,s,se]

    def get_val_and_direct_neighbours(self,i,j):
        arr,h,w = self.arr,self.h,self.w
        n = arr[(i-1)%w][j]
        e = arr[i][(j+1)%h]
        s = arr[(i+1)%w][j]
        w_ = arr[i][(j-1)%h]
        return arr[i][j],[s,w_,n,e]

    def get_indices_ones(self):
        return zip(*np.where(self.arr==1))

    def __iter__(self):
        for i,row in enumerate(self.arr):
            for j,val in enumerate(row):
                yield self.get_val_and_neighbours(i,j)
