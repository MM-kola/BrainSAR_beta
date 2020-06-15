# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(382, 281)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.radioButton = QtWidgets.QRadioButton(dialog)
        self.radioButton.setGeometry(QtCore.QRect(30, 60, 89, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(30, 90, 89, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(QtCore.QRect(30, 30, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 120, 101, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 180, 91, 16))
        self.label_3.setObjectName("label_3")
        self.ipaddr = QtWidgets.QLineEdit(dialog)
        self.ipaddr.setGeometry(QtCore.QRect(30, 150, 161, 20))
        self.ipaddr.setObjectName("ipaddr")
        self.lineEdit_2 = QtWidgets.QLineEdit(dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(30, 210, 161, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.hz = QtWidgets.QLineEdit(dialog)
        self.hz.setGeometry(QtCore.QRect(210, 60, 113, 20))
        self.hz.setObjectName("hz")
        self.label_4 = QtWidgets.QLabel(dialog)
        self.label_4.setGeometry(QtCore.QRect(210, 30, 101, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(dialog)
        self.label_5.setGeometry(QtCore.QRect(210, 100, 101, 16))
        self.label_5.setObjectName("label_5")
        self.eeglen = QtWidgets.QLineEdit(dialog)
        self.eeglen.setGeometry(QtCore.QRect(210, 130, 113, 20))
        self.eeglen.setObjectName("eeglen")

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Dialog"))
        self.radioButton.setText(_translate("dialog", "离线实验"))
        self.radioButton_2.setText(_translate("dialog", "在线判读"))
        self.label.setText(_translate("dialog", "模式选择"))
        self.label_2.setText(_translate("dialog", "输入刺激端IP地址"))
        self.label_3.setText(_translate("dialog", "输入端口号"))
        self.label_4.setText(_translate("dialog", "设置刺激呈现频率"))
        self.label_5.setText(_translate("dialog", "设置捕捉特征时长"))
