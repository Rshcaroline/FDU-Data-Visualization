def get_goal_message(image_path=None):

	if image_path==None:
		points={}
		points['left_eye_left_corner']={'y':0.1 ,'x':0.256}
		points['left_eye_right_corner']={'y':0.156,'x':0.444}
		points['right_eye_left_corner']={'y':0.144,'x':0.556}
		points['right_eye_right_corner']={'y':0.089,'x':0.733}
		points['nose_left']={'y':0.711 ,'x': 0.3}
		points['nose_right']={'y': 0.733,'x': 0.644}
		points['mouth_left_corner']={'y': 0.7,'x':0.189 }
		points['mouth_lower_lip_left_contour1']={'y': 0.844,'x': 0.3}
		points['mouth_lower_lip_top']={'y':0.933 ,'x': 0.478}
		points['mouth_lower_lip_right_contour1']={'y':0.911 ,'x':0.667 }
		points['mouth_right_corner']={'y': 0.778,'x': 0.778}

		return points
	else:
		raise Exception("Not implemented yet")