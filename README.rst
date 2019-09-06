===================================================
nifixer-qt
===================================================

This application aims to quickly fix mesh and texture 
files from the OG morrowind to properly display in 
`OpenMW <https://github.com/OpenMW/openmw#openmw>`_. So
far this application does the following:

- Fixes shiny meshes
    - removes references to bump maps (ignored by OpenMW anyways)
    - removes references to environment textures
- Attempts to correctly rename texture files so that they are recognized by OpenMW
    - specular file renamed with the `_spec` suffix 
    - normal files renamed with the `_n` suffix 

To take advantage of specular and normal maps, edit the following values (or
add them if they don't exist) in the `settings.cfg` file found `here
<https://openmw.readthedocs.io/en/latest/reference/modding/paths.html>`_.

    .. code-block:: ini

        [Shaders]
        force shaders = true
        clamp lighting = false # makes normal maps look much better!
        auto use object normal maps = true
        auto use object specular maps = true
        auto use terrain normal = true
        auto use terrain specular maps = true

Installation
__________________

- *Windows*
    - There are binaries only available for 64-bit windows 8/10

- *Arch Linux*
    - A package is provided with the source 
    
        `$ cd packages/aur`
    
        `$ makepkg`
    
        `$ makepkg -i`

Build Requirements:

- python 3.5+
- setuptools  
- pyside2

Building:

1. Clone or download the repository

    `$ git clone https://github.com/ShirtlessSlothKing/nifixer-qt.git`

2. Run setuptools

    `$ python setup.py install`

Usage
__________________
Just select the folder in the application, check all the boxes, and press go!


Disclaimer
__________________
Use at your own risk, this is in an early alpha stage and should only be used 
on a per mod basis. 