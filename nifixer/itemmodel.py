#!/usr/bin/env python

from PySide2.QtCore import Qt
from PySide2.QtGui  import QColor
from PySide2.QtGui  import QBrush
from PySide2.QtGui  import QIcon
from PySide2.QtGui  import QStandardItemModel

# settings for our tree view/model 
class Options:
    TYPE_TEXTURE = 'texture'
    TYPE_MESH = 'mesh'
    BRUSH_BAD = QBrush(QColor('#e35b5b'))
    BRUSH_GOOD = QBrush(QColor('#73f0a3'))

    def __init__(self):
        self.tex_specular = False
        self.tex_normal = False
        self.input_folder = None
        self.fix_nifs = False

class TreeItemModel(QStandardItemModel):
    ORIGINAL, MODIFIED, TYPE = range(3)

    def __init__(self, tree):
        super().__init__(0, 3, tree)
        self.setHeaderData(self.ORIGINAL, Qt.Horizontal, 'Original')
        self.setHeaderData(self.TYPE, Qt.Horizontal, 'Type')
        self.setHeaderData(self.MODIFIED, Qt.Horizontal, 'Modified')
    def insert(self, path, type_ref, modified, brush=None):
        self.insertRow(0)
        self.setData(self.index(0, self.ORIGINAL), path)
        self.setData(self.index(0, self.TYPE), self.tr(str(type_ref)))
        self.setData(self.index(0, self.MODIFIED), modified)
        item = self.item(0, self.TYPE)
        if type_ref == Options.TYPE_MESH:
            item.setIcon(QIcon(":icons/mesh.png"))
        else:
            item.setIcon(QIcon(":icons/texture.png"))
        if brush:
            self.setData(self.index(0, self.ORIGINAL), brush,
                         Qt.ItemDataRole.BackgroundColorRole)
            self.setData(self.index(0, self.TYPE), brush,
                         Qt.ItemDataRole.BackgroundColorRole)
            self.setData(self.index(0, self.MODIFIED), brush,
                         Qt.ItemDataRole.BackgroundColorRole)