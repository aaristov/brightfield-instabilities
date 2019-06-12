import numpy as np
from scipy.ndimage import gaussian_filter as gf
import brightfield_instabilities.plot as plot
from tqdm.auto import tqdm



def crop(data, corner_x, corner_y, size):
    '''
    Crops 2d array
    Outputs size*size crop
    '''
    return data[corner_y:corner_y+size, corner_x:corner_x+size]

def corrcoef(*arr):
    '''
    Computes normalized correlation btween two images 
    
    '''
    ravels = tuple(t.ravel() for t in arr)
    stack = np.vstack(ravels)
    return np.corrcoef(stack)[0, 1]

def sliding_corr(im0:np.ndarray, im1:np.ndarray, size:int=40, verbose:bool=False, fun=corrcoef, smooth:float=0):
    '''
    Computes correlation coefficient between two two images using sliding window of size 'size'
    
    Parameters:
    ----------
    im0 : 2d array, same size as im1
    im1 : 2d array
    size: int, optional
        Size for sliding window
    verbose: bool, optional
        Default is False. If True, plots crops and output array at every step of sliding window path.
    fun : function, optional
        Function used to compute similarity of the fragments. corrcoef by default
    smooth : float, optional
        Smotthing kernel sigma in pixels. If positive, smooth both images before processing. 

    Returns:
    -------
    out : 2d array of the same size as original images

    Raises:
    ------
    AssertionError
        if images have different size
        if number of dimensions is not 2
        if `smooth` less than zero
    
    '''

    assert im0.shape == im1.shape
    assert im0.ndim == 2
    assert smooth >= 0

    print(f'Start processing with window size {size}')
    print(f'Data shape: {im0.shape}')
    qy, qx = np.indices(im0.shape)
    out = np.zeros_like(im0, dtype=float)

    if smooth:
        print(f'Smoothing with sigma {smooth}')
        im0 = gf(im0, smooth)
        im1 = gf(im1, smooth)
        
    for x, y in tqdm(list(zip(np.ravel(qx), np.ravel(qy)))):
        template = crop(im0, x, y, size)
        image = crop(im1, x, y, size)
        if template.shape == (size, size) and image.shape == (size, size):
            out[y+size//2, x+size//2] = fun(image, template)
            if verbose:
                plot.multi_imshow(template, image, out)
                print(fun(template, image))

    return out.astype(np.float32)
