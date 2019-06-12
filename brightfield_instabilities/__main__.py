import brightfield_instabilities.io as io
import brightfield_instabilities.corr as cc
import argparse, os
from brightfield_instabilities.version import __version__


OUT_FILENAME = 'brightfield_instabilities.tif'


if __name__ == "__main__":
    print(f'Bright Field Instabilities v{__version__}')
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument('--size', default=40)

    args = parser.parse_args()

    folderPath = args.folder
    size = args.size
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
        savePath = os.path.join(parentDir, '_'.join([os.path.basename(folderPath), OUT_FILENAME]))
        io.save_tiff(out, savePath)


