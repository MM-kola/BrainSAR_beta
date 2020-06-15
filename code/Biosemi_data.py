import socket
import numpy as np
from multiprocessing import Process, Queue
import time as TIME
DATA_QUEUE = Queue(1000)


def Biosemi_getdata(time, QUEUE, index):
    print('启动biosemi')
    start = TIME.time()
    # 设定主机、端口与常量
    IPADDR = "localhost"
    PORT = 8888
    CHANNELS = 64
    SAPMLES = 16
    SAPMLES_RATE = 2048
    WORDS = CHANNELS*SAPMLES
    LOOP = time*SAPMLES_RATE/SAPMLES
    BUFFERSIZE = WORDS*3
    data_sum = np.zeros(shape=(0, 0))
    # print('初始sum', data_sum)
    # 创建tcpip客户端连接端口读取数据
    client = socket.socket()

    # 捕获服务端连接异常，若没打开端口则提示打开ActiView
    try:
        client.connect((IPADDR, PORT))  # 连接服务端
    except Exception as e:
        print("尝试连接 ActiView 失败！！！\n请检查是否打开 ActiView 客户端\n", e)
        return
    for L in range(int(LOOP)):
        # print("轮数：", L)
        rawdata = client.recv(BUFFERSIZE)
        rawdata = np.frombuffer(rawdata, dtype=np.uint8)
        # print(type(rawdata))
        # print(rawdata)
        rawdata = rawdata.reshape((3, WORDS))
        # print(rawdata.shape)
        normaldata = rawdata[2, :]*16777216 + rawdata[1, :]*65536 + rawdata[0, :]*256 + 0
        # print(normaldata.shape)
        i = np.arange(WORDS-1, step=CHANNELS)
        # print(i)
        data_struct = np.zeros(shape=(SAPMLES, CHANNELS))
        # print(data_struct.shape)
        #
        for d in range(CHANNELS):
        # print(normaldata[i + d].shape)
        # print(data_struct.shape)
            data_struct[:, d] = normaldata[i + d]
        # print(data_struct.T.shape)
        if L == 0:
            data_sum = data_struct.T
            # print(data_sum)
        else:
            data_sum = np.hstack((data_sum, data_struct.T))
        # print(data_sum.shape)
    # data = data_sum
    cell = [0, 0]
    cell[0] = index
    cell[1] = data_sum
    QUEUE.put(cell)
    end = TIME.time()
    print('数据推进队', end-start)
    client.close()


if __name__ == '__main__':
    gettime = 0.5


    # show
    for j in range(20):
        print('show', j)
        print(DATA_QUEUE.empty())
        data = DATA_QUEUE.get()
        print(data[1].shape)
