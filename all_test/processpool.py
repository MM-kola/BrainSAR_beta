import os
import time
import random
from multiprocessing import Pool


def task(name):
    n = random.random()
    print('正在运行的任务：%s，PID：（%s）' % (name, os.getpid()))
    # print('任务%s将运行%s秒，PID：（%s）' % (name, n, os.getpid()))
    start = time.time()
    time.sleep(n * 10)
    end = time.time()
    print('!!!任务%s结束了，用时：%0.2f 秒' % (name, (end - start)))


if __name__ == '__main__':
    print('父进程ID：%s' % (os.getpid()))
    i = 0
    p = Pool(10)
    while True:
        p.apply_async(task, args=(i,))
        i = i+1
    print('等待所有添加的进程运行完毕。。。')
    # p.close()  # 在join之前要先关闭进程池，避免添加新的进程
    # p.join()
    print('End!!,PID:%s' % os.getpid())