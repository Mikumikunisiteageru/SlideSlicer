# 20230331

import os
import sys
import numpy as np
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(150, 50)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.recordButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.recordButton.sizePolicy().hasHeightForWidth())
        self.recordButton.setSizePolicy(sizePolicy)
        self.recordButton.setMinimumSize(QtCore.QSize(50, 50))
        self.recordButton.setObjectName("recordButton")
        self.horizontalLayout.addWidget(self.recordButton)
        self.helpButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.helpButton.sizePolicy().hasHeightForWidth())
        self.helpButton.setSizePolicy(sizePolicy)
        self.helpButton.setMinimumSize(QtCore.QSize(50, 50))
        self.helpButton.setObjectName("helpButton")
        self.horizontalLayout.addWidget(self.helpButton)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closeButton.sizePolicy().hasHeightForWidth())
        self.closeButton.setSizePolicy(sizePolicy)
        self.closeButton.setMinimumSize(QtCore.QSize(50, 50))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SlideSlicer"))
        self.recordButton.setText(_translate("MainWindow", "="))
        self.helpButton.setText(_translate("MainWindow", "?"))
        self.closeButton.setText(_translate("MainWindow", "x"))

def readSettings(ui):
    ui.settings = QtCore.QSettings("SlideSlicer_config.ini", QtCore.QSettings.IniFormat)
    helpStr = "*** Edit this file to configure settings and restart when necessary ***"
    ui.settings.setValue("HELP/help", helpStr)
    ui.settings.setValue("ABOUT/name", "SlideSlicer")
    ui.settings.setValue("ABOUT/version", "0.1.0")
    ui.settings.setValue("ABOUT/repository", "https://github.com/Mikumikunisiteageru/SlideSlicer")
    ui.path = ui.settings.value("OUTPUT/path")
    if not ui.path or not os.path.isdir(ui.path):
        ui.path = os.path.join(os.getcwd(), "SlideSlicer_output")
        if not os.path.isdir(ui.path):
            os.mkdir(ui.path)
        ui.settings.setValue("OUTPUT/path", ui.path)
    try:
        string = ui.settings.value("SCREENSHOT/everyxmillisecond")
        ui.everyXMillisecond = int(string)
        assert ui.everyXMillisecond > 999
    except:
        ui.everyXMillisecond = 2000
        ui.settings.setValue("SCREENSHOT/everyxmillisecond", ui.everyXMillisecond)
    try:
        string = ui.settings.value("PAGEDETECTION/medium")
        ui.medium = int(string)
        assert 1 <= ui.medium <= 254
    except:
        ui.medium = 128
        ui.settings.setValue("PAGEDETECTION/medium", ui.medium)
    try:
        string = ui.settings.value("PAGEDETECTION/rangesize")
        ui.rangesize = int(string)
        assert 1 <= ui.rangesize <= 254
    except:
        ui.rangesize = 154
        ui.settings.setValue("PAGEDETECTION/rangesize", ui.rangesize)
    try:
        string = ui.settings.value("PAGEDETECTION/threshold")
        ui.threshold = float(string)
        assert 0.0 <= ui.threshold <= 1.0
    except:
        ui.threshold = 0.001
        ui.settings.setValue("PAGEDETECTION/threshold", ui.threshold)
    try:
        position = ui.settings.value("WINDOW/position")
        assert isinstance(position, QtCore.QPoint)
        ui.position = position
    except:
        ui.position = QtCore.QPoint(200, 200)

def screenshot(ui):
    return ui.screen.grabWindow(0).toImage()

def recordClick(ui):
    if ui.recording:
        ui.recordButton.setText("=")
        ui.recording = False
    else:
        ui.recordButton.setText("@")
        ui.recording = True
        periodStart(ui)

def periodStart(ui):
    if ui.recording:
        img = screenshot(ui)
        height = img.height()
        width = img.width()
        depth = img.depth() // 8
        length = height * width * depth
        buffer = img.constBits()
        buffer.setsize(length)
        imgFlattened = np.ndarray(shape=(length,), buffer=buffer, dtype=np.uint8).copy()
        if not isinstance(ui.oldImgFlattened, type(None)):
            condition1 = np.logical_xor(imgFlattened > ui.medium, ui.oldImgFlattened > ui.medium)
            condition2 = np.abs(imgFlattened - ui.oldImgFlattened) > ui.rangesize
            newPage = np.mean(np.logical_and(condition1, condition2)) > ui.threshold
        else:
            newPage = True
        if newPage:
            img.save(os.path.join(ui.path, datetime.now().strftime("%Y%m%d_%H%M%S.png")))
            ui.oldImgFlattened = imgFlattened
            ui.alpha = 255
        else:
            ui.alpha = ui.alpha * 2 // 5
    else:
        ui.alpha = ui.alpha * 2 // 5
    ui.centralwidget.setStyleSheet(f"background-color: rgba(57, 197, 187, {ui.alpha})")
    ui.timer.start(ui.everyXMillisecond)

def terminate(ui):
    ui.settings.setValue("WINDOW/position", mainWindow.pos())
    sys.exit()
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    mainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SubWindow)
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    readSettings(ui)
    mainWindow.move(ui.position)
    ui.alpha = 0
    ui.screen = QtWidgets.QApplication.primaryScreen()
    ui.timer = QtCore.QTimer()
    ui.timer.timeout.connect(lambda: periodStart(ui))
    ui.recording = False
    periodStart(ui)
    ui.oldImgFlattened = None
    ui.recordButton.clicked.connect(lambda: recordClick(ui))
    ui.helpButton.clicked.connect(lambda: os.system("start SlideSlicer_config.ini"))
    ui.closeButton.clicked.connect(lambda: terminate(ui))
    mainWindow.show()
    sys.exit(app.exec_())
