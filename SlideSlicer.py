# 20230331

import os
import sys
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

def readSettings():
    settings = QtCore.QSettings("SlideSlicer_config.ini", QtCore.QSettings.IniFormat)
    settings.setValue("ABOUT/name", "SlideSlicer")
    settings.setValue("ABOUT/version", "0.1.0")
    settings.setValue("ABOUT/repository", "https://github.com/Mikumikunisiteageru/SlideSlicer")        
    path = settings.value("OUTPUT/path")
    if not path or not os.path.isdir(path):
        path = os.path.join(os.getcwd(), "SlideSlicer_output")
        if not os.path.isdir(path):
            os.mkdir(path)
        settings.setValue("OUTPUT/path", path)
    os.chdir(path)

if __name__ == '__main__':
    readSettings()
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    mainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SubWindow)
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    ui.closeButton.clicked.connect(sys.exit)
    mainWindow.show()
    sys.exit(app.exec_())
