import cv2
import numpy as np
import os


class ObjectDetection(object):

	def __init__(self):
		self.red_light = False
		self.green_light = False
		self.yellow_light = False
		

	def detect(self, cascade_classifier, gray_image, image, idx):

		# read icons 
		stop_icon = cv2.imread('icons/stop_icon.png')
		stop_icon = cv2.resize(stop_icon, (60, 60))

		yaya_icon = cv2.imread('icons/yaya.jpg')
		yaya_icon = cv2.resize(yaya_icon, (60, 60))

		forwardLeft_icon = cv2.imread('icons/ileriden_sol.png')
		forwardLeft_icon = cv2.resize(forwardLeft_icon, (60, 60))

		forward_icon = cv2.imread('icons/forward_icon.png')
		forward_icon = cv2.resize(forward_icon, (60, 60))

		right_icon = cv2.imread('icons/right.jpg')
		right_icon = cv2.resize(right_icon, (60, 60))

		left_icon = cv2.imread('icons/left.jpg')
		left_icon = cv2.resize(left_icon, (60, 60))


		# y camera coordinate of the target point 'P'
		v = 0

		# minimum value to proceed traffic light state validation
		threshold = 150

		# detection
		cascade_obj = cascade_classifier.detectMultiScale(
			gray_image,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30))

		# draw a rectangle around the objects
		for (x_pos, y_pos, width, height) in cascade_obj:
			cv2.rectangle(image, (x_pos + 5, y_pos + 5), (x_pos + width - 5, y_pos + height - 5), (0, 255, 0), 2)
			v = y_pos + height - 5
			

			# stop sign
			if idx == 1:
				#cv2.putText(image, 'DUR', (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				image[0:60, 0:60] = stop_icon

			# yaya_cascade sign
			elif idx == 2:
				#cv2.putText(image, 'Yaya Gecidi', (x_pos, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				image[0:60, 0:60] = yaya_icon
				
			# left_from_forward_cascade sign
			elif idx == 3:
			    #cv2.putText(image, 'Ileriden Sol', (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)    
			    image[0:60, 0:60] = forwardLeft_icon    
				

			# ileri_cascade sign
			elif idx == 4:
			    #cv2.putText(image, 'Ileri', (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)    
			    image[0:60, 0:60] = forward_icon

			# Right Cascade Sign
			elif idx == 5:
				#cv2.putText(image, 'Sag', (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)    
				image[0:60, 0:60] =  right_icon

			# Left Cascade Sign
			elif idx == 6:
				#cv2.putText(image, 'Sol', (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)    
				image[0:60, 0:60] =  left_icon


			# traffic lights
			else:
				roi = gray_image[y_pos + 10:y_pos + height - 10, x_pos + 10:x_pos + width - 10]
				mask = cv2.GaussianBlur(roi, (25, 25), 0)
				(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)

				# check if light is on
				if maxVal - minVal > threshold:
					cv2.circle(roi, maxLoc, 5, (255, 0, 0), 2)

					# Red light
					if (1.0 / 8 * (height - 30) < maxLoc[1] < 4.0 / 8 * (height - 30)):
						cv2.putText(image, 'Red', (x_pos + 5, y_pos - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
						self.red_light = True

					# Green light
					elif 5.5 / 8 * (height - 30) < maxLoc[1] < height - 30:
						cv2.putText(image, 'Green', (x_pos + 5, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),2)
						self.green_light = True

					# yellow light
					# elif 4.0/8*(height-30) < maxLoc[1] < 5.5/8*(height-30):
					#    cv2.putText(image, 'Yellow', (x_pos+5, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
					#    self.yellow_light = True
		return v