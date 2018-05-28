# -*- coding: utf-8 -*-

import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
import base64
import json



def get_face_message(image_path):

	url='https://api-cn.faceplusplus.com/facepp/v3/detect'
	API_KEY='znU49IIfP_C3jVSuTpHsbkCaE4yIzpLt'
	API_SECRET='E3j5lCz-XZRi6lJPvaiPfIHnuEygxRSA'

	# read image
	open_icon = open(image_path,"rb")
	b64str = base64.b64encode(open_icon.read())
	open_icon.close()

	# use api to detect face message
	para={'api_key':API_KEY,'api_secret':API_SECRET,'image_base64':b64str,'return_landmark':1}
	DATA=urllib.urlencode(para)
	req= urllib.urlopen(url,DATA)
	faceData=json.loads(req.read())

	# face_rectangle example: {'width': 395, 'top': 295, 'height': 395, 'left': 237}
	# 'top': 'y' of upper-left corner; 'left': 'x' of upper-left corner
	face_rectangle=faceData['faces'][0]['face_rectangle']

	# 11 key points totally
	points={}
	points['left_eye_left_corner']=faceData['faces'][0]['landmark']['left_eye_left_corner']
	points['left_eye_right_corner']=faceData['faces'][0]['landmark']['left_eye_right_corner']
	points['right_eye_left_corner']=faceData['faces'][0]['landmark']['right_eye_left_corner']
	points['right_eye_right_corner']=faceData['faces'][0]['landmark']['right_eye_right_corner']
	points['nose_left']=faceData['faces'][0]['landmark']['nose_left']
	points['nose_right']=faceData['faces'][0]['landmark']['nose_right']
	points['mouth_left_corner']=faceData['faces'][0]['landmark']['mouth_left_corner']
	points['mouth_lower_lip_left_contour1']=faceData['faces'][0]['landmark']['mouth_lower_lip_left_contour1']
	points['mouth_lower_lip_top']=faceData['faces'][0]['landmark']['mouth_lower_lip_top']
	points['mouth_lower_lip_right_contour1']=faceData['faces'][0]['landmark']['mouth_lower_lip_right_contour1']
	points['mouth_right_corner']=faceData['faces'][0]['landmark']['mouth_right_corner']

	return (face_rectangle,points)