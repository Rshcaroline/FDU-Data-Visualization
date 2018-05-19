import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imread, imshow


def GetBilinearPixel(imArr, posX, posY):
    out = []
    # Get integer and fractional parts of numbers
    Xi = int(posX)
    Yi = int(posY)
    Xf = posX - Xi
    Yf = posY - Yi
    XiPlusOneLim = min(Xi + 1, imArr.shape[1] - 1)
    YiPlusOneLim = min(Yi + 1, imArr.shape[0] - 1)

    # Get pixels in four corners
    for chan in range(imArr.shape[2]):    # Don't forget it's three channels
        bl = imArr[Yi, Xi, chan]
        br = imArr[Yi, XiPlusOneLim, chan]
        tl = imArr[YiPlusOneLim, Xi, chan]
        tr = imArr[YiPlusOneLim, XiPlusOneLim, chan]

        # Calculate interpolation
        b = Xf * br + (1. - Xf) * bl
        t = Xf * tr + (1. - Xf) * tl
        pxf = Yf * t + (1. - Yf) * b
        out.append(int(pxf + 0.5))

    return out


if __name__ == "__main__":
    # GRB is three channel
    im = imread("./data/feifei.png", mode="RGB")

    # The enlarge part. Enlarge 2 times.
    enlargedShape = [int(im.shape[0] * 2), int(im.shape[1] * 2), im.shape[2]]
    enlargedImg = np.empty(enlargedShape, dtype=np.uint8)

    rowScale = float(im.shape[0]) / float(enlargedImg.shape[0])
    colScale = float(im.shape[1]) / float(enlargedImg.shape[1])

    for r in range(enlargedImg.shape[0]):
        for c in range(enlargedImg.shape[1]):
            oric = c * colScale
            orir = r * rowScale      # Find position in original image
            enlargedImg[r, c] = GetBilinearPixel(im, oric, orir)   # linear interpolation

    # The reduce part. Reduce 0.5 times.
    reducedShape = [int(im.shape[0] * 0.5), int(im.shape[1] * 0.5), im.shape[2]]
    reducedImg = np.empty(reducedShape, dtype=np.uint8)

    rowScale2 = float(im.shape[0]) / float(reducedImg.shape[0])
    colScale2 = float(im.shape[1]) / float(reducedImg.shape[1])

    for t in range(reducedImg.shape[0]):
        for p in range(reducedImg.shape[1]):
            oric2 = p * colScale2
            orir2 = t * rowScale2     # Find position in original image
            reducedImg[t, p] = GetBilinearPixel(im, oric2, orir2)

    plt.figure(figsize=(10,4))

    plt.subplot(1, 3, 1)
    plt.title('The original one')
    plt.imshow(im)

    plt.subplot(1, 3, 2)
    plt.title('The 2 times one')
    plt.imshow(enlargedImg)

    plt.subplot(1, 3, 3)
    plt.title('The 0.5 times one')
    plt.imshow(reducedImg)

    plt.savefig('Q2.png')
    # plt.show()