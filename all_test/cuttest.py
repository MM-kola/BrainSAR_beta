"""方形切图"""


from psychopy import visual, core, event
import cv2
import os
from PIL import Image as im
from all_test import celltest as cell
import math
im.MAX_IMAGE_PIXELS = None


def cut(lft_width, rt_width, lft_height, rt_height):

    return 1


def ternary_2(x):
    k = x % 3
    x = int(x/3)
    y = k*1 + x*10
    return y


def cut_slice(cell_line=200):
    image = im.open('G:/BrainSAR_Beta/SAR图片/original_SAR.jpg')
    # image.size
    # image.save('o.png', 'png')
    print(image.size)
    num_w = math.floor(image.size[0]/(9*cell_line))
    num_h = math.floor(image.size[1]/(9*cell_line))
    all_num = num_w * num_h
    print(num_w, num_h, all_num)
    # cropped = image.crop((0, 0, cell_width, cell_height))
    # print(cropped.size)
    allindex = 0
    num = 0
    cell_table = {}
    baseliney = 10
    baselinex = 10
    for all_h in range(num_h):
        ALL_basey = all_h * 9 * cell_line+baseliney
        print('block3循环：\r')
        for all_w in range(num_w):
            ALL_basex = all_w * 9 * cell_line+baselinex
            allindex += 1
            # block 2循环
            # print('ALL_base:', ALL_basex, ALL_basey)
            print('block2循环：\r')
            for i in range(1, 10):
                l2 = cell.encode(i)
                BASE = ternary_2(i-1)
                base_posx = BASE % 10*3*cell_line+ALL_basex
                base_posy = int(BASE/10)*cell_line+ALL_basey
                # block 1循环
                print('block1循环：\r')
                for j in range(1, 10):
                    CELL = ternary_2(j-1)
                    cell_posx = CELL % 10*200+base_posx
                    cell_posy = int(CELL/10)*200+base_posy
                    # print(cell_posx, cell_posy, cell_line, cell_line)
                    cropped = image.crop((cell_posx, cell_posy, cell_posx+cell_line, cell_posy+cell_line))
                    l1 = cell.encode(j)
                    code = l1 + 10 * l2
                    index_pic = 100 * allindex + code
                    cell_table[index_pic] = cell.Cell(0, 0, l1, l2, cropped)
                    name = str('G:/BrainSAR_Beta/切片/') + str(index_pic) + '.png'
                    cropped.save(name, 'png')
                    num += 1
                    print(allindex, num)



    #
    # cropped.show()
    # cropped.save('crop.png', 'png')
    # cell_table = {}
    # pic = 1
    # for k in range(1, all_num):
    #     # 创建索引表
    #     for i in range(1, 10):
    #         l2 = cell.encode(i)
    #         for j in range(1, 10):
    #             l1 = cell.encode(j)
    #             code = l1 + 10 * l2
    #             cell_table[100 * k + code] = cell.Cell(1, 1, l1, l2, pic)
    #             ++pic
    # print("lists is:", cell_table)

# win = visual.Window(fullscr=True, color=(0.5, 0.5, 0.5))
# pic = visual.ImageStim(win, image=Image)
# pic.draw()
# win.flip()
# core.wait(0.5)

if __name__ == '__main__':
    cut_slice(250)
    # name = 'G:/BrainSAR_Beta/SAR图片/original_SAR.jpg'
    # print(os.path.splitext(os.path.split(name)[1])[0])
    # print(ternary_2(2))

