import time
import queue
from multiprocessing import Process, Queue, Pipe

MSG_QUEUE_base = Queue(maxsize=5)
MSG_QUEUE = Queue()

# 展示一组数据5
def getqueue(msgQueue, i):
    while True:
        if msgQueue.empty() > 0:
            print('queue is empty %d' % (msgQueue.qsize()))
        else:
            msg = msgQueue.get()
            print('get msg %s %d' % (msg, i, ))
        time.sleep(1)

# 得到一个数据1
def putqueue(msgQueue1, eegflag, startflag):
    while True:
        if eegflag.recv():
            if msgQueue1.full():
                startflag.send(True)
                msgQueue1.get()
                msgQueue1.put('hello world')
                time.sleep(1)
            else:
                msgQueue1.put('hello world')
                time.sleep(1)

# 得到一组数据5
def getqueue1(msgQueue1, msgQueue2, show0flag, i):
    while True:
        if show0flag.recv():
            # print('queue is empty %d' % (msgQueue1.qsize()))
            outlist = {}
            for k in range(int(msgQueue1.qsize())):
                x = msgQueue1.get()
                outlist[k] = x
                msgQueue1.put(x)
                print("x:", x, k)
            msgQueue2.put(outlist)
            print('put hello world queue size is %d %d' % (msgQueue1.qsize(), i, ))


def test():
    (eegflag, show1flag) = Pipe()
    (startflag, show0flag) = Pipe()
    processA = Process(target=getqueue, args=(MSG_QUEUE, 0))
    processC = Process(target=putqueue, args=(MSG_QUEUE_base, eegflag, startflag))
    processB = Process(target=getqueue1, args=(MSG_QUEUE_base, MSG_QUEUE, show0flag, 2))

    processA.start()
    print('processA start..')

    processB.start()
    print('processC start..')

    processC.start()
    print('processC start..')

    while True:
        show1flag.send(True)
        time.sleep(1)


if __name__ == '__main__':
    test()
