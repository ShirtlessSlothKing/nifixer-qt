#!/usr/bin/env python

import re
import os
import shutil
import tempfile
import struct
from   pyffi.formats.nif  import NifFormat

# returns true if the file extension points to a nif 
def is_nif_ext(filename):
    return filename.lower().endswith('.nif')

# returns true if the file extension points to a valid texture file 
def is_tex_ext(filename):
    return filename.lower().endswith(('.tga', '.dds'))

# reads a nif file and modifies it to be compatible with openmw 
def nif_clean(filename):
    file_changed = False
    try:
        if __debug__:
            print('processing nif ', filename)
        stream = open(filename, 'rb')
        data = NifFormat.Data()
        data.read(stream)
        for block in data.blocks:
            # Remove NiTextureEffect blocks for various reasons (most common are environment maps)
            if isinstance(block, NifFormat.NiTextureEffect):
                if __debug__:
                    print('Removing NiTextureEffect block from file ', filename)
                data.replace_global_node(block, None)
                file_changed = True
            # Remove NiSourceTextures for bump maps
            elif (isinstance(block, NifFormat.NiTexturingProperty) and block.has_bump_map_texture):
                if __debug__:
                    print('Removing normal map and reference from file ', filename)
                source_block = block.bump_map_texture.source
                # sometimes source block is empty for some reason, so this check is necassary 
                if source_block is not None:
                    bump_map_file = str(source_block.file_name)
                    data.replace_global_node(source_block, None)
                block.has_bump_map_texture = False
                file_changed = True
        stream.close()

        # No need to write file if we did nothing :)
        if file_changed:
            if __debug__:
                print('Attempting to write file ', filename)
            # write to temporary file and move to better avoid any corruption while writing
            output = tempfile.NamedTemporaryFile(prefix='nifixer_',delete=False)
            data.write(output)
            output.close()
            shutil.move(output.name,filename)
            if __debug__:
                print('Wrote file ', output.name, '  =>>  ', filename)
            
    except Exception as e:
        print('Error reading file: ', e)
        return False
    
    return True
