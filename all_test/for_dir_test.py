import time

dir = {}
for i in range(10):
    dir[i] = i
ts = time.time()
for value in dir.values():
    te = time.time()
    print(value, te-ts)