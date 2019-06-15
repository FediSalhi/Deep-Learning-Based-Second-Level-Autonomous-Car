import RPi.GPIO as GPIO
from time import sleep 
import spidev
from adafruit_servokit import ServoKit
import adafruit_motor.servo
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import socket

#Raspberry client socket configurations
host = "192.168.0.101"
port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host,port))
message = "START"
client_socket.send(message.encode())

#Raspberry pins mode setting
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#ServoDriver (PCA 9685) configurations
serv_driver_num_of_channels = 16
serv_driver_used_channel = 0
pca_frequency = 50

i2c_bus = busio.I2C(SCL, SDA) # Create the I2C bus interface.
pca = PCA9685(i2c_bus) # Create a simple PCA9685 class instance.
kit = ServoKit(channels=serv_driver_num_of_channels)
pca.frequency = pca_frequency
servo_channel = pca.channels[serv_driver_used_channel]
servo = adafruit_motor.servo.Servo(servo_channel)
kit.servo[0].angle = 70


#Servo angles
max_left_angle = 30
max_right_angle = 110
forward_angle = 70
forward_right_angle = 110
forward_left_angle = 30


#DC motor configurations
Motor1A = 23
Motor1B = 24
Motor1E = 22
duty_cycle = 50

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

pwm = GPIO.PWM(Motor1E, 100)
pwm.start(0)
pwm.ChangeDutyCycle(duty_cycle)


#drive functions

def stop():
    client_socket.send('STOP'.encode())
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.LOW)

def forward():
    client_socket.send('FORWARD'.encode())
    kit.servo[0].angle = forward_angle
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)

def reverse():
    client_socket.send('REVERSE'.encode())
    kit.servo[0].angle = forward_angle
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    
def right():
    client_socket.send('RIGHT'.encode())
    kit.servo[0].angle = max_right_angle
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    
def left():
    client_socket.send('LEFT'.encode())
    kit.servo[0].angle = max_left_angle
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)    

def forward_right():
    client_socket.send('FORWARD_RIGHT'.encode())
    kit.servo[0].angle = forward_right_angle
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)

def forward_left():
    client_socket.send('FORWARD_LEFT'.encode())
    kit.servo[0].angle = forward_left_angle
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)

def reverse_left():
    client_socket.send('REVERSE_LEFT'.encode())
    kit.servo[0].angle = forward_left_angle
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)

def reverse_right():
    client_socket.send('REVERSE_RIGHT'.encode())
    kit.servo[0].angle = forward_right_angle
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)

    

while message.lower().strip != 'bye':
    
    command = client_socket.recv(1024).decode()
    #print('Receieved from server: ' + command)
    
    
    if command == '0':
        print('Receieved from server: STOP')
        stop()
           
    elif command == '1':
        print('Receieved from server: FORWARD')
        forward()
            
    elif command == '2' :
        print('Receieved from server: REVERSE')
        reverse()
           
    elif command == '3' :
        print('Receieved from server: RIGHT')
        right()    
            
    elif command == '4' :
        print('Receieved from server: LEFT')
        left()
            
    elif command == '5' :
        print('Receieved from server: FORWARD RIGHT')
        forward_right()
            
    elif command == '6' :
        print('Receieved from server: FORWARD LEFT')
        forward_left()
            
    elif command == '7' :
        print('Receieved from server: REVERSE LEFT')
        reverse_left()
            
    elif command == '8' :
        print('Receieved from server: REVERSE RIGHT')
        reverse_right()
        
    else:
        print("Invalid Command\n")
            
client_socket.close()
