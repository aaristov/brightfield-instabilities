# Brightfield Instabilities
Highlights local differences in brightfield images

# Manual installation

Use Python 3.7 or newer

`git clone https://github.com/aaristov/brightfield_instabilities.git`

Go to brightfield-instabilities folder

`pip install -r requirements.txt`

To install into the system:

`pip install .`

# Installing from Github

`pip install git+https://github.com/aaristov/brightfield_instabilities.git`

# Usage

Suppose you have a folder Pos1 with brightfield images save as individual tiffs.

`python -m brightfield_instabilities path_to_Pos1`

This will compute correlation coefficient between two images and output correlation map as 32-bit tif image `Pos1_brightfield_instabilities.tif`.

positional arguments:

  folders : you can put many -- data processed in parallel.

optional arguments:

  -h, --help   show this help message and exit

  --size SIZE


