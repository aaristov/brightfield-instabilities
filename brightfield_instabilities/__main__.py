
import argparse, os
from brightfield_instabilities.version import __version__
from functools import partial
from multiprocessing import Pool, cpu_count
from brightfield_instabilities.process import process_folder


if __name__ == "__main__":

    print(f'Bright Field Instabilities v{__version__}')
    
    parser = argparse.ArgumentParser()
    parser.add_argument("folders", nargs='*')
    parser.add_argument('--size', type=int, default=40)
    parser.add_argument('--smooth', type=float, default=0)

    args = parser.parse_args()

    folderPaths = args.folders
    size = args.size
    smooth = args.smooth

    p = Pool(cpu_count())
    fun = partial(
                process_folder,
                smooth=smooth,
                size=int(size)
                )
    result = list(p.map(fun, folderPaths))
    
