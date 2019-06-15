import numpy as np
import cv2
import socket
import struct
import io


class VideoStreamingTest(object):
    def __init__(self, host, port):

        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.streaming()

    def streaming(self):

        try:
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)
            print("Streaming...")
            print("Press 'q' to exit")

            stream_bytes = b' '
            while True:
                # Read the length of the image as a 32-bit unsigned int.
                # If the length is zero, quit the loop

                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')#if find()method find anything, it returns -1 value.
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:   #if first point and last point find, it runs the proceses.
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    cv2.imshow('image', image)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

        finally:
            self.connection.close()
            self.server_socket.close()
    
if __name__ == '__main__':
    # host, port
    h, p = "192.168.2.171", 8000
    VideoStreamingTest(h, p)
                
