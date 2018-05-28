# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import cv2
import numpy as np
from matplotlib import pyplot as plt

def affine_matrix(u1,v1,u2,v2,u3,v3):
    # 该函数利用三对确定的点来求仿射变换矩阵
    # input：6个点的坐标。其中u1、u2、u3是原图的三个点，
    #       v1、v2、v3为它们在另一张图所对应的点。
    # output：3*3的仿射变换矩阵
    x_u1, y_u1, x_v1, y_v1 = u1[0], u1[1], v1[0], v1[1]
    x_u2, y_u2, x_v2, y_v2 = u2[0], u2[1], v2[0], v2[1]
    x_u3, y_u3, x_v3, y_v3 = u3[0], u3[1], v3[0], v3[1]
    
    p = [[x_u1,y_u1,0,0,1,0], [0,0,x_u1,y_u1,0,1],
         [x_u2,y_u2,0,0,1,0], [0,0,x_u2,y_u2,0,1],
         [x_u3,y_u3,0,0,1,0], [0,0,x_u3,y_u3,0,1]]
    p = np.array(p)
    q = [x_v1, y_v1, x_v2, y_v2, x_v3, y_v3]
    q = np.array(q)
    affine_parameter = np.linalg.solve(p,q)
    
    affine_matrix = np.array([[affine_parameter[i] for i in (0,1,4)],
                              [affine_parameter[i] for i in (2,3,5)],
                              [0,0,1]])
    return affine_matrix

class area1(object):
    # area1中包含信息：
    #   1、该区域的仿射变换矩阵 area1().matrix()
    #      (依据的点为原图像的三个点u1、u2、u3以及对应的v1、v2、v3)
    #   2、该区域包含的所有点 area1().domain()
    #   3、某点X到该区域的距离area1().distance(X)
    def __init__(self):
        self.u1 = (1,1)
        self.v1 = (2,2)
        self.u2 = (2,1)
        self.v2 = (3,2)
        self.u3 = (1,2)
        self.v3 = (2,3)
    def matrix(self):
        return affine_matrix(self.u1,self.v1,self.u2,self.v2,self.u3,self.v3)
    def domain(self):
        return [(1,1),(1,2),(2,1),(2,2)] # small_sample
    def distance(self,X):
        return ((X[0]-1.5)**2+(X[1]-1.5)**2)**0.5 # small_sample

class area2(object):
    def __init__(self):
        self.u1 = (4,5)
        self.v1 = (3,4)
        self.u2 = (5,5)
        self.v2 = (4,4)
        self.u3 = (5,4)
        self.v3 = (4,3)
    def matrix(self):
        return affine_matrix(self.u1,self.v1,self.u2,self.v2,self.u3,self.v3)
    def domain(self):
        return [(4,4),(4,5),(5,4),(5,5)] # small_sample
    def distance(self,X):
        return ((X[0]-4.5)**2+(X[1]-4.5)**2)**0.5 # small_sample

        
def locally_affine(X):
    # 该函数将原图的点X局部仿射成T(X)
    # 算法：老师提供的局部仿射空间变换公式
    # output: T(X)的坐标[x,y]
    D = sum(1.0/area().distance(X)**2 for area in (area1, area2))
    T_X = 0
    for area in (area1, area2):
        G_X = np.dot(area().matrix(), np.array([X[0],X[1],1]))[0:2]
        if X in area().domain():
            return list(G_X)
        else:
            d = area().distance(X)
            w = (1.0/d**2) / D
            T_X += w * G_X
    return list(T_X)

T = [range(6) for i in range(6)]
for x in range(6):
    for y in range(6):
        T[x][y] = [round(locally_affine((x,y))[0],2),round(locally_affine((x,y))[1],2)]
print T

'''
img = cv2.imread('ape.jpg', 1)
rows,cols,channel = img.shape



# input与output的位置对比
plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()

'''

# 输出output
'''
cv2.imshow('img',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''


    for point in U:
        b = affine_vector((U[point]['y'],U[point]['x']), (V[point]['y'],V[point]['x']))
        G_X = list(map(lambda x: x[0]+x[1], zip(X, b)))
        if (X[0] == U[point]['y'])&(X[1] == U[point]['x']):
            return G_X
        else:
            D2_I_sum = sum([1.0/((U[p]['y']-X[0])**2+(U[p]['x']-X[1])**2) for p in U])
            d = ((U[point]['y']-X[0])**2+(U[point]['x']-X[1])**2)**0.5
            w = (1.0/d**2) / D2_I_sum
            wG = list(map(lambda x: w*x, G_X))
            T_X = list(map(lambda x: x[0]+x[1], zip(T_X, wG)))
    return T_X