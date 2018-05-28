from PIL import Image
from pylab import *

im = array(Image.open('zxh-ape.jpg'))
imshow(im)
print('Please click 3 points')
x = ginput(3)

print('you clicked about nose:')
for i in x:
    print(i)

print('Please click 4 points')
x = ginput(4)
print('you clicked about eyes:')
for i in x:
    print(i)

print('Please click 5 points')
x = ginput(5)
print('you clicked about mouths:')
for i in x:
    print(i)

show()
