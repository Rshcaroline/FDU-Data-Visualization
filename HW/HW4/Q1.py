from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def balance(image_array, image_bins=256):
    # 将图像转换成为直方图，返回元祖（频数，直方图区间坐标）
    hist, bins = np.histogram(image_array.flatten(), image_bins)
    # 计算直方图的累积函数
    cdf = hist.cumsum()
    # 将累积函数转化到区间[0,255]
    cdf = (255.0 / cdf[-1]) * cdf
    # 原图像矩阵利用累积函数进行转化，插值过程，注意区间比累积函数多一位数
    balanced_imgarray = np.interp(image_array.flatten(), bins[:-1], cdf)
    # 返回均衡化后的图像矩阵
    return balanced_imgarray.reshape(image_array.shape)


# 读入图片并转成灰度图
fold = './data/'
name = 'feifei.png'
image = Image.open(fold + name).convert("L")
image_array = np.array(image)

plt.figure(figsize=(14, 14))

# gray picture
plt.subplot(3, 2, 1)
plt.title('Histogram of the gray picture')
plt.hist(image_array.flatten(), 256)
plt.subplot(3, 2, 2)
plt.title('The gray picture')
plt.imshow(image_array, cmap='gray')
plt.axis("off")

# balanced gray picture
balanced_imgarray = balance(image_array)
plt.subplot(3, 2, 3)
plt.title('Histogram of the balanced gray picture')
plt.hist(balanced_imgarray.flatten(), 256)
plt.subplot(3, 2, 4)
plt.title('The balanced gray picture')
plt.imshow(balanced_imgarray, cmap='gray')
plt.axis("off")

# difference between two pictures
diff = balanced_imgarray - image_array
plt.subplot(3, 2, 5)
plt.title('Histogram of the difference between two pictures')
plt.hist(diff.flatten(), 256)
plt.subplot(3, 2, 6)
plt.title('Difference between two pictures')
plt.imshow(diff, cmap='gray')
# 通过平移后，得到均衡化前以及均衡化后的差别的灰度值所做的图。
plt.axis("off")

plt.savefig('Q1.png')
# plt.show()
