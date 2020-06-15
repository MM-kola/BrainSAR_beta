import sys
import random
import time
from PIL import Image
import numpy
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QImage, QColor
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
Image.MAX_IMAGE_PIXELS = None


class FirstMainWin(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()
        self.draw = QColor()
        self.draw.setBlue(53)
        self.draw.setGreen(53)
        self.draw.setRed(234)
        self.draw.setAlpha(0)
        self.initUI()
        # 设置窗口的尺寸
        self.setWindowTitle('显示图像')

    def initUI(self):
        self.resize(800, 300)
        self.move(300, 200)
        self.lbl = QLabel(self)
        # img = plt.imread('G:\BrainSAR_Beta\SAR图片\show.jpg')
        # print(img.shape)
        self.pil_image = QImage('G:\BrainSAR_Beta\SAR图片\show.jpg')
        self.pil_image.convertTo(QImage.Format_RGB888)
        print(self.pil_image.size(), self.pil_image.height())
        # self.pil_image = Image.open("G:\BrainSAR_Beta\SAR图片\show.jpg")
        self.initshow()
        # self.show()
        self.timer1 = QtCore.QTimer(self)  # 定义定时器，用于控制显示视频的帧率
        self.timer1.timeout.connect(self.fcku)
        self.timer1.start()
        self.plotdots()


    def fcku(self):
        pil_image = self.m_resize(self.width(), self.height(), self.pil_image)
        pixmap = QPixmap.fromImage(pil_image)
        self.lbl.resize(pil_image.width(), pil_image.height())
        self.lbl.setPixmap(pixmap)


    def m_resize(self, w_box, h_box, pil_image):  # 参数是：要适应的窗口宽、高、Image.open后的图片
        w, h = pil_image.width(), pil_image.height()  # 获取图像的原始大小
        f1 = 1.0 * w_box/w
        f2 = 1.0 * h_box/h

        factor = min([f1, f2])

        width = int(w * factor)

        height = int(h * factor)

        return pil_image.scaled(width, height)

    # 用来描点展示，输入原图对应的像素点，plot到pixmap中
    def plotdots(self):
        for show in range(1, 5):
            x = random.randint(1500, 8000)
            y = random.randint(1500, 9000)
            for i in range(x-1000, x+1000):  # 遍历所有长度的点
                for j in range(y-1000, y+1000):  # 遍历所有宽度的点
                    self.pil_image.setPixelColor(i, j, self.draw)

    def initshow(self):
        pil_image = self.m_resize(self.width(), self.height(), self.pil_image)
        pixmap = QPixmap.fromImage(pil_image)
        self.lbl.resize(pil_image.width(), pil_image.height())
        self.lbl.setPixmap(pixmap)


def test():
    img = Image.open("G:\BrainSAR_Beta\SAR图片\sb.jpg")  # 读取系统的内照片
    print(img.size)  # 打印图片大小
    print(img.getpixel((4, 4)))
    width = img.size[0]  # 长度
    height = img.size[1]  # 宽度
    img = img.convert("RGB")
    for i in range(0, 1000):  # 遍历所有长度的点
        for j in range(0, 1000):  # 遍历所有宽度的点
            data = (img.getpixel((i, j)))  # 打印该图片的所有点
            print("打印每个像素点的颜色RGBA的值(r,g,b,alpha):", data)  # 打印每个像素点的颜色RGBA的值(r,g,b,alpha)
            # if (data[0] > 100 or data[1] > 100 or data[2] > 100):  # RGBA的r值大于170，并且g值大于170,并且b值大于170
            img.putpixel((i, j), (234, 53, 57, 10))  # 则这些像素点的颜色改成大红色
    img = img.convert("RGB")  # 把图片强制转成RGB
    img.save("sb.jpg")#保存修改像素点后的图片

def testQImage():
    img = QImage('G:\BrainSAR_Beta\SAR图片\show.jpg').rgbSwapped()
    print(img.width())  # 打印图片大小
    print(img.height())  # 打印图片大小
    print(img.pixel(2, 2))
    for i in range(1000, 2000):  # 遍历所有长度的点
        for j in range(1000, 2000):  # 遍历所有宽度的点
            c = img.pixel(i, j)
            colors = QColor(c).getRgb()
            print("(%s,%s) = %s" % (i, j, colors))
            # QColor.HexArgb
            # print(colors.HexArgb)
            img.setPixel(i, j, 4293539385)  # 则这些像素点的颜色改成大红色
    # img = img.convert("RGB")
    # for i in range(0, 1000):  # 遍历所有长度的点
    #     for j in range(0, 1000):  # 遍历所有宽度的点
    #         data = (img.getpixel((i, j)))  # 打印该图片的所有点
    #         print("打印每个像素点的颜色RGBA的值(r,g,b,alpha):", data)  # 打印每个像素点的颜色RGBA的值(r,g,b,alpha)
    #         # if (data[0] > 100 or data[1] > 100 or data[2] > 100):  # RGBA的r值大于170，并且g值大于170,并且b值大于170
    #         img.putpixel((i, j), (234, 53, 57, 10))  # 则这些像素点的颜色改成大红色
    # img = img.convert("RGB")  # 把图片强制转成RGB
    img.save("QImage.jpg")

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('G:\BrainSAR_Beta\icon.jpg'))
    main = FirstMainWin()
    main.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    # testQImage()
    main()
    # img = QImage('G:\BrainSAR_Beta\SAR图片\show.jpg')
    # img.convertTo(QImage.Format_RGB888)
    # draw = QColor()
    # draw.setBlue(53)
    # draw.setGreen(53)
    # draw.setRed(234)
    # draw.setAlpha(10)
    #
    # for i in range(1000, 2000):  # 遍历所有长度的点
    #     for j in range(1000, 2000):  # 遍历所有宽度的点
    #         img.setPixelColor(i, j, draw)
    #         print("???")
    #
    # img.save("cnm.jpg")



