# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication


class Ui_dialog(QtWidgets.QDialog):

    def __init__(self):
        super(Ui_dialog, self).__init__()
        self.IPADDR = "169.254.51.127"
        self.IPORT = "40008"
        self.model = "null"
        self.setupUi(self)
        self.retranslateUi(self)


    def setupUi(self, dialog):

        dialog.setObjectName("dialog")
        dialog.resize(382, 281)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
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
        self.label_2.setGeometry(QtCore.QRect(170, 30, 101, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(dialog)
        self.label_3.setGeometry(QtCore.QRect(170, 110, 91, 16))
        self.label_3.setObjectName("label_3")
        self.ipaddr = QtWidgets.QLineEdit(dialog)
        self.ipaddr.setGeometry(QtCore.QRect(170, 60, 161, 20))
        self.ipaddr.setObjectName("ipaddr")
        self.iport = QtWidgets.QLineEdit(dialog)
        self.iport.setGeometry(QtCore.QRect(170, 130, 161, 21))
        self.iport.setObjectName("iport")

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)

        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "请选择Brain—SAR模式"))
        self.radioButton.setText(_translate("dialog", "离线实验"))
        self.radioButton_2.setText(_translate("dialog", "在线判读"))
        self.label.setText(_translate("dialog", "模式选择"))
        self.label_2.setText(_translate("dialog", "输入刺激端IP地址"))
        self.label_3.setText(_translate("dialog", "输入端口号"))
        self.ipaddr.setInputMask('000.000.000.000;_')
        self.ipaddr.setText(self.IPADDR)
        self.iport.setText(self.IPORT)

    def ok(self):
        global IPADDR
        global IPORT
        global MODEL
        IPADDR = self.ipaddr.text()
        IPORT = self.iport.text()
        if self.radioButton.isChecked():
            MODEL = "offline"
        if self.radioButton_2.isChecked():
            MODEL = "online"
        QCoreApplication.instance().quit()

    def cancel(self):
        sys.exit()

# class Dialog(QtWidgets.QDialog):
#     """对QDialog类重写，实现一些功能"""
#     def closeEvent(self, event):
#         """
#         重写closeEvent方法，实现dialog窗体关闭时执行一些代码
#         :param event: close()触发的事件
#         :return: None
#         """
#         reply = QtWidgets.QMessageBox.question(self,
#                                                '本程序',
#                                                "是否要退出程序？",
#                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
#                                                QtWidgets.QMessageBox.No)
#         if reply == QtWidgets.QMessageBox.Yes:
#             event.accept()
#         else:
#             event.ignore()


# GUI主函数，展现GUI
def main():
    app = QtWidgets.QApplication(sys.argv)
    DialogWindow = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(DialogWindow)
    DialogWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    global IPADDR
    global IPORT
    global MODEL
    IPADDR = "localhost"
    IPORT = 8888
    MODEL = "null"
    app = QtWidgets.QApplication(sys.argv)
    DialogWindow = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(DialogWindow)
    DialogWindow.show()
    app.exec_()
    IPORT = int(IPORT)
    print(IPADDR, IPORT, MODEL)




