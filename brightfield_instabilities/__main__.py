import brightfield_instabilities.io as io
import brightfield_instabilities.corr as cc
import argparse, os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument('--size', default=40)

    args = parser.parse_args()

    foldername = args.folder
    size = args.size
    assert os.path.isdir(foldername)
    assert isinstance(size, int)
    assert size > 1

    fList = io.scan_folder(foldername)
    two_files = io.select_two_images(fList)
    im0, im1 = io.read_images(*two_files)
    
    try:
        out = cc.sliding_corr(im0, im1, size=size)
    except KeyboardInterrupt:
        print('User stop, exiting')


