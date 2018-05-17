'''
3threshold.py 
'''
#  pip install Pillow

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

fold='C:/Users/zxh/work/0_projects/DataV_Python/5image/'
img=Image.open(fold+'brain.png')


gray=np.array(img.convert('L'))   #转换成灰度的Image格式和数组格式
xsize, ysize = gray.shape # x is vertical
#chan = 1
#print(xsize, ysize, chan)
print(np.max(gray), ' ', np.min(gray))

def GetThresholdValue( gray ):
	"design your method here" 
	thresh=200
	return thresh

thresh = GetThresholdValue( gray )

resultimage = np.zeros([xsize, ysize], np.int8) # -128 127
Foreground = 1
for x in range(xsize):
	for y in range(ysize):
		if gray[x,y]>thresh:
			resultimage[x,y] = Foreground

plt.figure('threshold using '+str(thresh))

plt.subplot(2,1,1), plt.title('origin')
plt.imshow(img), plt.axis('off')
plt.subplot(2,1,2), plt.title('binary')
plt.imshow( resultimage,cmap='gray' ), plt.axis('off')

plt.show()

 

