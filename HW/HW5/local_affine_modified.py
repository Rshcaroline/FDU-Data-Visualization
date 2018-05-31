# -*- coding: utf-8 -*-

from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
import urllib
import base64
import json

def get_orangutan_message(rows,cols):
    # 手动定位的16个狒狒脸特征点
    # 包括：
    #   1、左右眼各3个特征点：两个眼角及眼球中心(3x2=6)
    #   2、鼻子3个特征点：左右鼻翼及鼻尖(3)
    #   3、嘴巴7个特征点：将嘴巴从左嘴角至右嘴角六等分，取7个点(7)
    points={}
    points['left_eye_left_corner']={'y':int(0.1*rows),'x':int(0.256*cols)}
    points['left_eye_center']={'y':int(0.106*rows),'x':int(0.34*cols)}
    points['left_eye_right_corner']={'y':int(0.156*rows),'x':int(0.444*cols)}
    points['right_eye_left_corner']={'y':int(0.144*rows),'x':int(0.556*cols)}
    points['right_eye_center']={'y':int(0.095*rows),'x':int(0.648*cols)}
    points['right_eye_right_corner']={'y':int(0.089*rows),'x':int(0.733*cols)}
    points['nose_left']={'y':int(0.683*rows) ,'x':int(0.287*cols)}
    points['nose_right']={'y':int(0.687*rows),'x':int(0.644*cols)}
    points['nose_tip']={'y':int(0.719*rows),'x':int(0.461*cols)}
    points['mouth_left_corner']={'y':int(0.751*rows),'x':int(0.210*cols)}
    points['mouth_lower_lip_left_contour2']={'y':int(0.836*rows),'x':int(0.269*cols)}
    points['mouth_lower_lip_left_contour3']={'y':int(0.899*rows),'x':int(0.363*cols)}
    points['mouth_lower_lip_bottom']={'y':int(0.904*rows),'x':int(0.465*cols)}
    points['mouth_lower_lip_right_contour3']={'y':int(0.877*rows),'x':int(0.617*cols)}
    points['mouth_lower_lip_right_contour2']={'y':int(0.832*rows),'x':int(0.702*cols)}
    points['mouth_right_corner']={'y':int(0.769*rows),'x':int(0.768*cols)}

    return points

def get_face_message(image_path):
    # 利用旷视Face++的API定位16个人脸特征点
    # 包括：
    #   1、左右眼各3个特征点：两个眼角及眼球中心(3x2=6)
    #   2、鼻子3个特征点：左右鼻翼及鼻尖(3)
    #   3、嘴巴7个特征点：将嘴唇下轮廓从左嘴角至右嘴角六等分，取7个点(7)
    
    url='https://api-cn.faceplusplus.com/facepp/v3/detect'
    API_KEY='znU49IIfP_C3jVSuTpHsbkCaE4yIzpLt'
    API_SECRET='E3j5lCz-XZRi6lJPvaiPfIHnuEygxRSA'

    # read image
    open_icon = open(image_path,"rb")
    b64str = base64.b64encode(open_icon.read())
    open_icon.close()

    # use api to detect face message
    para={'api_key':API_KEY,'api_secret':API_SECRET,'image_base64':b64str,'return_landmark':1}
    DATA=urllib.parse.urlencode(para).encode("utf-8")
    req= urllib.request.urlopen(url, DATA)
    faceData=json.loads(req.read())

    # 16 key points totally
    points={}
    points['left_eye_left_corner']=faceData['faces'][0]['landmark']['left_eye_left_corner']
    points['left_eye_center']=faceData['faces'][0]['landmark']['left_eye_center']
    points['left_eye_right_corner']=faceData['faces'][0]['landmark']['left_eye_right_corner']
    points['right_eye_left_corner']=faceData['faces'][0]['landmark']['right_eye_left_corner']
    points['right_eye_center']=faceData['faces'][0]['landmark']['right_eye_center']
    points['right_eye_right_corner']=faceData['faces'][0]['landmark']['right_eye_right_corner']
    points['nose_left']=faceData['faces'][0]['landmark']['nose_left']
    points['nose_right']=faceData['faces'][0]['landmark']['nose_right']
    points['nose_tip']=faceData['faces'][0]['landmark']['nose_tip']
    points['mouth_left_corner']=faceData['faces'][0]['landmark']['mouth_left_corner']
    points['mouth_lower_lip_left_contour2']=faceData['faces'][0]['landmark']['mouth_lower_lip_left_contour2']
    points['mouth_lower_lip_left_contour3']=faceData['faces'][0]['landmark']['mouth_lower_lip_left_contour3']
    points['mouth_lower_lip_bottom']=faceData['faces'][0]['landmark']['mouth_lower_lip_bottom']
    points['mouth_lower_lip_right_contour3']=faceData['faces'][0]['landmark']['mouth_lower_lip_right_contour3']
    points['mouth_lower_lip_right_contour2']=faceData['faces'][0]['landmark']['mouth_lower_lip_right_contour2']
    points['mouth_right_corner']=faceData['faces'][0]['landmark']['mouth_right_corner']

    return (points)

def affine_vector(u,v):
    # 该函数利用一对确定的点来求平移向量
    # input：2个点的坐标。其中u是原图的点，v是其在另一张图所对应的点。
    # output：平移向量b。此时，v=u+b
    vector = list(map(lambda x: x[0]-x[1], zip(v, u)))
    return vector

def locally_affine(X,U,V):
    # 该函数将原图的点X局部仿射成T(X)
    # 算法：老师提供的局部仿射空间变换公式，这里的仿射区域均为单点
    # input: 原图上的点X,包含所有进行仿射的区域(点)的字典U,它们的对应点的字典V。
    # output: T(X)的坐标[y,x]

    for point in U:  # 判断点X是否属于仿射区域(点)，若是，返回G(X)
        if (X[0] == U[point]['y'])&(X[1] == U[point]['x']):
            b = affine_vector((U[point]['y'],U[point]['x']), (V[point]['y'],V[point]['x']))
            G_X = list(map(lambda x: x[0]+x[1], zip(X, b)))
            return G_X

    T_X = [0,0]
    D2_I_sum = sum([1.0/((U[p]['y']-X[0])**2+(U[p]['x']-X[1])**2) for p in U])
    # srcAnchors = []
    # tarAnchors = []
    for point in U:
        # srcAnchors.append((V[point]['y'], V[point]['x']))
        # tarAnchors.append((U[point]['y'], U[point]['x']))
        b = affine_vector((U[point]['y'],U[point]['x']), (V[point]['y'],V[point]['x']))
        G_X = list(map(lambda x: x[0]+x[1], zip(X, b)))
        d = ((U[point]['y']-X[0])**2+(U[point]['x']-X[1])**2)**0.5
        w = (1.0/d**2) / D2_I_sum
        wG = list(map(lambda x: w*x, G_X))
        T_X = list(map(lambda x: x[0]+x[1], zip(T_X, wG)))
    # print(srcAnchors)
    # print(tarAnchors)
    return T_X

def interpolation(X,img):
    # 在图像上进行双线性插值，得出坐标X的RGB值
    rows, cols, channels = img.shape   
    y, x = X[0], X[1]
    # 判断点是否在两条非轴边界上，若是，则需往原点移动，否则越界。
    if y >= rows-1:
        y -= 1
    if x >= cols-1:
        x -= 1
    i, j = int(x), int(y)
    u, v = x-i, y-j
    # (y,x)左下角的整数像素点坐标为(j,i)
    # v为y和j的差,u为x和i的差
    color = np.zeros(channels, np.float)
    for c in range(channels):
        color[c] = (1-v)*(1-u)*img[j,i][c] + (1-v)*u*img[j,i+1][c] + v*(1-u)*img[j+1,i][c] + v*u*img[j+1,i+1][c]
    return color

# pic = "zxh-face.jpg"
# pic = "zxh-ape.jpg"
pic = 'mario.jpg'
ape = "ape.png"

# 读入人脸数据
face = Image.open(pic)
face = np.array(face.convert('RGB'))

# 读入狒狒脸数据
orangutan = Image.open(ape)
orangutan = np.array(orangutan.convert('RGB'))
rows, cols, channels = orangutan.shape

# 新建狒狒脸的图像，该图像用于重新设置像素点的颜色
orangutan_face = cv2.imread(ape, 1)

# 生成猩猩脸特征点字典U，人脸特征点字典V
# 即进行仿射的区域(点)的字典U,它们的对应点的字典V。
U = get_orangutan_message(rows,cols)
V = get_face_message(pic)

# 对于狒狒图像的每一个像素点
for y in range(rows):
    for x in range(cols):
        T_X = locally_affine((y,x), U, V) #计算该像素点对应到人脸的坐标
        color = interpolation(T_X,face) #双线性插值得出该人脸坐标的RGB值
        orangutan_face[y,x] = color #将狒狒图像像素点的RGB值进行替换

plt.subplot(2,2,1), plt.title('Face')
plt.imshow(face), plt.axis('off')
plt.subplot(2,2,3), plt.title('Orangutan')
plt.imshow(orangutan), plt.axis('off')
plt.subplot(2,2,4), plt.title('Face + Orangutan')
plt.imshow(orangutan_face), plt.axis('off')
plt.show()
