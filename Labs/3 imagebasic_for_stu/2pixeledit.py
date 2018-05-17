from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

fold='./'
oimg=Image.open(fold+'brain.png')
img=np.array(oimg)

#随机生成5000个椒盐
rows,cols,dims=img.shape
for i in range(5000):
    x=np.random.randint(0,rows)
    y=np.random.randint(0,cols)
    img[x,y,:]=255

#画个圆圈
rows,cols,dims=img.shape
cen=[(rows-1)*0.5, (cols-1)*0.5]
radiusf, radiust = 50, 58
for x in range(rows):
    for y in range(cols):
        if (x-cen[0])**2+(y-cen[1])**2 <= radiust**2 and \
        (x-cen[0])**2+(y-cen[1])**2 >= radiusf**2:
            img[x,y,0]=255


plt.figure("with noise")
plt.imshow(img)
plt.axis('off')
plt.show()











