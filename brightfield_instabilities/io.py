import imageio
import numpy as np
from glob import glob
import os

def open_tiff(path:str) -> np.ndarray:
    '''
    Opens single tif file
    '''
    return imageio.imread(path)

def scan_folder(path, pattern='*.tif'):
    '''
    Returns a list of images
    '''
    return glob(path + os.path.sep + pattern)

def select_two_images(fileList:list):
    return (fileList[0], fileList[-1])

def read_images(*paths, handler=open_tiff):
    '''
    reads every entry in file list
    '''
    return (handler(p) for p in paths)