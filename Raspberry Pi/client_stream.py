import io
import socket
import struct
import time
import picamera

# Create and Connect a client socket to my_server:8000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.100', 8000))

#Create a connection to a file-like object
connection = client_socket.makefile('wb')


try:
    with picamera.PiCamera() as camera:  #create a camera object
        camera.resolution = (320, 240)   # pi camera resolution
        camera.start_preview()           # Start a preview 
        camera.framerate = 15            # 15 frames/sec
        time.sleep(2)                    # wait 2 seconds for camera to warm-up

        #The start time and construct a stream to hold image data temporarily 
        start = time.time()                              # beginning time
        my_stream = io.BytesIO()               # created a file-like object


         # send jpeg format images to video stream
        for foo in camera.capture_continuous(my_stream, format= 'jpeg', use_video_port = True):
            # Write the length of the capture to the stream. tell() return the current stream position.
            connection.write(struct.pack('<L', stream.tell()))# "<" = little-endian, Byte Order Specifiers for struct
            print(stream.tell())
            print(struct.pack('<L', stream.tell()))
            
            connection.flush()          #flush to ensure it actually gets
            stream.seek(0)              # Rewind the stream, Change the stream position to the given byte offset.
                                                        # If the parameters is 0, offset should be zero or positive
                                                        
            connection.write(stream.read())#send the image data
            
            # If we've been capturing for more than 10 minutes, quit
            if time.time() - start > 600:               
                break

            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()    # Resize the stream to the given size in bytes
                                                #The current stream position is not changed unless the resizing is expanding the stream
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))#If the length is 0, the connection should be closed.
    
finally:
    connection.close()
    client_socket.close()    
    
