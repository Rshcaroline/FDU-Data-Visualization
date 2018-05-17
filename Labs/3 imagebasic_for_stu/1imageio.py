'''
1imageio.py 
'''
#  pip install Pillow

from PIL import Image
import matplotlib.pyplot as plt
fold='C:/Users/zxh/work/0_projects/DataV_Python/5image/'
img=Image.open(fold+'brain.png')

plt.figure("brain PD MRI")
plt.imshow(img)
plt.show()


print(img.size) #图片的尺寸
print(img.mode) #图片的模式
print(img.format) #图片的格式
#img.Save(fold+'test.jpg') # save


fold='./'
img=Image.open(fold+'feifei.jpg')
gray=img.convert('L')   #转换成灰度的Image格式
r,g,b=img.split()   #分离三通道
pic=Image.merge('RGB',(r,g,b)) #合并三通道

plt.figure("convert color")
plt.subplot(2,3,1), plt.title('origin')
plt.imshow(img),plt.axis('off')
plt.subplot(2,3,2), plt.title('gray')
plt.imshow(gray,cmap='gray'),plt.axis('off')
plt.subplot(2,3,3), plt.title('merge')
plt.imshow(pic),plt.axis('off')
plt.subplot(2,3,4), plt.title('r')
plt.imshow(r,cmap='gray'),plt.axis('off')
plt.subplot(2,3,5), plt.title('g')
plt.imshow(g,cmap='gray'),plt.axis('off')
plt.subplot(2,3,6), plt.title('b')
plt.imshow(b,cmap='gray'),plt.axis('off')
plt.show()



