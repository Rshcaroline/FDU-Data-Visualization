from PIL import Image
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import copy
from scipy.misc import imread, imshow


def equal_line(file_path, num):
    # 读入图片并转换成灰度图格式
    im = np.array(Image.open(file_path).convert("L")).astype(np.uint8)
    i, j = im.shape

    # 复制一个一样的数组 用于画等值线
    # 注意这里不能直接"=" 因为只会赋值地址
    im_new_array = copy.deepcopy(im)

    # 循环遍历i,j
    for a in range(i):
        for b in range(j):
            # 如果原图片的值等于规定值 则令新数组值为0 显示为黑色
            if im[a, b] == num:
                im_new_array[a, b] = 0

    # 开始作图
    plt.figure(figsize=(5, 3))

    plt.subplot(1, 2, 1)
    plt.title('origin')
    plt.imshow(im, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title('equal line ' + str(num))
    plt.imshow(im_new_array, cmap="gray")
    plt.axis("off")
    # plt.show()
    plt.savefig('Q3.png')


if __name__ == "__main__":
    fold = './data/'
    file_path = fold + "hw3.png"

    equal_line(file_path, 100)


