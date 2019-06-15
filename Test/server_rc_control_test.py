import socket
import pygame
from pygame.locals import *

class RCTest(object):


    def __init__(self):
        pygame.init()
        pygame.display.set_mode((250, 250)) #start a 250 by 250 window
        self.send_inst = True
        self.host = '192.168.0.101'
        self.port = 8004
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        self.conn, self.address = self.server_socket.accept()
        print ("Connection from : " + str(self.address))
        self.steer() # this method send command via TCP socket
        data = self.conn.recv(1024).decode()
        print("from connected Raspi : " + str(data))



    def right(self):
        data = self.conn.recv(1024).decode()
        print("from connected Raspi : " + str(data))
        data = "3"
        self.conn.send(data.encode())

    def stop(self):
        data = self.conn.recv(1024).decode()
        print("from connected Raspi : " + str(data))
        data = "0"
        self.conn.send(data.encode())

    def left(self):
        data = self.conn.recv(1024).decode()
        print("from connected Raspi : " + str(data))
        data = "4"
        self.conn.send(data.encode())

    def reverse(self):
        data = self.conn.recv(1024).decode()
        print("from connected Raspi : " + str(data))
        data = "2"
        self.conn.send(data.encode())

    def forward(self):
        data = self.conn.recv(1024).decode()
        print("from connected Raspi : " + str(data))
        data = "1"
        self.conn.send(data.encode())

    def forward_right(self):
        data = self.conn.recv(1024).decode()
        print("from connected Raspi : " + str(data))
        data = "5"
        self.conn.send(data.encode())

    def forward_left(self):
        data = self.conn.recv(1024).decode()
        print("from connected Raspi : " + str(data))
        data = "6"
        self.conn.send(data.encode())

    def reverse_right(self):
        data = self.conn.recv(1024).decode()
        print("from connected Raspi : " + str(data))
        data = "8"
        self.conn.send(data.encode())

    def reverse_left(self):
        data = self.conn.recv(1024).decode()
        print("from connected Raspi : " + str(data))
        data = "7"
        self.conn.send(data.encode())

    
        
        
        

    def steer(self):
        while self.send_inst:
            for event in pygame.event.get():
                if event.type == KEYDOWN: # tests if any key is pressed down on the frame started
                    key_input = pygame.key.get_pressed() # pressed key on the frame

                    # complex orders
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        self.forward_right()

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        self.forward_left()

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        self.reverse_right()

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        self.reverse_left()

                    elif key_input[pygame.K_UP]: # simple orders
                        self.forward()

                    elif key_input[pygame.K_DOWN]:
                        self.reverse()

                    elif key_input[pygame.K_RIGHT]:
                        self.right()
                        

                    elif key_input[pygame.K_LEFT]:
                        self.left()

                    # exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("Exit")
                        self.send_inst = False
                        break

                elif event.type == pygame.KEYUP: # tests if the pressed key on the frame is no longer pressed
                    self.stop()

        conn.close()

# execute RCTest() when this file is invoked directly, if it's imported don't execute RCTest()
if __name__ == '__main__':
    RCTest()
