import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from math import floor
from skimage import transform as tf
from numpy.linalg import norm
from numpy.linalg import inv
from util import *
#The local affine transformation
def local_affine_transformation(ori_img,proto_img,e,regions,is_in_regions,distance_funs,affine_funs):
    new_img = np.zeros(proto_img.shape)
    
    for i in range(new_img.shape[0]):
        for j in range(new_img.shape[1]):

            tmp_point = np.array([i,j])
            flag = is_in_regions(tmp_point,regions)
            if flag >= 0 :
                #When the points is in V_i
                affine_point = affine_funs[flag](tmp_point)
                
                new_img[i][j] = ori_img[int(affine_point[0])][int(affine_point[1])]
            else:
                #When the points is not in V_i
                weights = weight(tmp_point,distance_funs,e)
                #Compute the new position
                affine_point = transform(np.array([i,j]),weights,affine_funs)
                #Compute the value of the pixel value
                new_img[i][j] = linear_interpolation(affine_point,ori_img)
    return new_img

def affine_points_MLS(ori_img,proto_img,ori_points,proto_points,alpha):
    new_img = np.zeros(proto_img.shape)
    for ii in range(new_img.shape[0]):
        for jj in range(new_img.shape[1]):
            # Compute the new position
            v = np.array([ii,jj])
            index = find_index(v,proto_points) 
            if index >= 0:
                new_img[ii][jj] = ori_img[ori_points[index][0]][[ori_points[index][1]]]
                continue
            w = weight_mls(proto_points,v,(alpha))
            w = w.reshape(w.shape[0],1)
            p_star = np.sum(w*proto_points,0)/np.sum(w)
            q_star = np.sum(w*ori_points,0)/np.sum(w)
            p_hat = proto_points - p_star
            q_hat = proto_points - q_star
            t = sum([w[i]*np.outer(p_hat[i].reshape(p_hat[i].shape[0],1),p_hat[i]) for i in range(len(w))])
            tt = inv(t)
            A = np.array([(v-p_star)*w[i]*tt.dot(p_hat[i].reshape(p_hat[i].shape[0],1)) for i in range(len(w))])
            fv = sum([A[j].dot(q_hat[j].reshape(2,1)) for j in range(A.shape[0])]).reshape(2,) + q_star
            # Do the linear interpolation
            new_img[ii][jj] = linear_interpolation(fv,ori_img)
    
    return new_img
#The face++ api 
def detect(path):
    API_KEY = "3o6_lMDRxcpYalXhuXq9cymJeeN7cHCS"
    API_SECRET = "6776wZFWYVfYjwDgS8G_0rmWhtXVyUcW"
    from facepp import API, File
    api = API(API_KEY, API_SECRET)
    result = api.detect(image_file=File(path),return_landmark=1)
    landmarks = result['faces'][0]['landmark']
    new_dict = {}
    for k,v in landmarks.iteritems():
        
        new_dict[k] = np.array([v['y'],v['x']])
    return new_dict
#Preprocess the data and return the useful data for the algorithms
def preprocess(ori_path,proto_path,ori_points_path,proto_points_path,regions_path,distance_item):
    ori_img = Image.open(ori_path)
    proto_img = Image.open(proto_path)
    ori_img = np.array(ori_img)   
    proto_img = np.array(proto_img)
    a = np.array([1.0*ori_img.shape[0]/proto_img.shape[0],1.0*ori_img.shape[1]/proto_img.shape[1]])
    a = np.array([1,1])
    #Load control points data
    try:
        proto_dict = load_data(proto_points_path)
        ori_dict = load_data(ori_points_path)
        
    except BaseException:
        
        return ('The control points format is not correct,please change it'),None
    #Load the regions data we want to use
    try:
        regions = load_region(regions_path)
    except BaseException:
        
        return ('The control regions choose is not correct,please change it'),None

    #For plot the control points on the face which is useless for the GUI and algorithms
    ori_dict_plot = {}
    proto_dict_plot = {}
   
    for region in regions:
        ori_tmp = []
        proto_tmp = []
        for key in region:
            if key not in ori_dict or key not in proto_dict:
                
                return ('The control points format is not correct,please change it'),None
            ori_tmp.append(ori_dict[key])
            proto_tmp.append(proto_dict[key])
        ori_dict_plot[','.join(region)] = ori_tmp
        proto_dict_plot[','.join(region)] = proto_tmp
    #Change the dictionary data to list data
    regions_points = []
    q_regions_points = []
    p_regions_points = []
    affine_funs = []
    affine_dict = {}
    distance_funs = []
    for i,keys in enumerate(regions):
        src = []
        dst = []
        for key in keys:
            if key not in ori_dict or key not in proto_dict:
                
                return ('The control regions choose is not correct,please change it'),None
            
            affine_dict[str(proto_dict[key])] = ori_dict[key]
            src.append(proto_dict[key])
            dst.append(ori_dict[key])
        #For different type of regions do different actions
        if len(keys) == 1:
            regions_points.append(src)
            p_regions_points.append(src[0])
            q_regions_points.append(dst[0])
            affine_funs.append(linear_affine_fun(np.array(dst[0])-np.array(src[0])))
            distance_funs.append(distance_fun(src,distance_item))
        elif len(keys) == 2:
            n=3
            if n < 0:
                regions_points.append(src)
                affine_funs.append(affine_fun(np.array(src),np.array(dst)))
                distance_funs.append(distance_fun(src,distance_item))
            else:
           
                src_aug_points = line_points(src[0],src[1],n)
                dst_aug_points = line_points(dst[0],dst[1],n)
                n = n+1
                for i in range(n):

                    src_tmp = src_aug_points[i:(i+2)]
                    dst_tmp = dst_aug_points[i:(i+2)]
                    
                    regions_points.append(src_tmp)
                    affine_funs.append(similarity_fun(np.array(src_tmp),np.array(dst_tmp)))
                    distance_funs.append(distance_fun(src_tmp,distance_item))
            
        elif len(keys) == 3:
            regions_points.append(src)
            affine_funs.append(affine_fun(np.array(src),np.array(dst)))
            distance_funs.append(distance_fun(src,distance_item))
    return (ori_img,proto_img,regions_points,is_in_regions_fun,distance_funs,affine_funs),(ori_dict_plot,proto_dict_plot,q_regions_points,p_regions_points)

def test_local_affine_transformation(ori_path,proto_path,e):
    (ori_img,proto_img,regions_points,is_in_regions_fun,distance_funs,affine_funs),(ori_dict_plot,proto_dict_plot,q_regions_points,p_regions_points) = preprocess(ori_path,proto_path,'zxh.txt','ape.txt','L2')
    new_img = local_affine_transformation(ori_img,proto_img,e,regions_points,is_in_regions_fun,distance_funs,affine_funs)
    plt.figure()
    plt.imshow(np.uint8(new_img))
    plt.axis('off')
    plt.savefig(str(e)+'trans.png', pad_inches=0, bbox_inches = 'tight')


if __name__ == '__main__':
    ori_path = 'zxh151.png'
    proto_path = 'ape.png'

    detect(ori_path)
    for e in [0.5,1,2,5]:
       test_local_affine_transformation(ori_path,proto_path,e)
