
import brightfield_instabilities.io as io
import brightfield_instabilities.io as io
import brightfield_instabilities.corr as cc
import os

from functools import partial
from multiprocessing import Pool, cpu_count

from brightfield_instabilities.picassoio import load_movie


OUT_FILENAME = 'brightfield_instabilities.tif'
FOLDER_SUFFIX = 'brightfield_instabilities'

def process_pairwise_pool(
    selected_paths,
    size, 
    smooth, 
    max_shift,
    cc_skip):
    
    images = list(io.read_images(*selected_paths))

    p = Pool(cpu_count())
    fun = partial(cc.sliding_corr, 
                size=size, 
                smooth=smooth,
                cc_skip=cc_skip,
                max_shift=max_shift)
    
    out = p.map(fun, zip(images[:-1], images[1:]))
    return out

def process_pairwise_loop(
    selected_paths,
    size, 
    smooth, 
    max_shift,
    cc_skip):

    im0 = io.open_tiff(selected_paths[0])
    out = []
    for f in selected_paths[1:]:
        f_short = os.path.basename(f)
        im1 = io.open_tiff(f)
        print(f'Processing {f_short}')
    
        res = cc.sliding_corr(
            (im0, im1), 
            size=size, 
            smooth=smooth,
            cc_skip=cc_skip,
            max_shift=max_shift)
        out.append(res)
    
    return out
    

def process_folder(
    path, 
    size, 
    smooth, 
    max_shift,
    cc_skip,
    skip_frames=-1,
    filename=OUT_FILENAME
    ):
    assert isinstance(size, int)
    assert size > 1
    assert smooth >= 0

    print(f'Processing {path}')

    if os.path.isdir(path):
    
        fList = io.scan_folder(path)
        selected_paths = io.select_multi_images(fList, skip=skip_frames)
        
        n_files = len(selected_paths)
        assert n_files > 1, 'File sequence too short'
        if n_files == 2:
            out = process_pairwise_loop(
                selected_paths,
                size, 
                smooth, 
                max_shift,
                cc_skip)
        else:
            out = process_pairwise_pool(
                selected_paths,
                size, 
                smooth, 
                max_shift,
                cc_skip)

    elif os.path.isfile(path) and path.index('ome.tif'):
        movie, [info] = load_movie(path)
        # to be continued

    save_correlation_results(path, out)

    return True


def save_correlation_results(folderPath, out):
    
    parentDir = os.path.dirname(folderPath)
    channels = ['corr', 'x', 'y']
    if len(out):
        general_subfolder = io.create_subfolder(
            parentDir,
            '_'.join([os.path.basename(folderPath), FOLDER_SUFFIX]) 
            )
        channel_subfolders = [ 
            io.create_subfolder(
                general_subfolder, 
                ch
                ) for ch in channels]
        for i, time_step_data in enumerate(out):
            assert len(time_step_data) == 3, 'Bad data'
            for data, channel_folder, channel_name in zip(time_step_data, channel_subfolders, channels):
                fName = '_'.join([channel_name, str(i + 1), '.tif'])
                savePath = os.path.join(channel_folder, fName)
                io.save_tiff(data, savePath)
    # exit(0)
    else:
        print('Result is empty.')
