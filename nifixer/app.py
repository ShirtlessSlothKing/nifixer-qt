#!/usr/bin/env python

import sys
import os
import shutil
import nifixer.settings 
from PySide2.QtGui              import QColor
from PySide2.QtGui              import QBrush
from PySide2.QtGui              import QStandardItem
from PySide2.QtGui              import QIcon
from PySide2.QtWidgets          import QApplication
from PySide2.QtWidgets          import QMainWindow
from PySide2.QtWidgets          import QTreeWidgetItem
from PySide2.QtWidgets          import QFileDialog
from PySide2.QtWidgets          import QTreeView
from PySide2.QtWidgets          import QStyle
from PySide2.QtWidgets          import QMessageBox
from nifixer.worker             import Worker
from nifixer.itemmodel          import Options
from nifixer.itemmodel          import TreeItemModel
from nifixer.ui                 import resources_rc
from nifixer.ui                 import mainwindow_ui
from nifixer.util               import is_nif_ext, is_tex_ext


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":icons/app.png"))
        self.setWindowTitle(self.tr('Nifixer'))
        self.opts = Options()

        # initialize options to correct values
        self.on_option_changed()
        
        # connect signals for our options
        self.ui.opt_fixmesh.stateChanged.connect(self.on_option_changed)
        self.ui.opt_specular.stateChanged.connect(self.on_option_changed)
        self.ui.opt_normal.stateChanged.connect(self.on_option_changed)
        self.ui.item_tree.setSortingEnabled(False)
        self.ui.progress.setVisible(False)
        self.ui.total_processed_label.setVisible(False)
        self.ui.apply_btn.setEnabled(False)

        # set button icon
        self.ui.file_in_btn.setIcon(
            QApplication.style().standardIcon(QStyle.SP_DirOpenIcon))

        self.ui.action_exit.triggered.connect(self.close)
        self.ui.file_in_btn.clicked.connect(self.on_select_input_folder)
        self.ui.apply_btn.clicked.connect(self.on_apply)

        self.model = TreeItemModel(self)
        self.ui.item_tree.setModel(self.model)
        self.ui.item_tree.setColumnWidth(TreeItemModel.ORIGINAL,350)
        self.ui.item_tree.setColumnWidth(TreeItemModel.MODIFIED,350)
        # setup worker threads
        self.worker = Worker(self.opts)
        self.worker.insert_tree_item.connect(self.insert_tree_item)
        self.worker.finished.connect(self.worker_finished)
        self.worker.finished.connect(self.on_option_changed)
        self.worker.started.connect(self.worker_started)
        self.worker.update_progress.connect(lambda val: self.ui.progress.setValue(self.ui.progress.value()+val))

    # override
    def closeEvent(self, event):
        if not self.worker.isFinished() and self.worker.isRunning():
            msg = QMessageBox()
            msg.setText(self.tr('Are you sure you want to quit?'))
            msg.setInformativeText(self.tr('Files are still being worked on, are you sure you want to quit and cancel this operation?'))
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if msg.exec_() == QMessageBox.Cancel:
                return event.ignore()
               
        self.worker.force_close = True
        self.worker.wait()
        print('Leaving Vvardenfell...')
        return event.accept()

    def insert_tree_item(self, path, type_str, modified, good):
        self.model.insert(path, type_str, modified,
                          Options.BRUSH_GOOD if good else Options.BRUSH_BAD)

    def worker_started(self):
        # count files we will be working on for progress bar 
        max_value=0
        fix_texture = self.opts.tex_specular or self.opts.tex_normal
        for root, dirs, files in os.walk(self.opts.input_folder):
            for f in files:
                if is_nif_ext(f) and self.opts.fix_nifs:
                    max_value += 1
                elif is_tex_ext(f) and fix_texture:
                    max_value += 1
                    
        # update UI
        self.model.removeRows(0, self.model.rowCount()) # clear tree 
        self.ui.apply_btn.setEnabled(False)
        self.ui.file_in_btn.setEnabled(False)
        self.ui.item_tree.setSortingEnabled(False)
        self.ui.total_processed_label.setVisible(False)
        self.ui.progress.setVisible(True)
        self.ui.progress.setMaximum(max_value)
        self.ui.progress.setValue(0)

    def worker_finished(self):
        # update our options, the class is lightweight so a copy is cheap
        self.worker.opts = self.opts

        # update UI
        self.ui.progress.setValue(self.ui.progress.maximum())
        self.ui.progress.setVisible(False)
        self.ui.file_in_btn.setEnabled(True)
        self.ui.item_tree.setSortingEnabled(True)
        self.ui.total_processed_label.setVisible(True)
        self.ui.total_processed_label.setText(self.tr('Total candidates ' + str(self.model.rowCount())))

    def on_option_changed(self):
        self.opts.fix_nifs = self.ui.opt_fixmesh.isChecked()
        self.opts.tex_specular = self.ui.opt_specular.isChecked()
        self.opts.tex_normal = self.ui.opt_normal.isChecked()

    def on_select_input_folder(self):
        tmp = QFileDialog.getExistingDirectory(
            self, self.tr('Select data folder'))
        # only set it as active folder if a file was selected
        if tmp:
            self.opts.input_folder = tmp
            self.ui.file_in_label.setText(self.opts.input_folder)
        if self.opts.input_folder:
            self.ui.apply_btn.setEnabled(True)

    def on_apply(self):
        if not self.opts.input_folder:
            return
        self.ui.progress.setValue(0)
        self.ui.progress.setVisible(True)
        self.worker.start()