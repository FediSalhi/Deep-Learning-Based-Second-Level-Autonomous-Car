from socket import *
import time
import RPi.GPIO as GPIO
import sys, errno


GPIO.setwarnings(False)

# create a socket and bind socket to the host
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('192.168.0.103', 8002))

# measure distance
def measure():

    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()

    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()

    # The received travel time value 
    elapsed = stop-start  

    # The speed of the sound is 340 m/s or 0.034 cm/µs
    distance = (elapsed * 34000)/4 

    # In order to get the distance in cm, d = (t * 0.034) / 2
    distance_cm = (elapsed * 0.034)/2 

    return distance_cm

# referring to the pins by GPIO numbers
GPIO.setmode(GPIO.BCM)

# define pi GPIO
GPIO_TRIGGER = 15
GPIO_ECHO    = 18

# output pin: Trigger
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)

# input pin: Echo
GPIO.setup(GPIO_ECHO,GPIO.IN)

# initialize trigger pin to low
GPIO.output(GPIO_TRIGGER, False)


try:
    while True:
            
            distance = measure()
            print ("Distance : %.1f cm" % distance)
            # send data to the host every 0.5 second
            client_socket.send(str(distance).encode())
            time.sleep(0.5)
finally:
    client_socket.close()
    GPIO.cleanup()
