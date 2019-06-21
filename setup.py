#!/usr/bin/env python

from distutils.core import setup

from brightfield_instabilities.version import __version__

setup(name='brightfield_instabilities',
      version=__version__,
      description='Highlights local differences in brightfield tiff stack',
      author='Andrey Aristov',
      author_email='aaristov@pasteur.fr',
      url='https://github.com/aaristov/brightfield-instabilities',
      packages=['brightfield_instabilities'],
      install_requires=[
            'numpy', 
            'scipy',
            'scikit-image', 
            'imageio', 
            'tqdm', 
            'matplotlib',
            'pyyaml']
     )