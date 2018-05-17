from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

fold='./'
img=Image.open(fold+'brain.png')

gray=np.array(img.convert('L'))   #转换成灰度的Image格式和数组格式
xsize, ysize = gray.shape # x is vertical

map = np.zeros([xsize, ysize], np.float)

N=3

kernx = np.zeros([N, N], np.float)
kernx[1,0], kernx[1,2] = -0.5, 0.5

kerny = np.zeros([N, N], np.float)
kerny[0,1], kerny[2,1] = -0.5, 0.5

print(kernx)
print(kerny)


for x in range(1, xsize-1):
    for y in range(1, ysize-1):
        gx = 0.5*np.float(gray[x+1, y]) - 0.5*np.float(gray[x-1, y])
        gy = 0.5*np.float(gray[x, y+1]) - 0.5*np.float(gray[x, y-1])
        map[x, y] = np.sqrt(gx*gx + gy*gy)

plt.figure('gradient magnitude')

plt.subplot(2,1,1)
plt.title('origin')
plt.imshow(img)
plt.axis('off')
plt.subplot(2,1,2)
plt.title('magnitude')
plt.imshow(map, cmap='gray')
plt.axis('off')

plt.show()