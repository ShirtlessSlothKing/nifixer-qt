#!/usr/bin/env python

import os 
import re
import shutil
import nifixer.settings
from   PySide2.QtCore             import QThread
from   PySide2.QtCore             import Signal
from   multiprocessing.pool       import Pool
from   nifixer.util               import nif_clean, is_nif_ext, is_tex_ext
from   nifixer.itemmodel          import Options

class Worker(QThread):

    update_progress = Signal(int)
    insert_tree_item = Signal(str, str, str, bool)

    def __init__(self, options):
        QThread.__init__(self)
        self.opts = options
        self.force_close = False

    def run(self):
        if self.opts.fix_nifs:
            for root, dirs, files in os.walk(self.opts.input_folder):
                # process loose files
                files[:] = filter(lambda rel: is_nif_ext(rel), files)
                files[:] = map(lambda rel: os.path.join(root,rel), files)
                for index, ret in enumerate(nifixer.settings.pool.imap_unordered(nif_clean, files, 3)): 
                    if self.force_close:
                        nifixer.settings.pool.close()
                        nifixer.settings.pool.terminate()
                        return 
                    self.insert_tree_item.emit(files[index], Options.TYPE_MESH, ' ', ret)
                    self.update_progress.emit(1)
        # fixing texture file names is pretty fast, we can just run it synchronously 
        self.tex_clean()

    def tex_clean(self):
        
        if self.opts.input_folder == None:
            return

        regex_normal = re.compile(
            r'(^.*)((?:_nm|_nrm|_normal|_normals)(.dds|.tga$))', re.IGNORECASE)
        regex_spec = re.compile(
            r'(^.*)((?:_refl|_reflection)(.dds|.tga$))', re.IGNORECASE)

        for root, dirs, files in os.walk(self.opts.input_folder):
            for file in files:
                if self.force_close:
                    return 
                self.update_progress.emit(1)        
                if is_tex_ext(file):
                    # try and detect if the file is a normal or specular texture without too much fuss
                    # this can be wrong, but it will always detect the correct type if it is either a
                    # specular or normal texture. if it is wrong, the file name simply won't be changed
                    if regex_normal.search(file) and self.opts.tex_normal:  # is normal
                        rename = regex_normal.sub(r'\1_n\3', file)
                    elif regex_spec.search(file) and self.opts.tex_specular:  # is spec
                        rename = regex_spec.sub(r'\1_spec\3', file)
                    else:
                        continue
                    if file != rename:
                        try:
                            if __debug__:
                                print('renaming file ', os.path.join(root, file), ' => ', os.path.join(root, rename))
                            shutil.move(os.path.join(root, file),
                                     os.path.join(root, rename))
                            self.insert_tree_item.emit(os.path.join(root, file), Options.TYPE_TEXTURE,
                                                     os.path.join(root, rename), True)
                        except Exception as e:
                            print('failed renaming file, ', e)
                            self.insert_tree_item.emit(os.path.join(root, file), Options.TYPE_TEXTURE,
                                                     os.path.join(root, rename), False)