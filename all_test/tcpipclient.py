
import socket
def socketclient():
    s = socket.socket()
    s.connect(('localhost', 1024))  # 连接服务端
    while True:
        data = input('data:').strip()
        # if len(data) == 0: continue
        s.send(data.encode())  # 发送数据
        recv = s.recv(1024).decode()
        print(recv)
        if recv == 'close':
            s.send("bye".encode())
            break
    s.close()
    print("结束客户端")


if __name__ == '__main__':
    for i in range(10):
        print("第 %s 轮发送", i)
        socketclient()
