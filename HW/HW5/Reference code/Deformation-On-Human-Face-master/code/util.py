import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from math import floor
from skimage import transform as tf
from numpy.linalg import norm
from numpy.linalg import inv


#Test whether a point is in a region
def is_in_regions_fun(p1,regions):
    for i in range(len(regions)):
        
        if len(regions[i]) == 1:
            if (p1== regions[i][0]).all():
                return i
        elif len(regions[i]) == 2:
            if (p1== regions[i][0]).all() or (p1==regions[i][1]).all()  :
                return i
        elif len(regions[i]) == 3:
            if is_in_triangle(p1,regions[i]):
                return i
    return -1    

def sign(p1,p2,p3):
    return (p1[0]-p3[0])*(p2[1]-p3[1])-(p2[0]-p3[0])*(p1[1]-p1[1])

#Test whether a point is in a triangle
def is_in_triangle(p1,region):
    b1 = sign(p1,region[0],region[1]) < 0.0
    b2 = sign(p1,region[1],region[2]) < 0.0
    b3 = sign(p1,region[2],region[0]) < 0.0
    return ((b1==b2) and (b2==b3))

def find_index(v,proto_points):
    for i,point in enumerate(proto_points):
        if (np.array(point)==v).all():
            return i
    return -1
# weight function for mls method
def weight_mls(points,v,alpha):
    return np.array([1.0/np.sum(np.abs(v-point)**(2*alpha)) for point in points])

#distance function l2 norm
def distance_l2(x,y):
    return np.sqrt(np.sum((np.array(x)-np.array(y))**2))

#distance function l1 norm
def distance_l1(x,y):
    return np.sum(np.abs(np.array(x)-np.array(y)))

#line distance from a point to a line
def line_distance(p1,p2,p3):
    return norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)


#Generate Affine function
def linear_affine_fun(bias):
    def linear_affine_tmp(x):
        return np.array(x)+np.array(bias)
    return linear_affine_tmp

#Similarity Transformation function
def similarity_fun(src,dst):
    tform = tf.estimate_transform('similarity', src, dst)
    def affine_fun(x):
        return tform(x)[0]
    return affine_fun

#Affine Transformation function
def affine_fun(src,dst):
    tform = tf.estimate_transform('affine', src, dst)
    def affine_fun(x):
        return tform(x)[0]
    return affine_fun

#Weights given the points and the distance function
def distance_fun(region,item):
    if item == 'L2':
        distance_ = distance_l2
    elif item == 'L1':
        distance_ = distance_l1
    def distance(p1):
        result = distance_(p1,np.mean(region,0))
        if len(region)==2:
            a = distance_(p1,region[0])
            b = distance_(p1,region[1])
            #result = min(result,a,b)  
        if result == 0:
            return 0.0000001
        return result
    return distance

#Judge where a poiint is on the parallel line
def is_in_parallel(p1,p2,p3):
    vec1 = p1-p2
    vec2 = p1-p3
    vec_line = p2-p3
    if np.sum(vec1*vec_line) < 0 or np.sum(vec2*vec_line) < 0:
        return False
    return True

#line distance function
def distance_line_fun(line):
    def distance(p1):
        dis1 = distance_l2(p1,line[0])
        dis2 = distance_l2(p1,line[1])
        #line_dis = distance_l2(line[0],line[1])
        if not is_in_parallel(p1,line[0],line[1]):
            return min(dis1,dis2)
        else:
            return line_distance(p1,line[0],line[1])
    return distance

#Weight for LAT
def weight(x,distance_funs,e):

    weights = np.array([1.0/(distance(x)**e) for distance in distance_funs])
    #print(weights)
    return weights/np.sum(weights)

#Get the transformed data
def transform(x,weights,affine_funs):
    return np.sum(np.array([affine_fun(x) for affine_fun in affine_funs])*weights.reshape(weights.shape[0],1),0)

# Produce the line points given the start and end point
def line_points(start,end,n):
    x_bin_width = (end[0] - start[0])/(n+1)
    y_bin_width = (end[1] - start[1])/(n+1)
    points = [start]
    for i in range(1,n+2):
        points.append(np.array([start[0]+x_bin_width*i,start[1]+y_bin_width*i]))
    return points
#Save the keypoints
def save_points(name,new_dict):
    outputfile = open(name,'w')
    for k,v in new_dict.iteritems():
        outputfile.write(k+'='+str(v[1])+','+str(v[0])+'\n')

#Load data from the format
def load_data(path):
    points = {}
    with open(path,'r') as reader:
        for line in reader:
            key,value = line.strip().split('=')

            x,y = value.split(',')
            x,y = int(x),int(y)
            points[key] = np.array([y,x])
    return points

#Plot data on faces
def plot(img,points_dict):
    print(points_dict)
    x = []
    y = []
    plt.figure()
    for k,v in points_dict.iteritems():
        if len(v) >= 2:
            for i in range(len(v)-1):
                for j in range(i+1,len(v)):
                    plt.plot([v[i][1],v[j][1]],[v[i][0],v[j][0]],'k')
                    plt.plot([v[i][1],v[j][1]],[v[i][0],v[j][0]],'ro')
        else:
            x.append(v[0][0])
            y.append(v[0][1])

    plt.imshow(img)
    plt.plot(y,x,'ro')
    plt.axis('off')
    #plt.show()
    #print(plt.gcf())
    return plt.gcf()
#Linear interpolation function
def linear_interpolation(location,img):
    x_size,y_size = img.shape[0:2]
    ori_i,ori_j = location
    new_i, u = int(floor(ori_i)),ori_i - floor(ori_i)
    new_j, v = int(floor(ori_j)),ori_j - floor(ori_j)
    #adjust when it is the border 
    new_ii = new_i+1
    new_jj = new_j+1
    if new_i == x_size-1:
        new_ii = new_i
        u = 0
    if new_j == y_size-1:
        new_jj = new_j
        v = 0
    #interpolation assignment
    return (1-u)*(1-v)*img[new_i][new_j]+(1-u)*v*img[new_i][new_jj]+u*(1-v)*img[new_ii][new_j] +u*v*img[new_ii][new_jj]

def load_region(path):
    lines = []
    with open(path,'r') as reader:
        for line in reader:
            terms = line.strip().split(',')
            lines.append(terms)
    return lines 
#change the dictionary to list
def dictToList(oriDict,protoDict):
    oriPoints = []
    protoPoints = []
    
    for key in protoDict:
        protoPoints.append(protoDict[key])
        oriPoints.append(oriDict[key])
    protoPoints = np.array(protoPoints)
    oriPoints = np.array(oriPoints)

    return oriPoints,protoPoints  
