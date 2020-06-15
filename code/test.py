# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BrainSAR.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import time
import shutil
import os
from PIL import Image as im
from all_test import celltest as cell
import math
from all_test.Biosemi_server import Biosemi_Server
im.MAX_IMAGE_PIXELS = None
import socket
from Biosemi_data import Biosemi_getdata
from PyQt5 import QtCore, QtGui, QtWidgets
from numpy import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from multiprocessing import Process, Queue, Pipe
from multiprocessing import Pool
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
"""选择界面"""


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
        self.label_2.setGeometry(QtCore.QRect(30, 120, 101, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 180, 91, 16))
        self.label_3.setObjectName("label_3")
        self.ipaddr = QtWidgets.QLineEdit(dialog)
        self.ipaddr.setGeometry(QtCore.QRect(30, 150, 161, 20))
        self.ipaddr.setObjectName("ipaddr")
        self.iport = QtWidgets.QLineEdit(dialog)
        self.iport.setGeometry(QtCore.QRect(30, 210, 161, 21))
        self.iport.setObjectName("lineEdit_2")
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
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)

        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "请选择BrainSAR工作模式"))
        self.radioButton.setText(_translate("dialog", "离线实验"))
        self.radioButton_2.setText(_translate("dialog", "在线判读"))
        self.label.setText(_translate("dialog", "模式选择"))
        self.label_2.setText(_translate("dialog", "输入刺激端IP地址"))
        self.label_3.setText(_translate("dialog", "输入刺激端端口号"))
        self.label_4.setText(_translate("dialog", "设置刺激呈现频率"))
        self.label_5.setText(_translate("dialog", "设置捕捉特征时长"))
        self.ipaddr.setInputMask('000.000.000.000;_')
        self.ipaddr.setText(self.IPADDR)
        self.iport.setText(self.IPORT)
        self.eeglen.setText(str(EEGLEN))
        self.hz.setText(str(RATE))

    def ok(self):
        global IPADDR
        global IPORT
        global MODEL
        global EEGLEN
        global RATE
        IPADDR = self.ipaddr.text()
        IPORT = self.iport.text()
        RATE = self.hz.text()
        EEGLEN = self.eeglen.text()
        if self.radioButton.isChecked():
            MODEL = "offline"
        if self.radioButton_2.isChecked():
            MODEL = "online"

        QCoreApplication.instance().quit()

    def cancel(self):
        sys.exit()


"""主界面"""


class Ui_test(QtWidgets.QMainWindow):

    def __init__(self, queue1, queue2, startflag, IPADDR, IPORT, RATE, EEGLEN):
        super(Ui_test, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

        # 初始化
        self.dataqueue = queue1
        self.posqueue = queue2
        self.startflag = startflag
        self.ipaddr = IPADDR
        self.iport = IPORT
        self.rate = RATE
        self.data_len = EEGLEN
        self.slicepath = ''  # 切片文件地址
        self.impath = ''  # 打开图片地址
        self.image = ''  # 图片类PIL的实例，用于标注
        self.cell_table = dict()  # 创建cell类字典，用于存储每个cell的详细信息

        self.send = SignalObj()
        self.send.sendMsg.connect(self.recogAdd)

        self.startSARFlag = False
        self.EEGdataworking = False
        self.Recogworking = False
        # 绑定信号槽slot

    def setupUi(self, test):
        test.setObjectName("test")
        test.resize(687, 494)
        self.centralwidget = QtWidgets.QWidget(test)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.modelname = QtWidgets.QLabel(self.centralwidget)
        self.modelname.setObjectName("modelname")
        self.gridLayout_2.addWidget(self.modelname, 2, 0, 1, 1)
        self.showCut = QtWidgets.QLabel(self.centralwidget)
        self.showCut.setObjectName("showCut")
        self.gridLayout_2.addWidget(self.showCut, 4, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(50, 20, 50, 20)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.open = QtWidgets.QPushButton(self.centralwidget)
        self.open.setObjectName("open")
        self.verticalLayout.addWidget(self.open)
        self.cut = QtWidgets.QPushButton(self.centralwidget)
        self.cut.setObjectName("cut")
        self.verticalLayout.addWidget(self.cut)
        self.LOAD = QtWidgets.QPushButton(self.centralwidget)
        self.LOAD.setObjectName("LOAD")
        self.verticalLayout.addWidget(self.LOAD)
        self.gridLayout_2.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.start = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.start.setFont(font)
        self.start.setObjectName("start")
        self.gridLayout_2.addWidget(self.start, 3, 0, 1, 1)
        self.log = QtWidgets.QLabel(self.centralwidget)
        self.log.setObjectName("log")
        # self.log.setPixmap(QtGui.QPixmap('G:/BrainSAR_Beta/log.jpg').scaled(self.log.width(), self.log.height()))
        self.gridLayout_2.addWidget(self.log, 0, 0, 1, 1)
        self.outputlabel = QtWidgets.QLabel(self.centralwidget)
        self.outputlabel.setObjectName("outputlabel")
        self.gridLayout_2.addWidget(self.outputlabel, 5, 0, 1, 1)
        self.showSAR = QtWidgets.QLabel(self.centralwidget)
        self.showSAR.setObjectName("showSAR")
        self.gridLayout_2.addWidget(self.showSAR, 0, 1, 6, 1)
        self.gridLayout_2.setColumnStretch(0, 2)
        self.gridLayout_2.setColumnStretch(1, 8)
        self.gridLayout_2.setRowStretch(0, 3)
        self.gridLayout_2.setRowStretch(1, 3)
        self.gridLayout_2.setRowStretch(2, 1)
        self.gridLayout_2.setRowStretch(3, 1)
        self.gridLayout_2.setRowStretch(4, 3)
        self.gridLayout_2.setRowStretch(5, 1)
        test.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(test)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 687, 23))
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
        self.openimage = QtWidgets.QAction(test)
        self.openimage.setObjectName("openimage")
        self.saveimage = QtWidgets.QAction(test)
        self.saveimage.setObjectName("saveimage")
        self.actionQuite_2 = QtWidgets.QAction(test)
        self.actionQuite_2.setObjectName("actionQuite_2")
        self.actionShow_input_SAR = QtWidgets.QAction(test)
        self.actionShow_input_SAR.setObjectName("actionShow_input_SAR")
        self.actionShow_output_SAR = QtWidgets.QAction(test)
        self.actionShow_output_SAR.setObjectName("actionShow_output_SAR")
        self.actionAbout_SAR_System = QtWidgets.QAction(test)
        self.actionAbout_SAR_System.setObjectName("actionAbout_SAR_System")
        self.menuFile.addAction(self.openimage)
        self.menuFile.addAction(self.saveimage)
        self.menuFile.addAction(self.actionQuite_2)
        self.menuView.addAction(self.actionShow_input_SAR)
        self.menuView.addAction(self.actionShow_output_SAR)
        self.menuHelp.addAction(self.actionAbout_SAR_System)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(test)
        #  函数连接
        self.timer1 = QtCore.QTimer(self)  # 定义定时器，用于控制显示视频的帧率
        self.timer1.timeout.connect(self.push)
        self.LOAD.clicked.connect(self.LOAD.click)
        # self.start.clicked.connect(self.start.click)
        self.cut.clicked.connect(lambda: self.cut_slice(500))
        self.start.clicked.connect(self.startBrainSAR)

        self.open.clicked.connect(self.openfile)
        # 菜单操作，打开文件夹，保存图像，退出系统
        self.openimage.triggered.connect(self.openfile)
        self.saveimage.triggered.connect(self.saveimage_SAR)
        # self.log.setPixmap(QtGui.QPixmap('G:\GUI_pyqt\log.jpg'))
        QtCore.QMetaObject.connectSlotsByName(test)

    def retranslateUi(self, test):
        _translate = QtCore.QCoreApplication.translate
        test.setWindowTitle(_translate("test", "BrainSAR--System"))
        self.modelname.setText(_translate("test", "modelname"))
        self.modelname.setAlignment(Qt.AlignCenter)  # 居中显示图片
        self.showCut.setText(_translate("test", "showCUT"))
        self.open.setText(_translate("test", "打开SAR图片"))
        self.cut.setText(_translate("test", "裁剪SAR图片"))
        self.showCut.setAlignment(Qt.AlignCenter)  # 居中显示图片
        self.LOAD.setText(_translate("test", "Load ML model"))
        self.start.setText(_translate("test", "START"))
        self.log.setText(_translate("test", "showlog"))
        self.log.setAlignment(Qt.AlignCenter)  # 居中显示图片
        self.log.setPixmap(QtGui.QPixmap('G:/BrainSAR_Beta/log.jpg').scaled(1.25*self.log.width(), self.log.width()))
        self.outputlabel.setText(_translate("test", "TextLabel"))
        self.outputlabel.setAlignment(Qt.AlignCenter)  # 居中显示图片
        self.showSAR.setText(_translate("test", "显示SAR图像"))
        self.showSAR.setAlignment(Qt.AlignCenter)  # 居中显示图片
        self.menuFile.setTitle(_translate("test", "File"))
        self.menuView.setTitle(_translate("test", "View"))
        self.menuSettings.setTitle(_translate("test", "Settings"))
        self.menuHelp.setTitle(_translate("test", "Help"))
        self.openimage.setText(_translate("test", "Open Image"))
        self.saveimage.setText(_translate("test", "Save Image"))
        self.actionQuite_2.setText(_translate("test", "Quite"))
        self.actionShow_input_SAR.setText(_translate("test", "Show input SAR"))
        self.actionShow_output_SAR.setText(_translate("test", "Show output SAR"))
        self.actionAbout_SAR_System.setText(_translate("test", "About  SAR System"))

    # 打开文件夹
    def openfile(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        self.impath = imgName
        self.image = im.open(self.impath)
        print(self.impath)
        W_H = self.image.size[0]/self.image.size[1]
        #
        if W_H*self.showSAR.height() <= self.showSAR.width():
            jpg = QtGui.QPixmap(imgName).scaled(W_H*self.showSAR.height(), self.showSAR.height())
        else:
            jpg = QtGui.QPixmap(imgName).scaled(self.showSAR.width(), self.showSAR.width()/W_H)
        self.showSAR.setPixmap(jpg)
        # self.showSAR.setAlignment(Qt.AlignCenter)

    # 保存识别后的SAR图像
    def saveimage_SAR(self):
        image = self.showSAR.pixmap()
        image.save('G:/BrainSAR_Beta/SAR识别/123.jpg')

    """
    BrainSAR核心程序
    """

    """三进制编码"""
    def ternary_2(self, x):
        k = x % 3
        x = int(x / 3)
        y = k * 1 + x * 10
        return y

    """制造切片"""
    def cut_slice(self, cell_line=200):
        self.cut.setEnabled(False)
        picname = os.path.splitext(os.path.split(self.impath)[1])[0]
        print(picname)
        print(os.path.exists(picname))
        if os.path.exists(picname):
            shutil.rmtree(picname)

        os.makedirs(picname)
        slicepath = str('G:/BrainSAR_Beta/') + str(picname)
        self.slicepath = slicepath
        image = im.open(self.impath)
        # image.size
        # image.save('o.png', 'png')
        # print(image.size)
        num_w = math.floor(image.size[0] / (9 * cell_line))
        num_h = math.floor(image.size[1] / (9 * cell_line))
        all_num = num_w * num_h
        # print(num_w, num_h, all_num)
        # cropped = image.crop((0, 0, cell_width, cell_height))
        # print(cropped.size)
        allindex = 0
        num = 0
        cell_table = {}
        baseliney = 10
        baselinex = 10
        for all_h in range(num_h):
            ALL_basey = all_h * 9 * cell_line + baseliney
            # print('block3循环：\r')
            for all_w in range(num_w):
                ALL_basex = all_w * 9 * cell_line + baselinex
                allindex += 1
                # block 2循环
                # print('ALL_base:', ALL_basex, ALL_basey)
                # print('block2循环：\r')
                for i in range(1, 10):
                    l2 = cell.encode(i)
                    BASE = self.ternary_2(i - 1)
                    base_posx = BASE % 10 * 3 * cell_line + ALL_basex
                    base_posy = int(BASE / 10) * cell_line + ALL_basey
                    # block 1循环
                    # print('block1循环：\r')
                    for j in range(1, 10):
                        QApplication.processEvents()
                        CELL = self.ternary_2(j - 1)
                        cell_posx = CELL % 10 * 200 + base_posx
                        cell_posy = int(CELL / 10) * 200 + base_posy
                        # print(cell_posx, cell_posy, cell_line, cell_line)
                        cropped = image.crop((cell_posx, cell_posy, cell_posx + cell_line, cell_posy + cell_line))
                        l1 = cell.encode(j)
                        code = l1 + 10 * l2
                        index_pic = 100 * allindex + code

                        imname = str(index_pic) + '.png'
                        slicepathname = slicepath + '/' + imname
                        cropped.save(slicepathname, 'png')
                        # imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
                        # self.impath = imgName
                        self.image = im.open(slicepathname)
                        print(self.impath)
                        W_H = self.image.size[0] / self.image.size[1]
                        #
                        if W_H * self.showCut.height() <= self.showCut.width():
                            jpg = QtGui.QPixmap(slicepathname).scaled(W_H * self.showCut.height(), self.showCut.height())
                        else:
                            jpg = QtGui.QPixmap(slicepathname).scaled(self.showCut.width(), self.showCut.width() / W_H)
                        self.cell_table[index_pic] = \
                            cell.Cell(cell_posx + int(cell_line/2), cell_posy + int(cell_line/2), l1, l2, jpg, 0)
                        num += 1
                        # print(allindex, self.cell_table[index_pic].pic, num)

        self.cut.setEnabled(True)
        print('end cut')

    """开始在线判读"""
    def startBrainSAR(self):
        self.start.setEnabled(False)
        # 用TCP/IP的方式告诉另一台机器开始展示图片
        s = socket.socket()
        # print(str(self.ipaddr), int(self.iport))
        s.connect((str(self.ipaddr), int(self.iport)))  # 连接服务端
        self.send.runshow("暂未产生EEG数据，请稍后...")
        while True:
            data = 'try_to_connect'
            s.send(data.encode())  # 发送数据
            recv = s.recv(256).decode()
            # print(recv)
            if recv == 'pic_addr_plz':
                s.send(self.slicepath.encode())
                break
        while True:
            recv = s.recv(256).decode()
            if recv == 'rate_plz':
                data = str(self.rate)
                s.send(data.encode())
                break
        # 展示结果
        # print('进入展示阶段')
        num = 0
        # stopflag = False
        # self.timer1.start(0.05)
        # pushprcs = Process(target=self.pushData)
        # pushprcs.start()
        while True:
            QApplication.processEvents()
            recv = s.recv(256).decode()
            # print(recv)
            if recv == 'start_eeg':
                # self.startflag.send('launch')
                s.send('pic_index'.encode())
                pic_index = s.recv(256).decode()
                pic_index = int(pic_index)
                self.startflag.send(pic_index)
            if recv == 'end':
                # stopflag = True
                # while self.dataqueue.empty() != 1:
                #     QApplication.processEvents()
                #     s.send('wait'.encode())
                # 循环self.data_len次,作为读取数据的尾处理
                for rng in range(int(self.data_len)):
                    self.startflag.send(1)
                print('我一滴也没有啦！！！')
                s.send('done'.encode())
                self.startflag.send(0)
                s.close()
                print("结束客户端")
                self.start.setEnabled(True)
                break
            # if stopflag and self.dataqueue.empty():
            #     print('我一滴也没有啦！！！')
            #     s.send('done'.encode())
            #     s.close()
            #     print("结束客户端")
            #     self.start.setEnabled(True)
            #     break
            # if recv == 'end':
            #     while True:
            #         # print('while')
            #         if self.dataqueue.empty() != 1:
            #             msg = self.dataqueue.get()
            #             # print('导出数据：', msg.shape)
            #             # self.send.runshow('识别结果： %s' % (msg.shape,))
            #             out = self.EEGNetmodel(msg)
            #             num += 1
            #             self.cell_table[pic_index].set_label(out)
            #             # print('识别结果：', out)
            #             self.showCut.setPixmap(self.cell_table[pic_index].pic)
            #             self.send.runshow('识别结果： %s' % (out,))
            #             print('图片序列：', num)
            #         if self.dataqueue.empty():
            #             print('我一滴也没没有啦！！！')
            #             s.send('done'.encode())
            #             s.close()
            #             # print('335')
            #             break
                # print('337')
                # break
            if self.dataqueue.empty() != 1:
                msg = self.dataqueue.get()
                # print('导出数据：', msg)
                # self.send.runshow('识别结果： %s' % (msg.shape,))
                out = self.EEGNetmodel(msg)
                num += 1
                self.cell_table[pic_index].set_label(out)
                # print('识别结果：', out)
                self.showCut.setPixmap(self.cell_table[pic_index].pic)
                self.send.runshow('识别结果： %s' % (out,))
                print('图片序列：', num)

        print("结束客户端")
        # self.timer1.stop()
        self.start.setEnabled(True)

    #  不是推的太慢，而是产的有阻塞

    def push(self):
        print('刷新定时器')
        p = Process(target=self.pushData)
        p.start()

    def pushData(self):
        if self.dataqueue.empty() != 1:
            print('推出数据')
            # QApplication.processEvents()
            msg = self.dataqueue.get()
            # print('导出数据：', msg.shape)
            # self.send.runshow('识别结果： %s' % (msg.shape,))
            out = self.EEGNetmodel(msg[1])
            self.cell_table[int(msg[0])].set_label(out)
            # print('识别结果：', out)
            self.showCut.setPixmap(self.cell_table[int(msg[0])].pic)
            self.send.runshow('识别结果： %s' % (out,))
            # print('图片序列：', num)

    def recogAdd(self, file_inf):
        # 添加识别结果
        self.outputlabel.setText(file_inf)

    def EEGNetmodel(self, data):
        data = data
        # print(data.shape)
        out = random.randint(0, 2)
        return out


class SignalObj(QObject):
    """
    定义一个信号的类
    """
    # 自定义一个信号,注意这个地方定义约束发送出去的参数类型,下面要一致
    sendMsg = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def runshow(self, msg):
        self.sendMsg.emit(msg)


# GUI主函数，展现GUI
def main(queue1, queue2, flag, ipaddr, iport, rate, eeglen):
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('G:\BrainSAR_Beta\icon.jpg'))
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_test(queue1=queue1, queue2=queue2, startflag=flag, IPADDR=ipaddr, IPORT=iport, RATE=rate, EEGLEN=eeglen)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# 识别出结果
def EEGdata(queue, dqueue, eegflag, gettime):
    num = 0
    print(gettime)
    eegserver = Biosemi_Server(gettime, queue)
    while True:
        # 实现功能：
        # 1、从图片展示端得到采脑电的信号，若有信号则开启一个进程采脑电
        # 2、从Biosime获取脑电数据
        # 3、再次循环等待收到采脑电信号
        index = eegflag.recv()
        if index == 0:
            print("结束尾操作：", num)
            eegserver.close()
            break
        if index > 0:
            num += 1
            print('我TM在读eeg！！！', num)
            if queue.full():
                outlist = {}
                for k in range(int(queue.qsize())):
                    x = queue.get()
                    outlist[k] = x
                    queue.put(x)
                    # print("x:", x, k)
                dqueue.put(outlist)
                queue.get()
                eegserver.start_server(index=index)
                # Biosemi_getdata(gettime, queue, index)
            else:
                # Biosemi_getdata(gettime, queue, index)
                eegserver.start_server(index=index)
            # geteegdata = Process(target=Biosemi_getdata, args=(gettime, queue, index))
            # geteegdata.start()
            # Biosemi_getdata(gettime, queue, index)


if __name__ == '__main__':
    """
    Brain—SAR主程序：
    parameters:
        global IPADDR       呈现刺激服务端ip地址
        global IPORT        呈现刺激服务端ip端口
        global MODEL        软件工作模式：在线判读，离线实验
        global EEGLEN       在线判读模式下，刺激后采样时间长度(单位：秒)
        global RATE         刺激端刺激频率
    
    function：
        1、第一个展示供用户选择的界面，选择软件工作模式，输入参数等
        2、开启双进程：
            ① 界面进程：人机交互，供用户观察识别结果
            ② Biosemi采集进程：后台等待命令采集特定时间下特定长度的脑电数据
            
    author:
        2019/11/27  yongxiang wu 
    """

    global IPADDR
    global IPORT
    global MODEL
    global EEGLEN
    global RATE
    IPADDR = "localhost"
    IPORT = 9999
    MODEL = "online"
    RATE = 5.0
    EEGLEN = 4

    """选择窗口"""
    # app = QtWidgets.QApplication(sys.argv)
    # DialogWindow = QtWidgets.QDialog()
    # ui = Ui_dialog()
    # ui.setupUi(DialogWindow)
    # DialogWindow.show()
    # app.exec_()
    # IPORT = int(IPORT)
    # RATE = float(RATE)
    # EEGLEN = float(EEGLEN)
    # # print(IPADDR, IPORT, MODEL, RATE, EEGLEN)
    # DialogWindow.close()

    """依靠参数开辟队列"""
    RAW_DATA = Queue(maxsize=EEGLEN)
    DATA_QUEUE = Queue()
    RECOG_QUEUE = Queue()
    POS_QUEUE = Queue()

    if MODEL == 'online':
        # (eegflag, show1flag) = Pipe()
        # (startflag, show0flag) = Pipe()
        (startflag, eegflag) = Pipe()
        processA = Process(target=EEGdata, args=(RAW_DATA, DATA_QUEUE, eegflag, 1.0/RATE, ))
        processA.start()
        processC = Process(target=main, args=(DATA_QUEUE, POS_QUEUE, startflag, IPADDR, IPORT, RATE, EEGLEN, ))
        processC.start()
    elif MODEL == 'offline':
        print('空')
    elif MODEL == 'null':
        print("未选择模式,请重新选择模式！！！")
    else:
        print('严重未知错误！！！')
# test code
# if __name__ == "__main__":
#     (eegflag, show1flag) = Pipe()
#     (startflag, show0flag) = Pipe()
#     # 刺激频率
#     rate = 0.6
#     processA = Process(target=EEGdata, args=(RECOG_QUEUE, eegflag, rate, ))
#     processA.start()
#     # 这个进程仅在测试时使用，正式结构使用另一台机器TCP/IP
#     processB = Process(target=sendPicture, args=(POS_QUEUE, show1flag, show0flag, ))
#     processB.start()
#
#     processC = Process(target=main, args=(RECOG_QUEUE, POS_QUEUE, startflag, ))
#     processC.start()

## 曾经的尝试过程。。
# class PEEGdata(QObject, Process):
#     sinOut = pyqtSignal(str)
#
#     def __init__(self, parent=None):
#         super(PEEGdata, self).__init__(parent)
#         # 设置工作状态与初始num数值
#         self.working = True
#         self.num = 0
#
#     def __del__(self):
#         # 线程状态改变与线程终止
#         self.working = False
#         self.wait()
#
#     def run(self, queue):
#         while self.working == True:
#             # if START == True:
#             # 获取数据
#             # for i in range(1, 100):
#             file_str = self.num
#             self.num += 1
#             # push数据
#             queue.put(file_str)
#
#             # START = False
#             # self.sleep(1)
#
# class PRecog(QProcess):
#
#     sinOut = pyqtSignal(str)
#
#     def __init__(self, parent=None):
#         super(PRecog, self).__init__(parent)
#         #设置工作状态与初始num数值
#         self.working = True
#         self.num = 0
#
#     def __del__(self):
#         #线程状态改变与线程终止
#         self.working = False
#         self.wait()
#
#     def run(self, queue):
#         while self.working == True:
#             while True:
#                 if queue.empty() > 0:
#                     self.sinOut.emit('暂未产生EEG数据，请稍后。。。')
#
#                 else:
#                     msg = queue.get()
#                     self.sinOut.emit('识别结果： %s' % (msg,))
#                 # self.sleep(1)

# 获取脑电数据，传输至DATA_QUEUE
# class EEGdata(QThread):
#
#     sinOut = pyqtSignal(str)
#
#     def __init__(self, parent=None):
#         super(EEGdata, self).__init__(parent)
#         #设置工作状态与初始num数值
#         self.working = True
#         self.num = 0
#
#     def __del__(self):
#         #线程状态改变与线程终止
#         self.working = False
#         self.wait()
#
#     def run(self):
#         while self.working == True:
#
#             if START == True:
#                 # 获取数据
#                 # for i in range(1, 100):
#                 file_str = self.num
#                 self.num += 1
#                 # push数据
#                 DATA_QUEUE.put(file_str)
#                 START = False
#             # else:
#                 # 线程休眠2秒
#                 # self.sleep()

# # 识别从DATA_QUEUE pop出的脑电数据，结果表示至testlabel
# class Recog(QThread):
#
#     sinOut = pyqtSignal(str)
#
#     def __init__(self, parent=None):
#         super(Recog, self).__init__(parent)
#         #设置工作状态与初始num数值
#         self.working = True
#         self.num = 0
#
#     def __del__(self):
#         #线程状态改变与线程终止
#         self.working = False
#         self.wait()
#
#     def run(self):
#         while self.working == True:
#             while True:
#                 if DATA_QUEUE.empty() > 0:
#                     self.sinOut.emit('暂未产生EEG数据，请稍后。。。')
#
#                 else:
#                     msg = DATA_QUEUE.get()
#                     self.sinOut.emit('识别结果： %s' % (msg,))
#                 self.sleep(1)

# # 获取脑电数据，传输至DATA_QUEUE
# class showPicture(QThread):
#
#     sinOut = pyqtSignal(str)
#
#     def __init__(self, parent=None):
#         super(showPicture, self).__init__(parent)
#         #设置工作状态与初始num数值
#         self.working = True
#         self.num = 0
#
#     def __del__(self):
#         #线程状态改变与线程终止
#         self.working = False
#         self.wait()
#
#     def run(self):
#         while self.working == True:
#
#             # TCP/IP传输
#             START = True
#             # 获取数据
#             # for i in range(1, 100):
#             file_str = self.num
#             self.num += 1
#             # push数据
#             POS_QUEUE.put(file_str)
#
#             # # 线程休眠2秒
#             self.sleep(1)
