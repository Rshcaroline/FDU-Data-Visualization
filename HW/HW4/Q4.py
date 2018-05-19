from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


fold = './data/'
img = Image.open(fold+'feifei.png')
gray = np.array(img.convert('L'))      # 转换成灰度的Image格式和数组格式
xsize, ysize = gray.shape
resultimage=np.zeros([xsize,ysize], np.float)
N=3   # 卷积核的层数
# kern = np.ones([N,N],np.float)s
# kern = kern*1.0/(N*N)

# kern = np.mat([[0,-1,0],[-1,4,-1],[0,-1,0]])
# kern = np.mat([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
kern = np.mat([[-0.8,-0.8,-0.8],[-0.8,200,-0.8],[-0.8,-0.8,-0.8]])
ntime = 1
imgsm = gray

for nt in range(ntime):
    for x in range(1, xsize-1):
        for y in range(1, ysize-1):
            smooth = 0.0
            for a in range(-1, 2):
                for b in range(-1, 2):
                    smooth += imgsm[x+a,y+b] * kern[a+1,b+1]
                resultimage[x,y] = smooth
    imgsm = resultimage

plt.figure('smooth'+str(ntime)+'times')
plt.subplot(3,1,1)
plt.title('origin')
plt.imshow(gray, cmap='gray')
plt.axis('off')

plt.subplot(3,1,2)
plt.title('sharpen')
plt.imshow(resultimage, cmap='gray')
plt.axis('off')

plt.subplot(3,1,3)
plt.title('both')
plt.imshow(resultimage+gray, cmap='gray')
plt.axis('off')

# plt.show()
plt.savefig('Q4.png')