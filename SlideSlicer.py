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
    settings = QtCore.QSettings("SlideSlicer_config.ini", QtCore.QSettings.IniFormat)
    helpStr = "*** Edit this file to configure settings and restart when necessary ***"
    settings.setValue("HELP/help", helpStr)
    settings.setValue("ABOUT/name", "SlideSlicer")
    settings.setValue("ABOUT/version", "0.1.0")
    settings.setValue("ABOUT/repository", "https://github.com/Mikumikunisiteageru/SlideSlicer")
    ui.path = settings.value("OUTPUT/path")
    if not ui.path or not os.path.isdir(ui.path):
        ui.path = os.path.join(os.getcwd(), "SlideSlicer_output")
        if not os.path.isdir(ui.path):
            os.mkdir(ui.path)
        settings.setValue("OUTPUT/path", ui.path)
    try:
        string = settings.value("SCREENSHOT/everymillisecond")
        ui.s = int(string)
        assert ui.s > 999
    except:
        ui.s = 2000
        settings.setValue("SCREENSHOT/everymillisecond", ui.s)

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
    img = screenshot(ui)
    img.save(os.path.join(ui.path, datetime.now().strftime("%Y%m%d_%H%M%S.png")))
    # print(os.path.join(ui.path, datetime.now().strftime("%Y%m%d_%H%M%S.png")))
    ui.timer.start(ui.s)

def periodRefresh(ui):
    if ui.recording:
        periodStart(ui)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    mainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SubWindow)
    ui = Ui_MainWindow()
    readSettings(ui)
    ui.screen = QtWidgets.QApplication.primaryScreen()
    ui.timer = QtCore.QTimer()
    ui.timer.timeout.connect(lambda: periodRefresh(ui))
    ui.recording = False
    ui.setupUi(mainWindow)
    ui.recordButton.clicked.connect(lambda: recordClick(ui))
    ui.helpButton.clicked.connect(lambda: os.system("start SlideSlicer_config.ini"))
    ui.closeButton.clicked.connect(sys.exit)
    mainWindow.show()
    sys.exit(app.exec_())
