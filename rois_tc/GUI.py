
import sys
import os

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QGridLayout, QLabel,
                             QSpinBox, QComboBox, QDialogButtonBox, QCheckBox,
                             QApplication, QFileDialog, QLineEdit, QListWidget,
                             QPushButton, QErrorMessage, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSlot
import numpy as np
import pycartool

from .utils import transform_svds


class RoisTcToolbox(QDialog):
    def __init__(self, parent=None, QApplication=None):
        super().__init__(parent)
        self.setWindowTitle(' Compute Rois time course')
        vbox = QVBoxLayout(self)
        grid = QGridLayout()
        # Init
        self.fname_rois = None
        self.rois = None
        self.ris_files = None
        self.output_directory = None
        self.scalings = {"None": "none",
                         "Eigenvalue": "Eigenvalues"}
        # Ris files
        grid.addWidget(QLabel('Ris files:'), 0, 0)
        self.QListWidget_ris = QListWidget()
        grid.addWidget(self.QListWidget_ris, 0, 1)
        self.QPushButton_ris = QPushButton('Open')
        self.QPushButton_ris.clicked.connect(self.open_ris)
        grid.addWidget(self.QPushButton_ris, 0, 3)
        # ROI file
        grid.addWidget(QLabel('ROI file:'), 1, 0)
        self.QLineEdit_rois = QLineEdit()
        grid.addWidget(self.QLineEdit_rois, 1, 1)
        self.QPushButton_rois = QPushButton('Open')
        self.QPushButton_rois.clicked.connect(self.open_rois)
        grid.addWidget(self.QPushButton_rois, 1, 3)
        # scaling
        grid.addWidget(QLabel('Scaling:'), 4, 0)
        self.QComboBox_scaling = QComboBox()
        self.QComboBox_scaling.addItems(self.scalings.keys())
        self.QComboBox_scaling.setCurrentText('None')
        grid.addWidget(self.QComboBox_scaling, 4, 1)
        # outputdir
        grid.addWidget(QLabel('Output directory:'), 5, 0)
        self.QLineEdit_output_dir = QLineEdit()
        self.output_directory = os.getcwd()
        self.QLineEdit_output_dir.setText(self.output_directory)
        grid.addWidget(self.QLineEdit_output_dir, 5, 1)
        self.QPushButton_open_output_dir = QPushButton('Open')
        self.QPushButton_open_output_dir.clicked.connect(
                                                   self.open_output_directory)
        grid.addWidget(self.QPushButton_open_output_dir, 5, 3)
        # run
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok |
                                          QDialogButtonBox.Cancel)
        grid.addWidget(self.buttonbox, 6, 1, 1, 4)
        self.buttonbox.accepted.connect(self.run)
        self.buttonbox.rejected.connect(self.reject)
        # self.buttonbox.setEnabled(False)

        vbox.addLayout(grid)

    def open_ris(self):
        filter = "RIS (*.ris)"
        names, _ = QFileDialog.getOpenFileNames(self, "Open RIS files",
                                                filter=filter)
        self.ris_files = names
        self.QListWidget_ris.clear()
        self.QListWidget_ris.insertItems(0, self.ris_files)
        self.data_changed()
        return()

    def open_rois(self):
        filter = "ROIs(*.rois)"
        fname, _ = QFileDialog.getOpenFileName(self,
                                               'Open ROI',
                                               filter=filter)
        if fname:
            self.fname_rois = fname
            try:
                with open(self.fname_rois) as f:
                    self.rois = pycartool.regions_of_interest.read_roi(self.fname_rois)
            except Exception as e:
                QApplication.restoreOverrideCursor()
                self.QErrorMessage = QErrorMessage()
                self.QErrorMessage.showMessage(str(e))
        else:
            self.fname_rois = None
            self.rois = None
        self.QLineEdit_rois.setText(self.fname_rois)
        self.data_changed()
        return()

    def open_output_directory(self):
        dirname = QFileDialog.getExistingDirectory(self, 'Output directory')
        if dirname:
            self.output_directory = dirname
        else:
            self.output_directory = None
        self.QLineEdit_output_dir.setText(self.output_directory)
        self.data_changed()
        return()

    def data_changed(self):
        if any(x is None for x in [self.rois, self.fname_rois,
                                   self.ris_files,
                                   self.output_directory]):
            self.buttonbox.setEnabled(False)
        else:
            self.buttonbox.setEnabled(True)
        return()

    def run(self):
        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            transform_svds(self.ris_files,
                           self.rois,
                           self.QComboBox_scaling.currentText(),
                           self.output_directory)
            QApplication.restoreOverrideCursor()
            self.QMessageBox_finnish = QMessageBox()
            self.QMessageBox_finnish.setWindowTitle("Finished")
            self.QMessageBox_finnish.setText("Done.")
            self.QMessageBox_finnish.exec_()
        except Exception as e:
            QApplication.restoreOverrideCursor()
            self.QErrorMessage = QErrorMessage()
            self.QErrorMessage.showMessage(str(e))
