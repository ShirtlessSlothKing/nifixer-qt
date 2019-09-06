# freeze the application, this will create a platform-dependent binary 

import os
import sys
import shutil
import subprocess
import argparse
import platform
import pyside2uic

try:  
    # relative root path to place our frozen app files 
    target_path = platform.system().lower() + '_' + platform.machine().lower()
    dist_path=os.path.join('dist',target_path)
    work_path=os.path.join('build',target_path)
    proc_args = [
            'pyinstaller',
            'nifixer.spec',
            '--onefile',
            '--distpath', dist_path,
            '--workpath', work_path
        ]
    # run pyinstaller to freeze app 
    subprocess.run(proc_args, check=True)
except Exception as e:
    print('failed freezing app: ', e)
    sys.exit(1)

try:
    # copy our license file to dist/ folder manually 
    shutil.copyfile('LICENSE.rst', os.path.join(dist_path,'nifixer','LICENSE.rst'))
except Exception as e:
    print('failed copying license file: ', e)
    sys.exit(1)