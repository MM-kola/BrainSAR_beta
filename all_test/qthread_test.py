import sys

import queue
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


DATA_QUEUE = queue.Queue(100)

class MainWidget(QWidget):

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        #设置标题
        self.setWindowTitle('QThread多线程例子')

        #实例化多线程对象
        self.thread1 = Worker1()
        self.thread2 = Worker2()

        #实例化列表控件与按钮控件
        self.listFile = QListWidget()
        self.btnStart = QPushButton('开始')

        #把控件放置在栅格布局中
        layout = QGridLayout(self)
        layout.addWidget(self.listFile, 0, 0, 1, 2)
        layout.addWidget(self.btnStart, 1, 1)

        #信号与槽函数的连接
        self.btnStart.clicked.connect(self.slotStart)

        # self.thread1.sinOut.connect(self.slotAdd)
        self.thread2.sinOut.connect(self.slotAdd)

    def slotAdd(self, file_inf):
        #向列表控件中添加条目
        self.listFile.addItem(file_inf)

    def slotStart(self):

        #开始按钮不可点击，线程开始
        self.btnStart.setEnabled(False)
        self.thread1.start()
        self.thread2.start()




class Worker1(QThread):

    sinOut = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Worker1, self).__init__(parent)
        #设置工作状态与初始num数值
        self.working = True
        self.num = 0

    def __del__(self):
        #线程状态改变与线程终止
        self.working = False
        self.wait()

    def run(self):

        while self.working == True:

            #获取文本
            file_str = 'File index{0}'.format(self.num)
            self.num += 1


            # 发射信号
            # self.sinOut.emit(file_str)
            DATA_QUEUE.put(file_str)

            # 线程休眠2秒
            self.sleep(2)

class Worker2(QThread):

    sinOut = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Worker2, self).__init__(parent)
        #设置工作状态与初始num数值
        self.working = True
        self.num = 0

    def __del__(self):
        #线程状态改变与线程终止
        self.working = False
        self.wait()

    def run(self):
        while self.working == True:
            #获取文本
            file_str = 'File index{0}'.format(self.num)
            self.num += 1

            # 发射信号
            # self.sinOut.emit(file_str)
            while True:
                if DATA_QUEUE.empty() > 0:
                    self.sinOut.emit('queue is empty %d' % (DATA_QUEUE.qsize()))
                else:
                    msg = DATA_QUEUE.get()
                    self.sinOut.emit('get msg %s' % (msg,))

                 # 线程休眠2秒
                self.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWidget()
    demo.show()
    sys.exit(app.exec_())

