import time

import signal
import os
from multiprocessing import Process, Queue

MSG_QUEUE = Queue()


def startA(msgQueue, i):
        while True:
            if msgQueue.empty() > 0:
                print('queue is empty %d' % (msgQueue.qsize()))
                print(msgQueue)
            else:
                msg = msgQueue.get()
                print('get msg %s %d' % (msg, i, ))
                print(msgQueue)
            time.sleep(2)


def startB(msgQueue, i):
    while True:
        msgQueue.put('hello world')
        print('put hello world queue size is %d %d' % (msgQueue.qsize(), i, ))
        print(msgQueue)
        time.sleep(1)

def startC(msgQueue, i):
    for n in range(10):
        msgQueue.put('hello world', False)
        print('put hello world queue size is %d %d' % (msgQueue.qsize(), i, ))
        print(msgQueue)
        time.sleep(1)
    return


if __name__ == '__main__':
    processA = Process(target=startA, args=(MSG_QUEUE, 0))
    processC = Process(target=startB, args=(MSG_QUEUE, 1))
    processB = Process(target=startC, args=(MSG_QUEUE, 2))

    processA.start()
    print('processA start..', processA.pid)

    processB.start()
    print('processB start..', processB.pid)

    processC.start()
    print('processC start..', processC.pid)

    while True:
        time.sleep(1)
        print(processC.is_alive())

    # os.kill(processC.pid, signal.SIGTERM)  # 注意此处的PID需要是int类型的

