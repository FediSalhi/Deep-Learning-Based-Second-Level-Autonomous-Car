# Deep-Learning-Based-Second-Level-Autonomous-Car

## Introduction
This project is a try to build a 1:20 scale second level autonomous car controlled by a Raspberry Pi (Client) wirelessly connected to a computer (Server). In this level of autonomy, at least one driver assistance system of  both steering and acceleration using information about the driving environment  is automated, like cruise control and lane-centering.
The understanding of this project requires a basic knowledge of both Convolutional Neural Networks and Python. Having previous experience with electronic circuits will help to understand the wiring schematic of this project. Codes are implemented in Python3, using Keras a high-level machine learning API and OpenCV for image processing.

![Self _driving](https://user-images.githubusercontent.com/45536639/59554886-cd21b600-8fb2-11e9-9a83-31888ca4e149.jpg)

## Principle Of Working
### Lane Centering
A Raspberry Pi collects images from a camera module and send them wirelessly to a computer to feed a Convolutional Neural Network which classifies the images into three classes (Right, left, and forward) . Predictions are then sent to the Raspberry Pi to drive the car accordingly. Collision avoidance is provided by an Ultrasonic Sensor connected to the Raspberry Pi.

![Principle of Working](https://user-images.githubusercontent.com/45536639/59554990-68fff180-8fb4-11e9-833c-b758641e899f.jpg)

### Traffic Signs Detection
Turkish traffic signs detection is done using Haar Cascade classification algorithms. You may use our classifiers or refer to this tutorial (https://coding-robin.de/2013/07/22/train-your-own-opencv-haar-classifier.html) if you want to train your own ones.
An Example of Stop sign detection is shown below:

![dur01](https://user-images.githubusercontent.com/45536639/59555423-a36c8d00-8fba-11e9-83c1-3de0756b33d0.png)
