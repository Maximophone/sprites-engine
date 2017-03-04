import pygame
import numpy as np
from scipy import signal

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

    def image_at(self, rectangle, size=None, colorkey = None):
        "Loads image from x,y,x+w,y+h"
        if size is not None:
            rectangle = (rectangle[0]*size+rectangle[0]*self.interval,rectangle[1]*size+rectangle[1]*self.interval,size,size)
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

    def load_strip(self, rect, image_count, colorkey=None, vertical=False):
        if not vertical:
            tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]) 
                for x in range(image_count)]
        else:
            tups = [(rect[0], rect[1]+rect[3]*x, rect[2], rect[3]) 
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

class SpriteStripAnim(object):

    def __init__(self, filename, rect, count, size = None, colorkey=None, loop=False, frames=1, vertical=False):
        if size is not None:
            rect = (rect[0]*size,rect[1]*size,size,size)
        self.filename = filename
        ss = SpriteSheet(filename)
        self.images = ss.load_strip(rect, count, colorkey, vertical=vertical)
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

kernel_nw = np.array([
        [0,0,0],
        [0,0,1],
        [0,1,1]
    ])
kernel_ne = np.array([
        [0,0,0],
        [1,0,0],
        [1,1,0]
    ])
kernel_sw = np.array([
        [0,1,1],
        [0,0,1],
        [0,0,0]
    ])
kernel_se = np.array([
        [1,1,0],
        [1,0,0],
        [0,0,0]
    ])
kernel_cards = np.array([
        [0,64,0],
        [16,0,8],
        [0,2,0]
    ])
kernel_cards_4bit = np.array([
        [0,16,0],
        [8,0,4],
        [0,2,0]
    ])

def conv_corner(arr,kernel):
    return (signal.convolve2d(arr,kernel,mode='same')==3).astype(int) 

def conv(arr,kernel):
    return signal.convolve2d(arr,kernel,mode='same')

def process_arr_8bit(arr):
    conv_ne = conv_corner(arr,kernel_ne)
    conv_nw = conv_corner(arr,kernel_nw)
    conv_se = conv_corner(arr,kernel_se)
    conv_sw = conv_corner(arr,kernel_sw)
    conv_cards = conv(arr,kernel_cards)
    return (conv_cards + conv_nw + 4*conv_ne + 32*conv_sw + 128*conv_se)*arr+(1-arr)*-1

def process_arr_4bit(arr):
    conv_cards = conv(arr,kernel_cards_4bit)
    return conv_cards*arr+(1-arr)*-1

class Tiler(object):
    def __init__(self, spritesheet,n_per_row,size,offset=(0,0),index_dict=None,colorkey=None):
        if index_dict is None:index_dict = {}
        self.spritesheet = spritesheet
        self.n_per_row = n_per_row
        self.size = size
        self.offset = offset
        self.index_dict = index_dict
        self.colorkey = colorkey
                
    def index_to_coords(self,index):
        """Turns an index number representing the surrounding configuration to a tile index on the spritesheet."""
        new_i = self.index_dict.get(index,index)
        return ((new_i%self.n_per_row)*(self.size+self.offset[0]), (new_i/self.n_per_row)*(self.size+self.offset[1]))
        
    def map_to_indices(self,arr):
        raise NotImplemented

    def get_surface(self,bin_map):
        indices = self.map_to_indices(bin_map.arr)
        surface = pygame.Surface((bin_map.arr.shape[0]*self.size,bin_map.arr.shape[1]*self.size), pygame.SRCALPHA, 32).convert()

        c_i = 0
        c_j = 0
        for i,row in enumerate(indices):
            for j,val in enumerate(row):
                coords = self.index_to_coords(val)
                tile = self.spritesheet.image_at((coords[0],coords[1],self.size,self.size),colorkey=self.colorkey)
                surface.blit(tile, (c_j,c_i))
                c_j+=self.size
            c_i+=self.size
            c_j = 0
        return surface

class Tiler8bit(Tiler):
    
    def map_to_indices(self,arr):
        return process_arr_8bit(arr)
        
class Tiler4bit(Tiler):
    
    def map_to_indices(self,arr):
        return process_arr_4bit(arr)

class BinMap(object):
    def __init__(self,arr):
        self.arr = arr
        self.h = len(arr)
        self.w = len(arr[0]) if self.h else 0
        
    def get_val_and_neighbours(self,x,y):
        arr,h,w = self.arr,self.h,self.w
        n = arr[(y-1)%h][x]
        e = arr[y][(x+1)%w]
        s = arr[(y+1)%h][x]
        w_ = arr[y][(x-1)%w]
        ne = arr[(y-1)%h][(x+1)%w]
        se = arr[(y+1)%h][(x+1)%w]
        nw = arr[(y-1)%h][(x-1)%w]
        sw = arr[(y+1)%h][(x-1)%w]
        return arr[y][x],[nw,n,ne,w_,e,sw,s,se]

    def get_val_and_direct_neighbours(self,x,y):
        arr,h,w = self.arr,self.h,self.w
        n = arr[(y-1)%h][x]
        e = arr[y][(x+1)%w]
        s = arr[(y+1)%h][x]
        w_ = arr[y][(x-1)%w]
        return arr[y][x],[s,w_,n,e]

    def get_indices_ones(self):
        return zip(*np.where(self.arr==1))

    def __iter__(self):
        for i,row in enumerate(self.arr):
            for j,val in enumerate(row):
                yield self.get_val_and_neighbours(i,j)

