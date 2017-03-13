import numpy as np
from scipy import interpolate
from marching_squares import array_reshape


def interpol_array(arr,factor):
    def inner(arr_22):
        vstart = np.linspace(arr_22[0],arr_22[2],factor,endpoint=False)
        vend = np.linspace(arr_22[1],arr_22[3],factor,endpoint=False)
        hval = np.linspace(0,1,factor,endpoint=False)
        new_arr = np.matmul(vstart[:,None],1-hval[None,:]) + np.matmul(vend[:,None],hval[None,:])
        return new_arr.flatten()
    reshaped = array_reshape(arr)
    interpolated = np.apply_along_axis(inner,2,array_reshape(arr)).reshape((reshaped.shape[0],reshaped.shape[1],factor,factor))
    return np.concatenate(np.concatenate(interpolated,axis=1),axis=1)
    

def gen_map_arr(size_x,size_y,factor=4,min=0,max=8):
    original_array = np.random.randint(min,max,size=(size_x//factor+1,size_y//factor+1))
    original_array[:,0] = 0
    original_array[:,-1] = 0
    original_array[0,:] = 0
    original_array[-1,:] = 0
    interpolated_array = interpol_array(original_array,factor).astype(int)
    return interpolated_array[:size_x,:size_y]
    
