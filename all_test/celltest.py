
"""索引方式"""


class Cell(object):
    # def __init__(self):
    #     self.centreX
    #     self.centreY
    #     self.index1
    #     self.index2

    def __init__(self, centre_x, centre_y, index1, index2, pic, label):
        self.centreX = centre_x
        self.centreY = centre_y
        self.index1 = index1
        self.index2 = index2
        self.pic = pic
        self.label = label

    def set_centre_pos(self, centre_x, centre_y):
        self.centreX = centre_x
        self.centreY = centre_y

    def set_index(self, index1, index2):
        self.index1 = index1
        self.index2 = index2

    def set_picture(self, pic):
        self.pic = pic

    def get_centre_pos(self):
        return self.centreX, self.centreY

    def get_index(self):
        return self.index1, self.index2

    def get_pic(self):
        return self.pic

    def set_label(self, label):
        self.label = label

    def get_label(self):
        return self.label



def table(all_num):
    pic = 1
    cell_table = {}
    for k in range(1, all_num):
        # 创建索引表
        for i in range(1, 10):
            l2 = encode(i)
            for j in range(1, 10):
                l1 = encode(j)
                code = l1 + 10 * l2
                cell_table[100*k+code] = Cell(1, 1, l1, l2, pic)
                ++pic
    print("lists is:", cell_table)
    return cell_table


def main():
    cell = Cell(1, 1, 1, 1, 2)
    print(cell.centreX, cell.centreY, cell.index1, cell.index2, cell.pic)


# map索引的映射关系
def encode(i):
    if i == 1:
        y = 2
    if i == 2:
        y = 7
    if i == 3:
        y = 4
    if i == 4:
        y = 5
    if i == 5:
        y = 1
    if i == 6:
        y = 9
    if i == 7:
        y = 8
    if i == 8:
        y = 3
    if i == 9:
        y = 6
    return y


if __name__ == '__main__':
    table = table(81)
    # 输出索引表
    for num in range(1, 81):
        for lv1 in range(1, 10):
            for lv2 in range(1, 10):
                key = lv1+lv2*10+num*100
                print("第 %s 的值" % key)
                print(table.get(key).pic)

    x = table.get(121)
    print('我是第 %s 张图' % (x.pic, ))

