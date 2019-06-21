import numpy as np
from scipy.ndimage import gaussian_filter as gf
import brightfield_instabilities.plot as plot
from tqdm.auto import tqdm
from skimage.feature import match_template
import logging
from matplotlib import pyplot as plt

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def crop(data, corner_x, corner_y, size):
    '''
    Crops 2d array
    Outputs size*size crop
    '''
    return data[corner_y:corner_y+size, corner_x:corner_x+size]

def get_corrcoef(*arr):
    '''
    Computes normalized correlation btween two images 
    
    '''
    ravels = tuple(t.ravel() for t in arr)
    stack = np.vstack(ravels)
    return np.corrcoef(stack)[0, 1]

def sliding_corr(
    im0:np.ndarray, 
    im1:np.ndarray, 
    size:int=40, 
    verbose:bool=False, 
    fun=get_corrcoef, 
    min_corr=0.5, 
    smooth:float=0, 
    cc_skip=10, 
    max_shift=5
    ):
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
        Function used to compute similarity of the fragments. get_corrcoef by default
    min_corr: float, < 1, optional
        minimal value of correlation to launch vector calculation. 0.5 by default.
    smooth : float, optional
        Smotthing kernel sigma in pixels. If positive, smooth both images before processing. 
    cc_skip : int, optional
        Undersampling of cross-correlation xy shift. 10 by default
    max_shift: int, optional
        Maximum shift in pixels. 5 by default
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

    assert im0.shape == im1.shape, f'image shapes are different {im0.shape, im1.shape}, check your stack'
    assert size > 8, f'size is too small, expected at least 8, got {size}'
    assert im0.ndim == 2, f'bad dimentionality {im0.ndim}, expected 2'
    assert smooth >= 0, f'smooth must not be negative, got {smooth}'
    assert min_corr < 1. and min_corr > 0, f'min_corr must be from 0 to 1, got {min_corr}'
    assert cc_skip > 0 and isinstance(cc_skip, int) , f'cc_skip should be positive integer, got {cc_skip}'
    assert max_shift > 0 and max_shift < size / 3 , f'max_shift can not exceed 1 / 3 * size = {1 / 3 * size:.1f}, got {max_shift}'
    
    print(f'Start processing with window size {size}')
    print(f'Data shape: {im0.shape}')
    qy, qx = np.indices(im0.shape)
    corrMap = np.zeros_like(im0, dtype=float)
    vectorMap = np.stack((corrMap, corrMap, corrMap), axis=0)
    print(f'vectorMap shape: {vectorMap.shape}')

    if smooth:
        print(f'Smoothing with sigma {smooth}')
        im0 = gf(im0, smooth)
        im1 = gf(im1, smooth)
        
    for x, y in tqdm(list(zip(np.ravel(qx), np.ravel(qy)))):
        template = crop(im0, x, y, size)
        image = crop(im1, x, y, size)
        if template.shape == (size, size) and image.shape == (size, size):
            corrCoef = get_corrcoef(image, template)
            vectorMap[0, y+size//2, x+size//2] = corrCoef
            if verbose:
                plot.multi_imshow(template, image, corrMap)
                print(corrCoef)
            
            if False:#corrCoef > min_corr and x % cc_skip == 0 and y % cc_skip == 0:
                crop_t = max_shift
                template_crop = template[crop_t:-crop_t, crop_t:-crop_t]
                cc = cc_template(image, template_crop, verbose=False)
                
                y_cc, x_cc = get_abs_max(cc)
                x_cc = x_cc - crop_t
                y_cc = y_cc - crop_t

                r = cc_skip // 2
                s = size // 2
                _yrange = y + s - r ,  y + s + r
                _xrange = x + s - r ,  x + s + r
                vectorMap[1, _yrange[0] : _yrange[1] , _xrange[0] : _xrange[1]] = x_cc
                vectorMap[2, _yrange[0] : _yrange[1] , _xrange[0] : _xrange[1]] = y_cc

    return vectorMap.astype(np.float32)


class FitResult():

    def __init__(self,
                 x=None,
                 y=None,
                 z=None,
                 good=False,
                 result_fit=None,
                 z_px=None):
        self.x = x
        self.y = y
        self.z = z
        self.good = good
        self.result_fit = result_fit
        self.z_px = z_px

    def __iter__(self):
        for a in (self.x, self.y, self.z, self.good, self.result_fit, self.z_px):
            yield a

    def __repr__(self):
        return 'x={}, y={}, z={}, good={}, result_fit={}, z_px={}'.format(self.x,
                                                                          self.y, self.z, self.good, self.result_fit,
                                                                          self.z_px)


def get_abs_max(data):
    """
    peaks up absolute maximum position in the stack/ 2D image
    First dimension comes first
    :param data: np.array
    :return: abs max coordinates in data.shape format
    """
    return np.unravel_index(np.argmax(data), data.shape)


def get_xcorr(image, template, verbose=False):
    try:
        cc = match_template(image, template, pad_input=False)
        if verbose:
            plot.multi_imshow(image, template, cc, 
                    titles=['image', 'template', 'cc'])
        return cc
    except ValueError:
        logging.error(f"Error in cc_template. Image shape {image.shape}, template shape {template.shape  }")


def fit_gauss_3d(img: np.ndarray,
                 radius_xy: int = 4,
                 min_xcorr: np.float = 0.5,
                 debug=False) -> FitResult:
    """
    Detects maximum on the stack in 3D
    Fitting 2D gaussian in xy, 4-order polynomial in z
    Ouputs [x,y,z] in pixels
    """
    fit2d = True

    from brightfield_instabilities import gaussfit

    logger.debug(f'Start fit_gauss_3d with the stack shape zyx {img.shape}')
    logger.debug(f'radius_xy={radius_xy}')
    

    
    cc_value = np.max(img)
    if cc_value < min_xcorr:
        # raise(LowXCorr("fit_gauss_3d: Cross corellation value os too low!"))
        logger.error("fit_gauss_3d: Cross corellation value os too low!")
        return FitResult()
    else:
        logger.debug(f'cc peak value={cc_value}')

    y_px, x_px = get_abs_max(img)
    y_max, x_max = img.shape
    
    # r = radius_xy

    # y1 = max(0, y_px - r)
    # y2 = min(y_max, y_px + r)
    # x1 = max(0, x_px - r)
    # x2 = min(x_max, x_px + r)
    
    # cut_img = img[y1:y2, x1:x2]
    cut_img = img
    logger.debug(f'After cutting x,y we got cut_stack shape {cut_img.shape}')
    

    if False:
        plt.imshow(img)
        plt.title('Max xy projection of cc-stack')
        plt.show()
    
    logger.debug(f'Got absolute maximum xyz (px) {(x_px, y_px )}')
    
    '''
    _, _x, _y = get_abs_max(cut_stack)
    logger.debug(f'Looking for xy peak {(_x, _y)}')

    z_crop = cut_stack[:, _y-1:_y+2, _x-1:_x+2]
    logger.debug(f'Crop {z_crop.shape}')

    z_proj = z_crop.mean(axis=(1, 2))
    '''
    # z_proj = cut_stack[:,r].max(axis=1) #ignore y
    # z_proj = cut_stack[:,r,r] #ignore xy
    # z_proj = cut_stack[:,r,r]

    # [(_min, _max, y, x, sig), good] = gaussfit.fitSymmetricGaussian(xy_proj,sigma=1)
    logger.debug('Fit gauss xy')
    try:
        [(_min, _max, y, x, _, _, _), good] = gaussfit.fitEllipticalGaussian(cut_img)
        # [result_fit, good] = gaussfit.fitEllipticalGaussian3D(cut_stack, init=fit_init)
        # background, height, z, y, x, el_x, el_y, el_z, an_xy, an_yz, an_xz, ramp_x, ramp_y, ramp_z = result_fit

    except Exception as e:
        logger.error(f'Error in gaussian fit: {e}')
        #logger.error(f'result: {result_fit}')
        return FitResult()

    # x_found = x - r + x_px
    # y_found = y - r + y_px
    x_found = x - x_max / 2
    y_found = y - y_max / 2
    logger.debug(f'xy found: {x_found:.2f} , {y_found:.2f}')

    
    logger.debug(f'raw xy {np.round((x, y),2)}')

    
    if debug and fit2d:
        fig = plt.figure(dpi=72, figsize=(3, 3))
        plt.imshow(cut_img)
        plt.plot(x,y,'r+')
        plt.title('xy')
        plt.colorbar()
        plt.show()
        
    return FitResult(x_found, y_found, 0, good, None, 0)

