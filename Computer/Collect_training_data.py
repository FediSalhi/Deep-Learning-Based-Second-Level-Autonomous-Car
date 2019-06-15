import sys
import threading
import socketserver
import numpy as np
import pygame
from time import sleep
import time
import cv2
from pygame.locals import *
import os


class DriveDataHandler(socketserver.BaseRequestHandler):

    def handle(self):

        self.data = " "
        self.send_inst = True


        while (self.send_inst):


            for event in pygame.event.get():

                if event.type == KEYDOWN: # tests if any key is pressed down on the frame started
                    key_input = pygame.key.get_pressed() # pressed key on the frame
                    pygame.event.post(event)

                    if key_input[pygame.K_UP]: # simple orders
                        #forward:
                        self.data =  self.request.recv(1024)
                        #print ("{} wrote:".format(self.client_address[0]))
                        #print(self.data)
                        self.data = "1"
                        self.request.sendall(self.data.encode())

                    elif key_input[pygame.K_RIGHT]:
                        #right:
                        self.data =  self.request.recv(1024)
                        #print ("{} wrote:".format(self.client_address[0]))
                        #print(self.data)
                        self.data = "3"
                        self.request.sendall(self.data.encode())

                    elif key_input[pygame.K_LEFT]:
                        #left:
                        self.data =  self.request.recv(1024)
                        #print ("{} wrote:".format(self.client_address[0]))
                        #print(self.data)
                        self.data = "4"
                        self.request.sendall(self.data.encode())



                    # exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("Exit")
                        self.send_inst = False
                        break

                elif event.type == pygame.KEYUP: # tests if the pressed key on the frame is no longer pressed
                    #self.stop:
                    self.data =  self.request.recv(1024)
                    #print ("{} wrote:".format(self.client_address[0]))
                    #print(self.data)
                    self.data = "0"
                    self.request.sendall(self.data.encode())


class VideoStreamHandler(socketserver.StreamRequestHandler):

    def handle(self):

        #self.input_size = 320 *240

        # create labels
        self.k = np.zeros((3, 3), 'float')
        for i in range(3):
            self.k[i, i] = 1

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print("Start collecting images...")
        print("Press 'q' or 'x' to finish...")
        start = cv2.getTickCount()

        X = np.empty((0,24,240)) # 0-> at the beginning 0 frame, 120 --> height, 240 --_> width

        y = np.empty((0, 3))



        try:
            stream_bytes = b' '
            frame = 1


            # stream video frames one by one
            while True:

                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    gray = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    #image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    #cv2.imshow('image', gray)



                    height, width = gray.shape   # output will be: 120,240
                    gray = gray[int(height/1.25):height, :]
                    cv2.imshow('Image', gray)
                    #temp_array = roi.reshape(1, int(height/2) * width).astype(np.float32)


                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            key_input = pygame.key.get_pressed()

                            # complex orders
                            if key_input[pygame.K_RIGHT]:
                                #print("Right")
                                X = np.vstack((X, gray[np.newaxis,:,:]))
                                y = np.vstack((y, self.k[1]))
                                saved_frame += 1
                                print("saved_frame :", saved_frame)

                            elif key_input[pygame.K_LEFT]:
                                #print("Left")
                                X = np.vstack((X, gray[np.newaxis,:,:]))
                                y = np.vstack((y, self.k[0]))
                                saved_frame += 1
                                print("saved_frame :", saved_frame)
                                
                            elif key_input[pygame.K_UP]:
                                #print("Forward")
                                X = np.vstack((X, gray[np.newaxis,:,:]))
                                y = np.vstack((y, self.k[2]))
                                saved_frame += 1
                                print("saved_frame :", saved_frame)
                                
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("Streaming Stopped")
                        break

            # save data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz', train=X, train_labels=y)
            except IOError as e:
                print(e)

            end = cv2.getTickCount()
            # calculate streaming duration
            print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))

            print(X.shape)
            print(y.shape)
            print("Total frame: ", total_frame)
            print("Saved frame: ", saved_frame)
            print("Dropped frame: ", total_frame - saved_frame)


        finally:
            print("npz data file successfully saved")
            #cv2.destroyAllWindows()
            #sys.exit()


class Server(object):
    def __init__(self, host, port1,port3):
        self.host = host
        self.port1 = port1
        #self.port2 = port2
        self.port3 = port3

        pygame.init()
        pygame.display.set_mode((250, 250))


    def video_stream(self, host, port):

        s = socketserver.TCPServer((host, port), VideoStreamHandler)
        s.serve_forever()

    def sensor_stream(self, host, port):

        s = socketserver.TCPServer((host, port), SensorDataHandler)
        s.serve_forever()

    def drive_stream(self, host, port):

        s = socketserver.TCPServer((host, port), DriveDataHandler)
        s.serve_forever()

    def start(self):
        drive_thread = threading.Thread(target=self.drive_stream, args=(self.host, self.port3))
##        sensor_thread = threading.Thread(target=self.sensor_stream, args=(self.host, self.port2))
##        sensor_thread.daemon = True #this thread will be killed after the main program exits
##        sensor_thread.start()
        drive_thread.daemon = True
        drive_thread.start()

        video_thread = threading.Thread(target=self.video_stream, args=(self.host, self.port1))
        video_thread.daemon = True #this thread will be killed after the main program exits
        video_thread.start()

        #self.video_stream(self.host, self.port1)



if __name__ == '__main__':
    h, p1, p3 = "192.168.0.106", 8000, 8004

    ts = Server(h, p1, p3)
    ts.start()
