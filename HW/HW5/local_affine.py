import sys
from skimage import io
from matplotlib import pyplot as plt
import math
import numpy as np
import copy

# 读取图片
srcImage = io.imread("zxh-ape.jpg")
tarImage = io.imread("ape.png")[...,:3]

# 选定锚点
if len(sys.argv) <2 or sys.argv[1] == str(1):
    # 稀疏的锚点 `python local_affine.py 1` 可以获取
    srcAnchors = [(348, 463), (483, 422), (474, 535),
                  (391, 320), (389, 421), (375, 522), (363, 612),
                  (566, 411), (575, 457), (579, 486), (568, 523), (548, 569)]
    tarAnchors = [(27, 127), (185, 77), (189, 166),
                  (23, 68), (40, 114), (37, 145), (26, 188),
                  (176, 49), (222, 80), (236, 126), (222, 168), (197, 198)]

else:
    # 稠密的锚点 `python local_affine.py 2` 可以获取
    srcAnchors = [(382, 349), (381, 384), (383, 420),
                  (369, 524), (360, 559),(358, 594),
                  (481, 425), (472, 536), (469, 477),
                  (560, 412), (582, 431),(598, 455), (602, 490), (592, 523), (572, 545), (546, 561)]
    tarAnchors = [(25, 66), (27, 87), (39, 114),
                  (36, 143), (24, 167), (22, 189),
                  (174, 74), (175, 166), (184, 118),
                  (192, 54), (214, 69), (230, 93),(231, 119), (224, 159), (212, 181), (196, 198)]

############### 辅助函数 ##############

def _distance(coord1, coord2):
    # 计算两点的欧式距离
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def _local_affine(coord1, tarAnchors, srcAnchors, linearFunc):
    # 对于锚点进行线性变换
    # 对于非锚点进行加权线性变换
    for i, anchor in enumerate(tarAnchors):
        if coord1 == anchor:
            return srcAnchors[i]
    else:
        e = 2.5 # 距离的指数
        dis = [(1/_distance(coord1, c))**e for c in tarAnchors]
        disSum = sum(dis)

        coordX, coordY = [], []

        for d, linear_affine in zip(dis, linearFunc):
            x_, y_ = linear_affine(coord1)
            coordX.append((d/disSum)*x_) # x点加权线性变换
            coordY.append((d/disSum)*y_) # y点加权线性变换

        return (sum(coordX), sum(coordY)) #坐标局部仿射结果

def _pick_pixel(coord, srcImage):
    # 双线性插值取像素
    r, c = coord
    h, w, _ = srcImage.shape

    c1, c2 = int(min(np.floor(c), w-1)), int(min(np.ceil(c), w-1)) # 横轴方向逆映射
    r1, r2 = int(min(np.floor(r), h-1)),  int(min(np.ceil(r), h-1)) # 纵轴方向逆映射

    if c1 == c2:
        f1, f2 = srcImage[r1, c1, :], srcImage[r2, c1, :]  # 横轴方向被整除时，避免分母为0
    else:
        # 横轴方向双线性插值
        f1 = (c2 - c) / (c2 - c1) * srcImage[r1, c2, :] +  (c - c1) / (c2 - c1) * srcImage[r1, c1, :]
        f2 = (c2 - c) / (c2 - c1) * srcImage[r2, c2, :] +  (c - c1) / (c2 - c1) * srcImage[r2, c1, :]
    if r1 == r2:
        res = f1  # 纵轴方向被整除时，避免分母为0
    else:
        # 将所求横轴插值在纵轴方向线性插值
        res = (r2 - r) / (r2 - r1) * f1 + (r - r1) / (r2 -r1) * f2
    return res

############### 核心函数 ##############

def linear_func(coord1, coord2):
    # 线性变换函数，即记录(x,y)的偏移项bias_x和bias_y
    bias_x = coord2[0] - coord1[0]
    bias_y = coord2[1] - coord1[1]
    def _linear_func(coord1):
        x, y = coord1
        return ((x+bias_x), (y+bias_y))
    return _linear_func

def local_affine_forward(srcImage, tarImage, srcAnchors, tarAnchors):
    # 前向图局部仿射(即上课内容)，即该程序的主函数
    # 获取锚点的线性变换
    linearFuncForward = [linear_func(c1, c2) for c1, c2 in zip(tarAnchors, srcAnchors)]

    tarImage_ = copy.deepcopy(tarImage)
    height, width, _ = tarImage_.shape

    # 遍历目标图的每一个像素，对该像素进行局部仿射(加权线性变换)，从而获取在源图的坐标
    for row in range(height):
        for col in range(width):
            coord = _local_affine((row, col), tarAnchors, srcAnchors, linearFuncForward)
            # 通过局部仿射获取源图坐标，在目标图坐标上填源图坐标的像素值
            tarImage_[row, col, :] = _pick_pixel(coord, srcImage)

    # 返回局部仿射图
    return tarImage_

def annotation_visualization(image):
    # 目标图、源图、结果图可视化
    srcImage_ = copy.deepcopy(srcImage)
    tarImage_ = copy.deepcopy(tarImage)

    # 探测锚点，变为蓝色
    for anchor in srcAnchors:
        x, y = anchor
        for x_ in range(x-8, x+8):
            for y_ in range(y-8, y+8):
                srcImage_[x_, y_, 2] = 255
                srcImage_[x_, y_, :2] = 0

    for anchor in tarAnchors:
        x, y = anchor
        for x_ in range(x-4, x+4):
            for y_ in range(y-4, y+4):
                tarImage_[x_, y_, 2] = 255
                tarImage_[x_, y_, :2] = 0

    # 显示图片
    plt.figure(figsize=(15,5))
    plt.subplot(131)
    plt.title("Target Image")
    plt.imshow(tarImage_)

    plt.subplot(132)
    plt.title("Source Image")
    plt.imshow(srcImage_)

    plt.subplot(133)
    plt.title("Local Affine Image")
    plt.imshow(image)

    plt.show()

if __name__ == "__main__":
    image = local_affine_forward(srcImage, tarImage, srcAnchors, tarAnchors)
    annotation_visualization(image)
