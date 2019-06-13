# Brightfield Instabilities
Highlights local differences in brightfield images

## Installing from Github

`pip install git+https://github.com/aaristov/brightfield_instabilities.git`


## Manual installation

Use Python 3.7 or newer

`git clone https://github.com/aaristov/brightfield_instabilities.git`

Go to brightfield-instabilities folder

`pip install -r requirements.txt`

To install into the system:

`pip install .`


## Usage

Suppose you have a folder Pos1 with brightfield images save as individual tiffs.

`python -m brightfield_instabilities path_to_Pos1`

This will compute correlation coefficient between two images and output correlation map as 32-bit tif image `Pos1_brightfield_instabilities.tif`.

```
>python -m brightfield_instabilities -h

Bright Field Instabilities v0.1.3
usage: __main__.py [-h] [--size SIZE] [--smooth SMOOTH]
                   [folders [folders ...]]

positional arguments:
  folders          Folders' paths to process

optional arguments:
  -h, --help       show this help message and exit
  --size SIZE      Window size, px. Integer, 40 by default.
  --smooth SMOOTH  Apply gaussian blur with sigma = smooth. Float, 0 by
                   default
```

