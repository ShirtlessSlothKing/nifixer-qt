#!/usr/bin/env python

import os
import sys
import shutil
import subprocess
import argparse
import platform
import pyside2uic
import nifixer
import nifixer.settings
from   setuptools         import setup, find_packages
from   setuptools.command import build_py

# run this script from within setup.py directory 
target_dir = os.path.dirname(os.path.abspath(__file__))
if os.getcwd() != target_dir:
    try:
        os.chdir(target_dir)
    except Exception as e:
        print('Failed changing to correct directory, please try and run this script from where setup.py is located')
        sys.exit(1)

try:
    # generate python files from ui files 
    pyside2uic.compileUiDir('resources',map=lambda dir,module: 
        (os.path.join('nifixer','ui'),  os.path.splitext(module)[0] + '_ui.py')
    )
        
except Exception as e:
    print('failed generating python class from ui files: ', e)
    sys.exit(1)

try:
    # generate python resource files
    subprocess.run(
        [
            'pyside2-rcc',
            '-o',
            os.path.join('nifixer','ui','resources_rc.py'),
            os.path.join('resources','resources.qrc')
        ],
        check=True)
except Exception as e:
    print('failed generating python resource files: ', e)
    sys.exit(1)
        
setup(
    name = 'nifixer',
    version = nifixer.settings.__version__,
    author = 'Cody Glassman',
    author_email = 'glassmancody@gmail.com',
    description = ('Qt application to fix mesh and texture files to be compatible with OpenMW'),
    license = 'MIT',
    keywords = 'openmw morrowind nif',
    packages=find_packages(),
    install_requires=['pyside2','pyffi==2.2.2'],
    entry_points={
        'gui_scripts': [
            'nifixer = nifixer.__main__:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ]
)
