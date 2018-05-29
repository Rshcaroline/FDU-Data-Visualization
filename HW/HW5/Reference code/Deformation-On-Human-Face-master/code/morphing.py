import numpy as np
import cv2
from PIL import Image
import sys
import matplotlib.pyplot as plt


def readPoints(path) :
    # Create an array of points.
    points = []
    # Read points
    with open(path) as file :
        for line in file :
            x, y = line.split()
            points.append((int(x), int(y)))
    return points

#load the points  from the format we define in readme
def load_data(path):
    points = {}
    with open(path,'r') as reader:
        for line in reader:
            key,value = line.strip().split('=')
            x,y = value.split(',')
            x,y = int(x),int(y)
            points[key] = np.array([x,y])
    return points

#This python file is for morphing 
def affineTransform(src, srcTri, dstTri, size) :
    
    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )
    
    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst


# Generate the triangles by using the opencv subdiv from the control points
def delaunaryTriangles(rect,points):
    #print(points,rect)
    subdiv = cv2.Subdiv2D(rect)
    pointsDict = {}
    #Get the triangle list 
    for i,p in enumerate(points) :

        subdiv.insert((int(p[0]),int(p[1])))
        pointsDict[(int(p[0]),int(p[1]))] = i 
    triangleList = subdiv.getTriangleList();
    
    triangleIndList = []
    #Get the index of the  triangle points
    for t in triangleList :

        pt1 = (int(t[0]), int(t[1]))
        pt2 = (int(t[2]), int(t[3]))
        pt3 = (int(t[4]), int(t[5]))
        
        if pt1 in pointsDict and pt2 in pointsDict and pt3 in pointsDict:
            triangleIndList.append([pointsDict[pt1],pointsDict[pt2],pointsDict[pt3]])
    
    return triangleIndList


#Do deformation on oriImg
def morphing(oriImg,protoImg,oriPoints,protoPoints,alpha):
    oriPoints = addPoints(oriPoints,oriImg)
    protoPoints = addPoints(protoPoints,protoImg)
    newShape = protoImg.shape
    #Get the morph points on M image or newImg
    morphPoints = (1-alpha)*oriPoints + alpha*protoPoints

    triangleIndList = delaunaryTriangles((0,0,newShape[1],newShape[0]),morphPoints)
    newImg = np.zeros(newShape,dtype=protoImg.dtype)
    for row in newImg  :
        for term in row:
            term[3]=255
   
    imgs = [oriImg,protoImg,newImg]
    #For each triangles do the affine transformation
    for tInd in triangleIndList:
        ts = [[],[],[]]
        for i in range(3):
            ts[0].append(np.array(oriPoints[tInd[i]]))
            ts[1].append(np.array(protoPoints[tInd[i]]))
            ts[2].append(np.array(morphPoints[tInd[i]]))
        morphingTriangle(imgs,ts,alpha)
    return imgs[2]


#Add points on the borders
def addPoints(points,img):
    points_ = []
    for point in points:
        points_.append((int(point[0]),int(point[1])))
    y_size,x_size = img.shape[0]-1,img.shape[1]-1
    points_.append((0,int(y_size)))
    points_.append((int(x_size),int(y_size)))
    points_.append((int(x_size),0))
    points_.append((0,0))
    points_.append((0,int(y_size/2)))
    points_.append((int(x_size/2),0))
    points_.append((int(x_size/2),int(y_size)))
    points_.append((int(x_size),int(y_size/2)))
    return np.array(points_)


#Morphing on the triangles 
def morphingTriangle(imgs, ts, alpha):

    #Finding the corresponding rectangles and the images
    recs = []
    recImgs = []
    tRects = [[],[],[]]
    for i,t in enumerate(ts):
        #compute the rectangle boundary of each img
        recs.append(cv2.boundingRect(np.float32([t])))
        # get the corresponding rectangles on the imgs
        recImgs.append(imgs[i][recs[i][1]:(recs[i][1]+recs[i][3]),recs[i][0]:(recs[i][0]+recs[i][2])])
        # get the offsets corrdinates on the recImages
        for j in range(3):
            tRects[i].append(((ts[i][j][0]-recs[i][0]),(ts[i][j][1]-recs[i][1])))

    
    size = (recs[2][2],recs[2][3])
    #Apply the affineTransform function
    affineRec1 = affineTransform(recImgs[0],tRects[0],tRects[2],size)
    affineRec2 = affineTransform(recImgs[1],tRects[1],tRects[2],size)

    #Create the mask
    mask = np.zeros((recs[2][3], recs[2][2], imgs[2].shape[2]), dtype = np.float32)
    cv2.fillConvexPoly(mask,np.int32(tRects[2]),(1.0,1.0,1.0),16,0)

    #compute the morphing value
    morphRec = (1-alpha)*affineRec1 + alpha*affineRec2

    imgs[2][recs[2][1]:recs[2][1]+recs[2][3],recs[2][0]:recs[2][0]+recs[2][2]] = recImgs[2]*(1-mask)+mask*morphRec


#Invoke face++ api to detect the facial keypoints
def detect(path):
    API_KEY = "3o6_lMDRxcpYalXhuXq9cymJeeN7cHCS"
    API_SECRET = "6776wZFWYVfYjwDgS8G_0rmWhtXVyUcW"

    # from facepp import API, File
    # api = API(API_KEY, API_SECRET)
    # result = api.detect(image_file=File(path),return_landmark=1)
    # landmarks = result['faces'][0]['landmark']

    import urllib
    import base64
    import json

    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    # API_KEY = 'znU49IIfP_C3jVSuTpHsbkCaE4yIzpLt'
    # API_SECRET = 'E3j5lCz-XZRi6lJPvaiPfIHnuEygxRSA'

    # read image
    open_icon = open(path, "rb")
    b64str = base64.b64encode(open_icon.read())
    open_icon.close()

    # use api to detect face message
    para = {'api_key': API_KEY, 'api_secret': API_SECRET, 'image_base64': b64str, 'return_landmark': 1}
    DATA = urllib.parse.urlencode(para).encode("utf-8")
    req = urllib.request.urlopen(url, DATA)
    faceData = json.loads(req.read())

    # 16 key points totally
    # points = {}
    # points['left_eye_left_corner'] = faceData['faces'][0]['landmark']['left_eye_left_corner']
    # points['left_eye_center'] = faceData['faces'][0]['landmark']['left_eye_center']
    # points['left_eye_right_corner'] = faceData['faces'][0]['landmark']['left_eye_right_corner']
    # points['right_eye_left_corner'] = faceData['faces'][0]['landmark']['right_eye_left_corner']
    # points['right_eye_center'] = faceData['faces'][0]['landmark']['right_eye_center']
    # points['right_eye_right_corner'] = faceData['faces'][0]['landmark']['right_eye_right_corner']
    # points['nose_left'] = faceData['faces'][0]['landmark']['nose_left']
    # points['nose_right'] = faceData['faces'][0]['landmark']['nose_right']
    # points['nose_tip'] = faceData['faces'][0]['landmark']['nose_tip']
    # points['mouth_left_corner'] = faceData['faces'][0]['landmark']['mouth_left_corner']
    # points['mouth_lower_lip_left_contour2'] = faceData['faces'][0]['landmark']['mouth_lower_lip_left_contour2']
    # points['mouth_lower_lip_left_contour3'] = faceData['faces'][0]['landmark']['mouth_lower_lip_left_contour3']
    # points['mouth_lower_lip_bottom'] = faceData['faces'][0]['landmark']['mouth_lower_lip_bottom']
    # points['mouth_lower_lip_right_contour3'] = faceData['faces'][0]['landmark']['mouth_lower_lip_right_contour3']
    # points['mouth_lower_lip_right_contour2'] = faceData['faces'][0]['landmark']['mouth_lower_lip_right_contour2']
    # points['mouth_right_corner'] = faceData['faces'][0]['landmark']['mouth_right_corner']
    #
    # return (points)

    landmarks = faceData['faces'][0]['landmark']
    print(landmarks)
    keys = [ 'left_eye_right_corner','left_eye_left_corner','right_eye_right_corner','right_eye_left_corner','left_eyebrow_right_corner','right_eyebrow_left_corner',
              'mouth_right_corner','mouth_left_corner','mouth_lower_lip_left_contour2','mouth_lower_lip_left_contour3','mouth_lower_lip_bottom','mouth_lower_lip_right_contour2','mouth_lower_lip_right_contour3','nose_left','nose_right']
    new_dict = {}
    for key in keys:
        v = landmarks[key]
        new_dict[key] = np.array([v['x'],v['y']])

    return new_dict


#The function invoked by the GUI
def morphingAction(ori_path,proto_path,proto_point_path,alpha):
    oriImg = np.array(Image.open(ori_path))
    protoImg = np.array(Image.open(proto_path))
    #Load the protot points data as the dictinary format
    protoDict = load_data(proto_point_path)
    #Get the Facial Keypoints by using face++
    oriDict = detect(ori_path)
    delList = []
    #Delete the key which proto points do not contain
    for key in oriDict:
        if key not in protoDict:
            delList.append(key)
    for key in delList:
        del oriDict[key]
    #change the dictionary to List
    oriPoints = []
    protoPoints = []
    
    for key in protoDict:
        protoPoints.append(protoDict[key])
        oriPoints.append(oriDict[key])
    protoPoints = np.array(protoPoints)
    oriPoints = np.array(oriPoints)

    newImg = morphing(oriImg,protoImg,oriPoints,protoPoints,alpha)
    
    return newImg

#A test example
if __name__ == '__main__':
    ori_path = 'data/zxh_new.png'
    proto_path = 'data/ape.png'
    oriImg = np.array(Image.open(ori_path))
    protoImg = np.array(Image.open(proto_path))
    
    protoDict = load_data('data/ape.txt')
   
    oriDict = detect(ori_path)
    delList = []
    for key in oriDict:
        if key not in protoDict:
            delList.append(key)
    for key in delList:
        del oriDict[key]

    oriPoints = []
    protoPoints = []
    
    for key in oriDict:   # for key in protoDict:
        protoPoints.append(protoDict[key])
        oriPoints.append(oriDict[key])
    protoPoints = np.array(protoPoints)
    oriPoints = np.array(oriPoints)

    
    alphas = [0.5,0.6,0.7,0.8,0.9,1]
    #alphas = [0,0.1,0.2,0.3,0.4]
    for i,alpha in enumerate(alphas):    
        newImg = morphing(oriImg,protoImg,oriPoints,protoPoints,alpha)
        
        plt.subplot(1,len(alphas),i+1)
        plt.imshow(np.uint8(newImg),interpolation=None)
        plt.axis('off')
        
    plt.show()
    