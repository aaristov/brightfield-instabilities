
import brightfield_instabilities.io as io
import brightfield_instabilities.io as io
import brightfield_instabilities.corr as cc
import os


OUT_FILENAME = 'brightfield_instabilities.tif'


def process_folder(
    folderPath, 
    size, 
    smooth, 
    max_shift,
    cc_skip,
    filename=OUT_FILENAME
    ):
    
    print(f'Processing folder {folderPath}')

    assert os.path.isdir(folderPath), 'Not a folder!'
    assert isinstance(size, int)
    assert size > 1
    assert smooth >= 0

    fList = io.scan_folder(folderPath)
    two_files = io.select_two_images(fList)
    im0, im1 = io.read_images(*two_files)
    
    try:
        out = cc.sliding_corr(
            im0, 
            im1, 
            size=size, 
            smooth=smooth,
            cc_skip=cc_skip,
            max_shift=max_shift)

    except KeyboardInterrupt:
        print('User stop, exiting')
        return False
    
    finally:    
        parentDir = os.path.dirname(folderPath)
        channels = ['corr', 'x', 'y']
        for i, channel in enumerate(out):
            fName = '_'.join([os.path.basename(folderPath), channels[i], filename])
            savePath = os.path.join(parentDir, fName)
            io.save_tiff(channel, savePath)
        # exit(0)

    return True
