from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

fold='./'
img=Image.open(fold+'brain.png')

gray=np.array(img.convert('L'))   #转换成灰度的Image格式和数组格式
xsize, ysize = gray.shape # x is vertical


resultimage = np.zeros([xsize, ysize], np.float)

kern = np.ones([3, 3], np.float)
kern = kern*1.0/9.0


print(kern)

ntime = 5
imgsm = gray

for nt in range(ntime):
    for x in range(1, xsize-1):
        for y in range(1, ysize-1):
            smooth = 0.0
            for a in range(-1, 2):
                for b in range(-1, 2):
                    smooth += imgsm[x+a, y+b] * kern[a+1, b+1]
            resultimage[x, y] = smooth
    imgsm = resultimage

plt.figure('smooth ' + str(ntime) + ' times')

plt.subplot(2,1,1)
plt.title('origin')
plt.imshow(img)
plt.axis('off')
plt.subplot(2,1,2)
plt.title('smoothed')
plt.imshow(resultimage, cmap='gray')
plt.axis('off')

plt.show()