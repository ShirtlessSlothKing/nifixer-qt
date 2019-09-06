# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

exclude = [
   'PySide2.QtWebEngine', 
   'PySide2.QtWebEngineCore', 
   'PySide2.QtWebEngineWidgets', 
   'PySide2.QtNetwork', 
   'PySide2.QtQml'
]

data = [
    ('external/pyffi/VERSION', 'pyffi'),    
    ('external/pyffi/formats/bsa/bsa.xml', 'pyffi/formats/bsa'), 
    ('external/pyffi/formats/dds/dds.xml', 'pyffi/formats/dds'), 
    ('external/pyffi/formats/nif/nifxml/nif.xml', 'pyffi/formats/nif/nifxml/')
]

a = Analysis(['nifixer/__main__.py'],
             pathex=['/home/cody/projects/nifixer-qt'],
             binaries=[],
             datas=data,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=exclude,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.binaries = a.binaries - TOC([
  ('libstdc++.so.6', None, None),
  ('libgtk-3.so.0', None, None),
  ('libgtk-3.so.0', None, None),
  ('libQt5Quick.so.5', None, None),
  ('libQt5Qml.so.5', None, None),
  ('libcrypto.so.1.1', None, None),
  ('libQt5Network.so.5', None, None),
  ('libQt5XcbQpa.so.5', None, None),
  ('libQt5VirtualKeyboard.so.5', None, None),
  ('libgio-2.0.so.0', None, None),
  ('libglib-2.0.so.0', None, None),
  ('libgcrypt.so.20', None, None),
  ('libcrypto-1_1.dll', None, None)
])

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='nifixer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          console=False , icon='resources/icons/app.ico')
