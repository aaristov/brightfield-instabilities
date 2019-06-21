# Brightfield Instabilities
Highlights local differences in brightfield images.

For slow tracking in bacteria (say, persistent motion) it's important to know that the cell did not move during fluorescent acquisition. For that purpose bright field images are acquired and saved periodically. We now can use this toolbox to highlight problematic regions in the colony.

## Installing from Github

`pip install git+https://github.com/aaristov/brightfield_instabilities.git`


## Manual installation

Use Python 3.7 or newer

`git clone https://github.com/aaristov/brightfield-instabilities.git`

Go to brightfield-instabilities folder

`pip install -r requirements.txt`

To install into the system:

`pip install .`


## Usage

Suppose you have a folder Pos1 with brightfield images save as individual tiffs.

`python -m brightfield_instabilities path_to_Pos1`

This will compute correlation coefficient between the first and the last image in the folder and output correlation map as 32-bit tif image `Pos1_brightfield_instabilities.tif`. 

Correlation spans from -1 for no correlation to 1 for complete similarity. So the map with show dark spots in the places where the bacteria have moved or changed the shape. 

For E.coli colony the good parameters are

`python -m brightfield_instabilities PATH_TO_FOLDER  --smooth=1.5 --size=32 --max-shift=5 --cc-skip=5`

It is recommended to remove the drift first. In Fiji you can use  Plugins › Registration › Register Virtual Stack Slices

```
>python -m brightfield_instabilities -h

Bright Field Instabilities v0.3.0
usage: __main__.py [-h] [--size SIZE] [--smooth SMOOTH] [--cc-skip CC_SKIP]
                   [--max-shift MAX_SHIFT]
                   [folders [folders ...]]

positional arguments:
  folders               Folders' paths to process

optional arguments:
  -h, --help            show this help message and exit
  --size SIZE           Window size, px. Integer, 40 by default.
  --smooth SMOOTH       Apply gaussian blur with sigma = smooth. Float, 0 by
                        default
  --cc-skip CC_SKIP     Downsample shift map, 10 by default
  --max-shift MAX_SHIFT
                        Maximum shift in pixels, 5 by default

```

