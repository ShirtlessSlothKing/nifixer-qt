#!/usr/bin/env python

import sys
import os 
import argparse
import multiprocessing
import nifixer.settings
from   nifixer.app              import MainWindow, Options
from   nifixer.worker           import Worker
from   multiprocessing.pool     import Pool
from   PySide2.QtWidgets        import QApplication

# this call is necassary for windows, does nothing on any other OS 
multiprocessing.freeze_support()
# we must initialize our pool in main to avoid issues with multiprocessing in windows 
nifixer.settings.pool = Pool(os.cpu_count())
     
opts = Options()
parser = argparse.ArgumentParser(description='Configure and install application', usage=('nifixer [options] FILE,DIRS...'))
parser.add_argument('-f','--nif', action='store_true', help='fix nifs',dest='fix_nifs', default=False)
parser.add_argument('-n','--normal', action='store_true', help='rename normal textures',dest='tex_normal', default=False)
parser.add_argument('-s','--specular', action='store_true', help='rename specular textures',dest='tex_specular', default=False)
parser.add_argument('files', nargs='+')
    
# headless mode is implied if one or more argument is passed
if len(sys.argv) >= 2:
    args = parser.parse_args()
    opts.tex_normal = args.tex_normal
    opts.tex_specular = args.tex_specular
    opts.fix_nifs = args.fix_nifs
    tworker = Worker(opts)
    for f in args.files:
        if os.path.isdir(f) or os.path.isfile(f):
            opts.input_folder = f
            tworker.opts = opts
            if __debug__:
                print('processing ', f)
            tworker.start()
            tworker.wait()
        else:
            print('no such files or directory ', f)
else:
    a = QApplication(sys.argv)
    a.setApplicationName('nifixer')
    a.setApplicationVersion(nifixer.settings.__version__)

    w = MainWindow().show()
    sys.exit(a.exec_())        