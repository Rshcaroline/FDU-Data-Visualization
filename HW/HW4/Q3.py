from PIL import Image
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imread, imshow


# Interpolation
def GetBilinearPixel(imArr, posX, posY):
    out = []
    # Get integer and fractional parts of numbers
    modXi = int(posX)
    modYi = int(posY)
    modXf = posX - modXi
    modYf = posY - modYi
    modXiPlusOneLim = min(modXi + 1, imArr.shape[1] - 1)
    modYiPlusOneLim = min(modYi + 1, imArr.shape[0] - 1)
    # Get pixels in four corners
    for chan in range(imArr.shape[2]):
        bl = imArr[modYi, modXi, chan]
        br = imArr[modYi, modXiPlusOneLim, chan]
        tl = imArr[modYiPlusOneLim, modXi, chan]
        tr = imArr[modYiPlusOneLim, modXiPlusOneLim, chan]

        # Calculate interpolation
        b = modXf * br + (1. - modXf) * bl
        t = modXf * tr + (1. - modXf) * tl
        pxf = modYf * t + (1. - modYf) * b
        out.append(int(pxf + 0.5))
    return out


if __name__ == "__main__":
    fold = './data/'
    im = imread(fold + "feifei.png", mode="RGB")

    enlargedShape = [int(im.shape[0] * 4), int(im.shape[1] * 4), im.shape[2]]
    enlargedImg = np.empty(enlargedShape, dtype=np.uint8)
    rowScale = float(im.shape[0]) / float(enlargedImg.shape[0])
    colScale = float(im.shape[1]) / float(enlargedImg.shape[1])

    for r in range(enlargedImg.shape[0]):
        for c in range(enlargedImg.shape[1]):
            oric = c * colScale
            orir = r * rowScale  # Find position in original image
            enlargedImg[r, c] = GetBilinearPixel(im, oric, orir)
    print("Hey, Interploation is completed")

    ############################
    # 读取灰度图像并获得矩阵长宽
    fold = './data/'
    image = Image.open(fold + 'feifei.png').convert("L")
    image_array = np.array(image)
    k = len(enlargedImg)
    i, j = enlargedImg[0].shape

    T = {0: [], 1: [], 2: []}

    ############################
    im_new_array = enlargedImg
    # 循环遍历i,j
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 240:
                    im_new_array[c][a][b] = 0
    print("240's value is completed")

    ############################
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 224:
                    im_new_array[c][a][b] = 0
    print("224's value is completed")

    ############################
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 208:
                    im_new_array[c][a][b] = 0
    print("208's value is completed")

    ############################
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 192:
                    im_new_array[c][a][b] = 0
    print("192's value is completed")

    ############################
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 176:
                    im_new_array[c][a][b] = 0
    print("176's value is completed")

    ############################
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 160:
                    im_new_array[c][a][b] = 0
    print("160's value is completed")

    ############################
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 128:
                    im_new_array[c][a][b] = 0
    print("128's value is completed")

    ############################
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 96:
                    im_new_array[c][a][b] = 0
    print("96's value is completed")

    ############################
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 80:
                    im_new_array[c][a][b] = 0
    print("80's value is completed")

    ############################
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 64:
                    im_new_array[c][a][b] = 0
    print("64's value is completed")

    ############################
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 48:
                    im_new_array[c][a][b] = 0
    print("48's value is completed")

    ############################
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 32:
                    im_new_array[c][a][b] = 0
    print("32's value is completed")

    ############################
    for c in range(k):
        for a in range(i):
            for b in range(j):
                if enlargedImg[c][a][b] == 16:
                    im_new_array[c][a][b] = 0
    print("16's value is completed")

    plt.imshow(im_new_array, cmap='gray')
    plt.axis("off")
    plt.show()

    # figure()
    # gray()
    # contour(image, origin='image')
    # axis('equal')
    # axis('off')
    # title('what')
    # show()
