import pygame
import spritesheet
import numpy as np

def corners_to_tile_id(vTL,vTR,vBL,vBR):
    """ Generates tile_id from corner values. T stands for top, B bottom, R right, L left"""
    # First lets store half values
    hTL = vTL>>1
    hTR = vTR>>1
    hBL = vBL>>1
    hBR = vBR>>1

    # We compute the saddle value (1 bit)
    saddle = ((vTL&1) + (vTR&1) + (vBL&1) + (vBR&1) + 1) >> 2

    # We compute the shape (4 bits)
    shape = (hTL&1) | (hTR&1) << 1 | (hBL&1) << 2 | (hBR&1) << 3

    # We compute the ring value (number of bits depends of number of tile types)
    ring = (hTL + hTR + hBL + hBR) >> 2

    # Finally, tile id
    tile_id = shape | (saddle << 4) | (ring << 5)

    # We also return row and col for direct mapping onto the tilesheet
    row = (ring << 1) | saddle
    col = shape - (ring & 1)

    return tile_id, row, col

def corners_to_values(vTL,vTR,vBL,vBR):
    """Generates inner values from corners"""
    hTL = vTL>>1
    hTR = vTR>>1
    hBL = vBL>>1
    hBR = vBR>>1

    value = (hTL + hTR + hBL + hBL) >> 2

    return value

def v_corners_to_values(row):
    return corners_to_values(*row)

def corners_array_to_values(arr):
    return np.apply_along_axis(v_corners_to_values,2,array_reshape(arr))
    
def vfunc(row):
    return corners_to_tile_id(*row)

def array_reshape(arr):
    BR = arr[1:,1:,None]
    TR = np.roll(arr,1,axis=0)[1:,1:,None]
    BL = np.roll(arr,1,axis=1)[1:,1:,None]
    TL = np.roll(np.roll(arr,1,axis=0),1,axis=1)[1:,1:,None]

    new_arr = np.concatenate([TL,TR,BL,BR],axis=2)
                              
    return new_arr

class MarchingSquaresTiler(object):

    def __init__(self,tilesheet,n_per_row,size,index_dict=None,colorkey=None):
        """
        A MarchingSquaresTiler will return tiles from a map (2D array of integers) according
        to the Marching Squares technique. 
        http://blog.project-retrograde.com/2013/05/marching-squares/

        Args:
        - tilesheet: SpriteSheet object containing the tiles
        - n_per_row: number of tiles per row in the tilesheet
        - size: size in pixels of each tile in the tilesheet (assumed square)
         
        Kwargs:
        - index_dict: dictionary that maps a tile id to a tile number in the tile sheet
        - colorkey: The color to use as alpha value
        """
        if index_dict is None:
            index_dict = {}
        self.tilesheet = tilesheet
        self.n_per_row = n_per_row
        self.size = size
        self.index_dict = index_dict
        self.colorkey = colorkey

    @staticmethod
    def map_to_tile_ids(arr):
        """ Given a numpy array, returns a new array that contains the tile_id, row and column.
        The returned array will be 1 cell smaller in each dimension than the original.
        """
        corners = array_reshape(arr)
        tile_id_map = np.apply_along_axis(vfunc,2,corners)
        return tile_id_map

    def get_surface(self,arr):
        tile_id_map = self.map_to_tile_ids(arr)
        surface_shape = (arr.shape[0]*self.size,arr.shape[1]*self.size)
        surface = pygame.Surface(surface_shape,pygame.SRCALPHA,32).convert()

        for i,vrow in enumerate(tile_id_map):
            for j,(tile_id,row,col) in enumerate(vrow):
                tile = self.tilesheet.image_at((col,row),size=self.size,colorkey=self.colorkey)
                surface.blit(tile, (j*self.size,i*self.size))

        return surface

class MSMap(object):
    def __init__(self,arr):
        """Marching Squares map."""
        self.corners = arr
        self.values = corners_array_to_values(arr)
        self.h = len(self.values)
        self.w = len(self.values[0]) if self.h else 0
        
    def get_values(self):
        return self.values

    def get_val_and_direct_neighbours(self,x,y):
        arr,h,w = self.values,self.h,self.w
        n = arr[(y-1)%h][x]
        e = arr[y][(x+1)%w]
        s = arr[(y+1)%h][x]
        w_ = arr[y][(x-1)%w]
        return arr[y][x],[s,w_,n,e]

    def get_indices_filter(self,filter):
        return zip(*np.where(filter(self.values)))
