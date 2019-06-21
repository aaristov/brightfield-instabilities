
import argparse, os
from brightfield_instabilities.version import __version__
from functools import partial
from multiprocessing import Pool, cpu_count
from brightfield_instabilities.process import process_folder


if __name__ == "__main__":

    print(f'Bright Field Instabilities v{__version__}')
    
    parser = argparse.ArgumentParser()
    parser.add_argument("folders", nargs='*', help='Folders\' paths to process')
    parser.add_argument('--size', type=int, default=32, help='Window size, px. Integer, 32 by default.')
    parser.add_argument('--smooth', type=float, default=1.5, help='Apply gaussian blur with sigma = smooth. Float, 1.5 by default')
    parser.add_argument('--cc-skip', type=float, default=5, help='Downsample shift map, 5 by default')
    parser.add_argument('--max-shift', type=float, default=5, help='Maximum shift in pixels, 5 by default')
    parser.add_argument('--frame-skip', type=int, default=-1, help='Number of frames to skip. -1 by default, \
        meaning only first and last frames will be correlated (same for 0). 1 means every frame, 2 every second etc.')

    args = parser.parse_args()
    # print(args)

    folderPaths = args.folders
    size = int(args.size)
    smooth = args.smooth
    cc_skip = int(args.cc_skip)
    max_shift = int(args.max_shift)
    skip_frames = int(args.frame_skip)


    # p = Pool(cpu_count())
    fun = partial(
                process_folder,
                smooth=smooth,
                size=size,
                cc_skip=cc_skip,
                max_shift=max_shift,
                skip_frames=skip_frames
                )
    try:
        result = list(map(fun, folderPaths))
    except AssertionError as e:
        for msg in e.args:
            print(f'Bad arguments: {msg}, exiting')
        exit(1)
    
