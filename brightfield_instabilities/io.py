import imageio
import numpy as np
from glob import glob
import os

def open_tiff(path:str) -> np.ndarray:
    '''
    Opens single tif file
    '''
    return imageio.imread(path)

def save_tiff(array:np.ndarray, path:str):
    print(f'Saving tif file to {path}')
    imageio.imsave(path, array, 'tiff')
    return True

def scan_folder(path, pattern='*.tif'):
    '''
    Returns a list of images
    '''
    
    flist = glob(path + os.path.sep + pattern)
    print(f'Found {len(flist)} files')
    return glob(path + os.path.sep + pattern)

def select_two_images(fileList:list):
    sel = (fileList[0], fileList[-1])
    print('Selected ', list(os.path.basename(p) for p in sel))
    return sel

def select_multi_images(fileList:list, skip:int=-1):
    sel = [fileList[0]]
    if skip <= 0:
        sel.append(fileList[-1])
    else:
        for i in fileList[::skip]:
            sel.append(i)
    print('Selected ', list(os.path.basename(p) for p in sel))
    return sel

def read_images(*paths, handler=open_tiff):
    '''
    reads every entry in file list
    '''
    print('Reading ', list(os.path.basename(p) for p in paths))
    return (handler(p) for p in paths)