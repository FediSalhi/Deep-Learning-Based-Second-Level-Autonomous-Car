import sys
import os
import cv2
import threading
import socketserver
import numpy as np
from model import NeuralNetwork

prediction = None
accuracy = None
sensor_data = None

class SensorDataHandler(socketserver.BaseRequestHandler):

	data = " "

	def handle(self):
		global sensor_data

		while self.data:
			self.data = self.request.recv(1024)
			sensor_data = round(float(self.data), 1)
			print("Distance : %0.1f cm\n" % sensor_data)


class VideoStreamHandler(socketserver.StreamRequestHandler):

	# load trained neural network
	model = NeuralNetwork()
	model.modified_model()
	model.load_model()


	# # hard coded thresholds for stopping, sensor 30cm, other two 25cm
	d_sensor_thresh = 15


	def handle(self):
		global prediction
		global sensor_data
	
		stream_bytes = b' '

		try:
			# stream video frames one by one
			while True:
				stream_bytes += self.rfile.read(1024)
				first = stream_bytes.find(b'\xff\xd8')
				last = stream_bytes.find(b'\xff\xd9')
				if first != -1 and last != -1:
					jpg = stream_bytes[first:last + 2]
					stream_bytes = stream_bytes[last + 2:]
					gray = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
					image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

					# lower half of the image
					height, width = gray.shape
					roi = gray[int(height/1.25):height, :]

			
					cv2.imshow('image', image)
					

					# reshape image
					gray = (np.expand_dims(roi,0))
					gray = gray[:,:,:, np.newaxis]

					# neural network makes prediction
					prediction = self.model.predict(gray)
				
					# stop conditions
					if sensor_data and int(sensor_data) < self.d_sensor_thresh:
						print("Dur, Nesne Algılandı...!\n")
						prediction = 4
						sensor_data = None


					if cv2.waitKey(1) & 0xFF == ord('q'):
						print("car stopped")
						break

		finally:
			cv2.destroyAllWindows()
			sys.exit()


class DriveDataHandler(socketserver.BaseRequestHandler):

	def handle(self):

		self.data = " "
		global prediction

		while (True):

			
			if prediction == 2: 
				#forward:
				self.data =  self.request.recv(1024)
				self.data = "1"
				self.request.sendall(self.data.encode())
				print('Forward')

			elif prediction == 1:
				#right:
				self.data =  self.request.recv(1024)
				self.data = "3"
				self.request.sendall(self.data.encode())
				print('Right')

			elif prediction == 0:
			 	#left:
			 	self.data =  self.request.recv(1024)
			 	self.data = "4"
			 	self.request.sendall(self.data.encode())
			 	print('Left')

			else:
				# 	#stop:
				self.data =  self.request.recv(1024)
				self.data = "0"
				self.request.sendall(self.data.encode())
				print("Stop")

			



class Server(object):
	def __init__(self, host, port1, port2, port3):
		self.host = host
		self.port1 = port1
		self.port2 = port2
		self.port3 = port3

	def video_stream(self, host, port):
		s = socketserver.TCPServer((host, port), VideoStreamHandler)
		s.serve_forever()

	def drive_stream(self, host, port):
		s = socketserver.TCPServer((host, port), DriveDataHandler)
		s.serve_forever()

	def sensor_stream(self, host, port):
		s = socketserver.TCPServer((host, port), SensorDataHandler)
		s.serve_forever()	

	def start(self):
		drive_thread = threading.Thread(target=self.drive_stream, args=(self.host, self.port2))
		drive_thread.daemon = True
		drive_thread.start()

		sensor_thread = threading.Thread(target=self.sensor_stream, args=(self.host, self.port3))
		sensor_thread.daemon = True
		sensor_thread.start()

		self.video_stream(self.host, self.port1)


if __name__ == '__main__':
	h, p1, p2, p3 = "192.168.0.100", 8000, 8004, 8006

	ts = Server(h, p1, p2, p3)
	ts.start()




