import socket
from multiprocessing import Process

class SocketServer:
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 建立一个tcp/ip scoket
        sock.bind(('localhost', 1024))  # 绑定端口号
        sock.listen(5)  # 监听
        self.sock = sock

    def start_server(self):
        while True:
            print('开始等待客户端过来')
            client, addr = self.sock.accept()
            print('客户过来了', addr)
            try:
                t = Process(target=self.client_recv, args=(client, addr))
                t.start()
            except Exception as e:
                print(e)

    def client_recv(self, client, addr):
        while True:
            try:
                data = client.recv(1024).decode()  # 获取到客户端的数据
            except Exception as e:
                print(e)
                break
            if not data or data == 'bye':
                # 如果没有发送过来数据就代表客户端close了，或者发过来bye代表连接要断开
                print('服务结束', addr)
                client.close()  # 断开连接，为下一个服务
                break
            else:  # 如果他还在发送的话
                print('发过来的', data)
                msg = 'close'
                client.send(msg.encode())  # 数据


if __name__ == '__main__':
    t1 = SocketServer()
    t1.start_server()


