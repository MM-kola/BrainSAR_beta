
# -*- encoding: utf-8 -*-
from socket import *
import random
from psychopy import visual, core, event
import os

pic_addr = "G:\BrainSAR_Beta\切片"
cf = os.listdir(pic_addr)
# cf = random.sample(cf, len(cf))
allnum = len(cf)
win = visual.Window(fullscr=True, color=(199, 237, 204), colorSpace='rgb255')
text_1 = visual.TextStim(win, text=u'如果您准备好了请敲击任何键开始判读，否则10s后自动开始',
                         height=0.1,
                         pos=(0, 0),
                         bold=True,
                         italic=True)
text_1.draw()
win.flip()
core.wait(0)
ok = event.waitKeys(10)
# for num in range(1, int(allnum/81) + 1):
#     for lv1 in range(1, 10):
#         for lv2 in range(1, 10):
#             key = lv1 + lv2 * 10 + num * 100
#             imgname = pic_addr + '/' + str(key) + '.png'
#             # Image = os.path.join(imgname)
#             pic = visual.ImageStim(win, image=imgname)
#             pic.draw()
#             win.flip()
#             core.wait(0.2)
# # for i in cf:
# #     if os.path.splitext(i)[1] == '.jpg':
# #         Image = os.path.join(pic_addr, i)
# #         pic = visual.ImageStim(win, image=Image)
# #         pic.draw()
# #         win.flip()
# #         core.wait(0.2)
# text_3 = visual.TextStim(win, text=u'结束在线判读，2秒后退出自动退出程序',
#                          height=0.1,
#                          pos=(0, 0),
#                          bold=True,
#                          italic=True)
# text_3.draw()
win.flip()
core.wait(2)
core.quit()
