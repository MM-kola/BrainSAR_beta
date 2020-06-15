import socket
import random
from psychopy import visual, core, event
import os

class SocketServer:
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 建立一个tcp/ip scoket
        sock.bind(('localhost', 9999))  # 绑定端口号
        sock.listen(5)  # 监听
        self.sock = sock

    def start_server(self):
        # while True:
        print('开始等待客户端过来')
        client, addr = self.sock.accept()
        print('客户过来了', addr)
        try:
            self.client_recv(client, addr)
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
            elif data == 'try_to_connect':
                msg = 'pic_addr_plz'
                client.send(msg.encode())
                data = client.recv(1024).decode()
                pic_addr = str(data)
                msg = 'rate_plz'
                client.send(msg.encode())
                data = client.recv(1024).decode()
                rate = 1.0/float(data)
                print(pic_addr, rate)
                # 另加核对
                break
        print('开始展示图片')
        cf = os.listdir(pic_addr)
        allnum = len(cf)
        # cf = random.sample(cf, len(cf))
        # win = visual.Window(fullscr=True, color=(199, 237, 204), colorSpace='rgb255')
        win = visual.Window(color=(199, 237, 204), colorSpace='rgb255')
        text_1 = visual.TextStim(win, text=u'如果您准备好了请敲击任意键开始判读，10s后自动开始',
                                 height=0.1,
                                 pos=(0, 0),
                                 bold=True,
                                 italic=True)
        text_1.draw()
        win.flip()
        core.wait(0)
        event.waitKeys(1)
        for num in range(1, int(allnum / 81) + 1):
            for lv1 in range(1, 10):
                for lv2 in range(1, 10):
                    msg = 'start_eeg'
                    client.send(msg.encode())
                    data = client.recv(1024).decode()
                    if data == 'pic_index':
                        key = lv1 + lv2 * 10 + num * 100
                        client.send(str(key).encode())
                        # print('发送的key', key)
                        imgname = pic_addr + '/' + str(key) + '.png'
                        # Image = os.path.join(imgname)
                        pic = visual.ImageStim(win, image=imgname)
                        pic.draw()
                        win.flip()
                        core.wait(rate)

        # for i in cf:
        #         #     if os.path.splitext(i)[1] == '.jpg':
        #         #         Image = os.path.join(pic_addr, i)
        #         #         pic = visual.ImageStim(win, image=Image)
        #         #         msg = 'start_eeg'
        #         #         client.send(msg.encode())
        #         #         pic.draw()
        #         #         win.flip()
        #         #         core.wait(rate)
                # print(Image)
        # 原呈现
        # for i in cf:
        #     if os.path.splitext(i)[1] == '.jpg':
        #         Image = os.path.join(pic_addr, i)
        #         pic = visual.ImageStim(win, image=Image)
        #         msg = 'start_eeg'
        #         client.send(msg.encode())
        #         pic.draw()
        #         win.flip()
        #         core.wait(rate)
        #         # print(Image)
        client.send('end'.encode())
        print('发送结束命令')
        text_3 = visual.TextStim(win, text=u'结束在线判读，请耐心等待结果',
                                 height=0.1,
                                 pos=(0, 0),
                                 bold=True,
                                 italic=True)
        text_3.draw()
        win.flip()
        core.wait(2)
        # for i in range(100):
        #     msg = 'start_eeg'
        #     client.send(msg.encode())
        #     time.sleep(rate)
        data = client.recv(1024).decode()
        print(data)
        if data == 'done':
            client.close()
            core.quit()


if __name__ == '__main__':
    t1 = SocketServer()
    t1.start_server()
