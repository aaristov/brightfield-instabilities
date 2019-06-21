# Brightfield Instabilities
Highlights local differences in brightfield images.

For slow tracking in bacteria (say, persistent motion) it's important to know that the cell did not move during fluorescent acquisition. For that purpose bright field images are acquired and saved periodically. We now can use this toolbox to highlight problematic regions in the colony and quantify local displacements.

## Installing from Github

`pip install git+https://github.com/aaristov/brightfield_instabilities.git`


## Manual installation

Use Python 3.7 or newer (conda virtual environment is recommended)

`git clone https://github.com/aaristov/brightfield-instabilities.git`

Go to brightfield-instabilities folder

`pip install -r requirements.txt`

To install into the system:

`pip install .`


## Usage

Suppose you have a folder Pos1 with brightfield images save as individual tiffs.

`python -m brightfield_instabilities path_to_Pos1`

This will compute correlation coefficient between the first and the last image in the folder and output 3 correlation maps as 32-bit tif images:
*  `Pos1_brightfield_instabilities/corr/corr_1_.tif`
*  `Pos1_brightfield_instabilities/x/x_1_.tif`
*  `Pos1_brightfield_instabilities/y/y_1_.tif` 

Correlation spans from -1 for no correlation to 1 for complete similarity. So the map with show dark spots in the places where the bacteria have moved or changed the shape. 

`x` and `y` maps show local displacement in pixels with x-axis spanning from left to right and y-axis from top to bottom. 

Outside colony correlations are still computed by don't make any sense (i.e. noise)

If you want to process time series, add `--frame-skip=N`, where `N` is positive integer. In that case N-th frame with be correlated with the first frame, 2N frame with N etc. Multiple files will be created at the output.

For E.coli colony at pixel size 80 nm the good parameters are

`python -m brightfield_instabilities PATH_TO_FOLDER  --smooth=1.5 --size=32 --max-shift=5 --cc-skip=5`

It is recommended to remove the drift first. In Fiji you can use  Plugins › Registration › Register Virtual Stack Slices

Full command line help:

```
>python -m brightfield_instabilities -h

Bright Field Instabilities v0.4.0
usage: __main__.py [-h] [--size SIZE] [--smooth SMOOTH] [--cc-skip CC_SKIP]
                   [--max-shift MAX_SHIFT] [--frame-skip FRAME_SKIP]
                   [folders [folders ...]]

positional arguments:
  folders               Folders' paths to process

optional arguments:
  -h, --help            show this help message and exit
  --size SIZE           Window size, px. Integer, 32 by default.
  --smooth SMOOTH       Apply gaussian blur with sigma = smooth. Float, 1.5 by
                        default
  --cc-skip CC_SKIP     Downsample shift map, 5 by default
  --max-shift MAX_SHIFT
                        Maximum shift in pixels, 5 by default
  --frame-skip FRAME_SKIP
                        Number of frames to skip. -1 by default, meaning only
                        first and last frames will be correlated (same for 0).
                        1 means every frame, 2 every second etc.
```

