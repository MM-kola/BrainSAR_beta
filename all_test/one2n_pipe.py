from multiprocessing import Process, Queue, Pipe
import time
import numpy as np
import signal
import os
from all_test.Biosemi_server import Biosemi_Server

"""
消费者，只需要接受显示数据
留有一个recv做通道
"""


class Consumer:
    def __init__(self, key, pull, queue):
        # 常量赋值
        self.CHANNEL = 64
        self.T = 400
        self.MAX = self.T * 2
        # 变量初始化
        self.queue = queue
        self.key = key  # 索引号，encode index
        self.recv = pull
        self.data = np.zeros(shape=(self.CHANNEL, self.T))
        self.first = True

    def recv_data(self):
        x = self.recv.recv()
        if isinstance(x, str):
            if self.isfull():
                # print("我好了！")
                self.killme()
            else:
                self.recv.send("NO")
        else:
            if self.first:
                self.data = x
                self.first = False
            else:
                self.data = np.hstack((self.data, x))
            print("消费者现在长度：", self.data.shape)

    def isfull(self):
        return self.data.shape[1] >= self.MAX

    def killme(self):
        self.recv.send(self.key)
        self.recv.send(self.data)
                # print('弹出', self.queue.qsize())

# """
# 生产者，只需要循环产出数据
# 接收一个queue用来接受推出的数据
# """
# class Producer:
#     def __init__(self, sendqueue):
#         self.Biosemi = Biosemi_Server(time=0.005, QUEUE=sendqueue)
#         self.Biosemi.start_server()
#         self.send = sendqueue
#
#
#     def msgsend(self):
#         # t = 0
#         while True:
#             t = np.random.random((64, 10))
#             self.send.put(t)
#             # t += 1
#             time.sleep(1)
#             # print("生产者在产生数据ing")


"""
生产者，只需要循环产出数据
接收一个queue用来接受推出的数据
"""


class Producer:
    def __init__(self, sendqueue):
        self.Biosemi = Biosemi_Server(time=0.2)
        self.send = sendqueue

    def msgsend(self):
        # t = 0
        while True:
            t = self.Biosemi.getdata()
            # print(t.shape)
            self.send.put(t)
            # t += 1
            # time.sleep(1)
            # print("生产者在产生数据ing")

    def close(self):
        self.Biosemi.close()


"""
中间转换功能
"""

class Switch:
    def __init__(self, queue_in, queue_out):
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.data = 0
        self.pipe_table = {}

    # 中心处理节
    # 1、先刷新表，看是否需要新的申请和kill
    # 2、
    def switcher(self):
        # while True:
        #     print("进程中的switch_table:", self.pipe_table)
        DEL_FLAG = False
        if self.queue_in.empty != 1:
            self.data = self.queue_in.get()
            # print("出队数据：", self.data)
            # print("进程中的switch_table:", self.pipe_table)
            # 检测是否需要更新
            for value in self.pipe_table.values():
                value[1].send("kill?")
                recv = value[1].recv()
                if isinstance(recv, int):
                    DEL_FLAG = True
                    del_key = recv
                    print("杀死进程：", del_key)
                    recv = value[1].recv()
                    self.queue_out.put(recv)
                    os.kill(value[0], signal.SIGTERM)
                else:
                    value[1].send(self.data)
            if DEL_FLAG:
                self.del_pipe(del_key)
                # print("遍历switch_table:", value)

    def make_pipe(self, key):
        (push, pull) = Pipe()
        poc = [0, 0]
        poc[1] = push
        self.pipe_table[key] = poc
        # print(self.pipe_table)
        return pull

    def get_pid(self, pid, key):
        self.pipe_table.get(key)[0] = pid
        print(self.pipe_table.get(key)[0])

    def del_pipe(self, key):
        pid = self.pipe_table.pop(key)[0]
        return pid

    def send_data(self):
        return 0


"""
循环产生新生产者
在产生生产者的时候反馈给switch，
让switcher刷新其pipe——table
(必须写在进程外部！！！)
"""


def newp(recv, key, queue):
    # print(recv)
    # 产生一个消费者
    x = Consumer(recv, key, queue)
    # 循环接受pipe中的数据并且拼接
    # 接受前检查是否满编，如果满编则申请kill
    # kill:
    # 1、停止接受数据
    # 2、反馈给switcher让其更新表，删除表中
    while True:
        x.recv_data()


def timer(a):
    K = 0
    while True:
        time.sleep(1)
        a.send(K)
        K += 1


def outqueue(queue):
    while True:
        if ~queue.empty():
            print('出队：', queue.get().shape)
        time.sleep(0.1)


queue_in = Queue()
queue_out = Queue()


def main():
    # 唯一的生产者，每一秒往queue_in队列中push一个值
    # key = 0
    prd = Producer(queue_in)
    procducer = Process(target=prd.msgsend, args=())
    procducer.start()
    pid_procducer = procducer.pid

    procs1 = Process(target=outqueue, args=(queue_out,))
    procs1.start()

    switcher = Switch(queue_in, queue_out)
    # (a, b) = Pipe()
    # 每过一秒申请一个消费者，并且调用switch函数建造一个pipe
    for key in range(10):
        # if NEW_C:
        pull = switcher.make_pipe(key=key)
        procs = Process(target=newp, args=(key, pull, queue_out, ))
        procs.start()
        # 更新pid
        switcher.get_pid(pid=procs.pid, key=key)
        switcher.switcher()
        key += 1
        time.sleep(0.1)
    # print(queue_out.empty())

    # 退出操作
    while True:
        print("等待结束。。。")
        switcher.switcher()
        # print(queue_out.empty())
        # print(queue_out.qsize())
        # print(queue_out.get().shape)
        time.sleep(0.1)
        if queue_out.qsize() == 10:
            os.kill(pid_procducer, signal.SIGTERM)
            # break
    # while True:
        # print('队列长度', queue_out.qsize())
        # print('队列空', queue_out.empty())
        # print("输出长度：", queue_out.get().shape)
        # if queue_out.empty():
        #     print('结束了！')
        #     break
    return


if __name__ == '__main__':
    main()
