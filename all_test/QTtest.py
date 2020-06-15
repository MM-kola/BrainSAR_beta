# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BrainSAR.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Ui_test(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_test, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)


    def setupUi(self, test):
        test.setObjectName("test")
        test.resize(834, 595)
        self.centralwidget = QtWidgets.QWidget(test)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 60, 149, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 20, 149, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 100, 149, 23))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 20, 621, 501))
        self.label.setObjectName("label")
        test.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(test)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 834, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        test.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(test)
        self.statusbar.setObjectName("statusbar")
        test.setStatusBar(self.statusbar)
        self.actionSave_Image = QtWidgets.QAction(test)
        self.actionSave_Image.setObjectName("actionSave_Image")
        self.actionQuite = QtWidgets.QAction(test)
        self.actionQuite.setObjectName("actionQuite")
        self.actionQuite_2 = QtWidgets.QAction(test)
        self.actionQuite_2.setObjectName("actionQuite_2")
        self.menuFile.addAction(self.actionSave_Image)
        self.menuFile.addAction(self.actionQuite)
        self.menuFile.addAction(self.actionQuite_2)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(test)

        # 菜单操作，打开文件夹，保存图像，退出系统
        self.actionSave_Image.triggered.connect(self.openfile)
        self.actionQuite_2.triggered.connect(self.saveimgae)

        QtCore.QMetaObject.connectSlotsByName(test)

    def retranslateUi(self, test):
        _translate = QtCore.QCoreApplication.translate
        test.setWindowTitle(_translate("test", "MainWindow"))
        self.pushButton_3.setText(_translate("test", "打开SAR图片"))
        self.pushButton_2.setText(_translate("test", "裁剪SAR图片"))
        self.pushButton.setText(_translate("test", "PushButton"))
        self.label.setText(_translate("test", "显示SAR图像"))
        self.menuFile.setTitle(_translate("test", "File"))
        self.menuView.setTitle(_translate("test", "View"))
        self.menuSettings.setTitle(_translate("test", "Settings"))
        self.menuHelp.setTitle(_translate("test", "Help"))
        self.actionSave_Image.setText(_translate("test", "Open Image"))
        self.actionQuite.setText(_translate("test", "Save Image"))
        self.actionQuite_2.setText(_translate("test", "Quite"))

    # 打开文件夹
    def openfile(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)

    # 保存识别后的SAR图像
    def saveimgae(self):
        image = self.label.pixmap()
        image.save('G:/GUI_pyqt/SAR识别/123.jpg')



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_test()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
