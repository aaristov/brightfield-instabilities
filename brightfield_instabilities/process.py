
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
    skip_frames=-1,
    filename=OUT_FILENAME
    ):
    
    print(f'Processing folder {folderPath}')

    assert os.path.isdir(folderPath), 'Not a folder!'
    assert isinstance(size, int)
    assert size > 1
    assert smooth >= 0

    fList = io.scan_folder(folderPath)
    selected_paths = io.select_multi_images(fList, skip=skip_frames)
    
    assert len(selected_paths) > 1, 'File sequence too short'

    im0 = io.open_tiff(selected_paths[0])
    
    print(im0.shape)

    for i, f in enumerate(selected_paths[1:]):
        f_short = os.path.basename(f)
        im1 = io.open_tiff(f)
        print(f'Processing {f_short}')
    
        out = []
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
            if len(out):
                for ii, channel in enumerate(out):
                    fName = '_'.join([os.path.basename(folderPath), channels[ii], str(i + 1), filename])
                    savePath = os.path.join(parentDir, fName)
                    io.save_tiff(channel, savePath)
            # exit(0)
            else:
                print('Result is empty.')

            im0 = im1

    return True
