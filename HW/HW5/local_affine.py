from skimage import io
from matplotlib import pyplot as plt
import math
import numpy as np

srcImage = io.imread("zxh-ape.jpg")
tarImage = io.imread("ape.png")[...,:3]

srcAnchors = [(348, 463), (483, 422), (474, 535),
              (391, 320), (389, 421), (375, 522), (363, 612),
              (566, 411), (575, 457), (579, 486), (568, 523), (548, 569)]

tarAnchors = [(27, 127), (185, 77), (189, 166),
              (23, 68), (40, 114), (37, 145), (26, 188),
              (176, 49), (222, 80), (236, 126), (222, 168), (197, 198)]

def annotation_visualization():
    for anchor in srcAnchors:
        x, y = anchor
        for x_ in range(x-5, x+5):
            for y_ in range(y-5, y+5):
                srcImage[x_, y_, :] = 255

    for anchor in tarAnchors:
        x, y = anchor
        for x_ in range(x-5, x+5):
            for y_ in range(y-5, y+5):
                tarImage[x_, y_, :] = 255

    io.imshow(srcImage)
    plt.show()
    io.imshow(tarImage)
    plt.show()

def _distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def _local_affine(coord1, tarAnchors, srcAnchors, linearFunc):
    for i, anchor in enumerate(tarAnchors):
        if coord1 == anchor:
            return srcAnchors[i]
    else:
        e = 2.5
        dis = [(1/_distance(coord1, c))**e for c in tarAnchors]
        disSum = sum(dis)

        coordX, coordY = [], []

        for d, linear_affine in zip(dis, linearFunc):
            x_, y_ = linear_affine(coord1)
            coordX.append((d/disSum)*x_)
            coordY.append((d/disSum)*y_)

        return (sum(coordX), sum(coordY))

def _pick_pixel(coord, srcImage):
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

def linear_func(coord1, coord2):
    bias_x = coord2[0] - coord1[0]
    bias_y = coord2[1] - coord1[1]
    def _linear_func(coord1):
        x, y = coord1
        return ((x+bias_x), (y+bias_y))
    return _linear_func

def local_affine_backward(srcImage, tarImage, srcAnchors, tarAnchors):
    linearFuncForward = [linear_func(c1, c2) for c1, c2 in zip(tarAnchors, srcAnchors)]
    linearFuncBackward = [linear_func(c2, c1) for c1, c2 in zip(tarAnchors, srcAnchors)]

    height, width, _ = srcImage.shape
    temp = np.zeros_like(srcImage)

    for row in range(height):
        for col in range(width):
            coord = _local_affine((row, col), srcAnchors, tarAnchors, linearFuncBackward)
            coord = _local_affine(coord, tarAnchors, srcAnchors, linearFuncForward)
            temp[row, col, :] = _pick_pixel(coord, srcImage)
    return temp

def local_affine_forward(srcImage, tarImage, srcAnchors, tarAnchors):
    linearFuncForward = [linear_func(c1, c2) for c1, c2 in zip(tarAnchors, srcAnchors)]

    height, width, _ = tarImage.shape
    print(srcImage.shape)
    print(tarImage.shape)

    for row in range(height):
        for col in range(width):
            coord = _local_affine((row, col), tarAnchors, srcAnchors, linearFuncForward)
            tarImage[row, col, :] = _pick_pixel(coord, srcImage)
    return tarImage


if __name__ == "__main__":
    # io.imshow(local_affine_forward(srcImage, tarImage, srcAnchors, tarAnchors))
    annotation_visualization()
    plt.show()
