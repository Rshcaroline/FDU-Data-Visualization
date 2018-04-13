from PIL import Image
import numpy as np

# RGB to CMY 色彩转换
def rgbtocmy (file):
    RGB_img = np.asarray(file)
    CMYK_img = 255 - RGB_img
    CMYK_img = np.append(CMYK_img, np.zeros(shape=(RGB_img.shape[0], \
                                                   RGB_img.shape[1], 1)), \
                         axis=2)  # 将K赋值为0
    CMYK = Image.fromarray(np.uint8(CMYK_img))
    CMYK.mode = 'CMYK'
    return CMYK

# CMY to RGB 色彩转换
def cmytorgb (file):
    CMYK_img = np.asarray(file)
    RGB_img = 255 - CMYK_img[:,:,:3]
    RGB = Image.fromarray(np.uint8(RGB_img))
    RGB.mode = 'RGB'
    return RGB


if __name__ == '__main__':
    RGB =Image.open('./photo.JPG')
    CMYK = RGB.convert('CMYK')
    RGB = cmytorgb(CMYK)
    RGB.show()


