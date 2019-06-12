
import brightfield_instabilities.io as io
import brightfield_instabilities.io as io
import brightfield_instabilities.corr as cc
import os


OUT_FILENAME = 'brightfield_instabilities.tif'

def process_folder(folderPath, size):
    
    print(f'Processing folder {folderPath}')

    assert os.path.isdir(folderPath)
    assert isinstance(size, int)
    assert size > 1

    fList = io.scan_folder(folderPath)
    two_files = io.select_two_images(fList)
    im0, im1 = io.read_images(*two_files)
    
    try:
        out = cc.sliding_corr(im0, im1, size=size)

    except KeyboardInterrupt:
        print('User stop, exiting')
        exit(2)
    finally:
        
        parentDir = os.path.dirname(folderPath)
        fName = '_'.join([os.path.basename(folderPath), OUT_FILENAME])
        savePath = os.path.join(parentDir, fName)
        io.save_tiff(out, savePath)
    return True
