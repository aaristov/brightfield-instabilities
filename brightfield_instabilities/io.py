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
    sel = []
    if skip <= 0:
        sel.append(fileList[0])
        sel.append(fileList[-1])
    else:
        for i in fileList[::skip]:
            sel.append(i)
        if i != fileList[-1]:
            sel.append(fileList[-1])
    print('Selected ', list(os.path.basename(p) for p in sel))
    return sel

def read_images(*paths, handler=open_tiff):
    '''
    reads every entry in file list
    '''
    print('Reading ', list(os.path.basename(p) for p in paths))
    for p in paths:
        img = handler(p)
        yield img

def create_subfolder(current_path, folder_name):
    '''
    Creates a folder inside current folder.
    Returns 
        the new subfolder path
    Raises
        IOError, AssertionError if folder has not be created
    '''
    assert os.path.isdir(current_path)
    desired_path = os.path.join([current_path, folder_name])
    if not os.path.isdir(desired_path):
        try:
            os.mkdir(desired_path)
            assert os.path.isdir(desired_path), 'Unable to create a folder.'
            print(f'Create {folder_name} subfolder')
            return desired_path
        except IOError as e:
            print(f'IOError, {e.args}')
            raise e
    

