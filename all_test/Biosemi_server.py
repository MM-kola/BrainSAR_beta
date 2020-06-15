import time as TIME
import socket
import numpy as np
from multiprocessing import Process, Queue


# 作为生产者
class Biosemi_Server:
    def __init__(self, time):
        self.IPADDR = "localhost"
        self.PORT = 8888
        self.CHANNELS = 64
        self.SAPMLES = 16
        self.SAPMLES_RATE = 2048
        self.WORDS = self.CHANNELS * self.SAPMLES
        self.LOOP = time * self.SAPMLES_RATE / self.SAPMLES
        self.BUFFERSIZE = self.WORDS * 3
        self.data_sum = np.zeros(shape=(0, 0))
        # print('初始sum', data_sum)
        # 创建tcpip客户端连接端口读取数据
        try:
            self.client = socket.socket()
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client.connect((self.IPADDR, self.PORT))  # 连接服务端
        except Exception as e:
            print('警告：', e)
        # self.queue = queue

    def start_server(self, index):
        t = Process(target=self.getdata, args=(index, ))
        t.start()

    def getdata(self):
        start = TIME.time()
        for L in range(int(self.LOOP)):
            # print("轮数：", L)
            rawdata = self.client.recv(self.BUFFERSIZE)
            rawdata = np.frombuffer(rawdata, dtype=np.uint8)
            # print(type(rawdata))
            # print(rawdata)
            rawdata = rawdata.reshape((3, self.WORDS))
            # print(rawdata.shape)
            normaldata = rawdata[2, :] * 16777216 + rawdata[1, :] * 65536 + rawdata[0, :] * 256 + 0
            # print(normaldata.shape)
            i = np.arange(self.WORDS - 1, step=self.CHANNELS)
            # print(i)
            data_struct = np.zeros(shape=(self.SAPMLES, self.CHANNELS))
            # print(data_struct.shape)
            #
            for d in range(self.CHANNELS):
                # print(normaldata[i + d].shape)
                # print(data_struct.shape)
                data_struct[:, d] = normaldata[i + d]
            # print(data_struct.T.shape)
            if L == 0:
                self.data_sum = data_struct.T
                # print(data_sum)
            else:
                self.data_sum = np.hstack((self.data_sum, data_struct.T))
            # print(data_sum.shape)
        # data = data_sum
        # cell = [0, 0]
        # cell[0] = index
        # cell[1] = data_sum
        end = TIME.time()
        print('数据推进队%f ' % (end - start))
        return self.data_sum
        # self.QUEUE.put(cell)


    def close(self):
        self.client.close()


def main(index, q):
    t1 = Biosemi_Server(0.08, q)
    t1.getdata(index)
    t1.close()


if __name__ == '__main__':
    q = Queue()
    t1 = Biosemi_Server(0.1)
    while True:
        print(t1.getdata().shape)
    t1.close()

    # for i in range(10):
    #     print(q.get()[1].shape)
