import cv2
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import glob
import sys
import time
import os
from keras.models import model_from_json
from sklearn.model_selection import train_test_split
import keras
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, Convolution2D
from keras.models import Sequential
from keras.optimizers import Adam



def load_train_data(path):
    print("Loading training data...")
    start = time.time()

    # load training data
    X = np.empty((0,24,240))
    y = np.empty((0, 3))
    training_data = glob.glob(path)

    # if no data, exit
    if not training_data:
        print("Data not found, exit")
        sys.exit()

    for single_npz in training_data:
        with np.load(single_npz) as data:
            train = data['train']
            train_labels = data['train_labels']
        X = np.vstack((X, train))
        y = np.vstack((y, train_labels))

    print("Train Image array shape: ", X.shape)
    print("Train Label array shape: ", y.shape)

    end = time.time()
    print("Loading data duration: %.2fs" % (end - start))

    # normalize data
    X = X / 255.

    # train validation split, 7:3

    return train_test_split(X, y, test_size=0)




def load_test_data(path):
    print("Loading test data...")
    start = time.time()

    # load training data
    X = np.empty((0,24,240))
    y = np.empty((0, 3))
    test_data = glob.glob(path)

    # if no data, exit
    if not test_data:
        print("Data not found, exit")
        sys.exit()

    for single_npz in test_data:
        with np.load(single_npz) as data:
            test = data['train']
            test_labels = data['train_labels']
        X = np.vstack((X, test))
        y = np.vstack((y, test_labels))

    print("Test Image array shape: ", X.shape)
    print("Test Label array shape: ", y.shape)

    end = time.time()
    print("Loading data duration: %.2fs" % (end - start))

    # normalize data
    X = X / 255.

    # train validation split, 7:3

    return train_test_split(X, y, test_size=0)





class NeuralNetwork(object):
    
    def __init__(self):
        self.model = None
        random.seed(1)  # Using seed to make sure it will generate same weights in every run

    def leNet_model(self):
      # create model
      self.model = Sequential()
      self.model.add(Conv2D(30, (5, 5), input_shape=(24, 240, 1), activation='relu'))# stride is by default=1 (to obtain a detailed feature map), padding isn't used beacuse the digits are centred in the images sı we are not interseted in the borders
      self.model.add(MaxPooling2D(pool_size=(2, 2)))

      self.model.add(Conv2D(15, (3, 3), activation='relu'))
      self.model.add(MaxPooling2D(pool_size=(2, 2)))

      self.model.add(Flatten()) #flatten the data -----> Converting the data to 1D
      self.model.add(Dense(500, activation='relu')) #500= number of nodes in the hidden layer, with higher node number we will need more power
      self.model.add(Dropout(0.5)) #used for fixing the overfitting, 0.5 recommended rate
      self.model.add(Dense(3, activation='softmax')) #define the output layer
      # Compile model
      self.model.compile(Adam(lr = 0.01), loss='categorical_crossentropy', metrics=['accuracy'])
      print(self.model.summary())


    def modified_model(self):
        self.model = Sequential()
        self.model.add(Conv2D(60, (5, 5), input_shape=(24, 240, 1), activation='relu'))
        self.model.add(Conv2D(60, (5, 5), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(30, (3, 3), activation='relu'))
        self.model.add(Conv2D(30, (3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Flatten())
        self.model.add(Dense(500, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(3, activation='softmax'))

        self.model.compile(Adam(lr = 0.001), loss='categorical_crossentropy', metrics=['accuracy'])
        print(self.model.summary())


    def nvidia_model(self):
        self.model = Sequential()
        self.model.add(Convolution2D(24, 5, 5, subsample=(2, 2), input_shape=(24, 240, 1), activation='elu'))
        self.model.add(Convolution2D(36, 5, 5, subsample=(2, 2), activation='elu'))
        self.model.add(Convolution2D(48, 5, 5, subsample=(2, 2), activation='elu'))
        self.model.add(Convolution2D(64, 3, 3, activation='elu'))

        self.model.add(Convolution2D(64, 3, 3, activation='elu'))
    #   model.add(Dropout(0.5))


        self.model.add(Flatten())

        self.model.add(Dense(100, activation = 'elu'))
    #   model.add(Dropout(0.5))

        self.model.add(Dense(50, activation = 'elu'))
    #   model.add(Dropout(0.5))

        self.model.add(Dense(10, activation = 'elu'))
    #   model.add(Dropout(0.5))

        self.model.add(Dense(3))

        optimizer = Adam(lr=1e-3)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        print(self.model.summary())


    def train(self, X_train, y_train, epochs, validation_split, batch_size ):
        # set start time
        start = time.time()

        print("Training ...")
        history=self.model.fit(X_train, y_train, epochs=epochs,  validation_split = validation_split, batch_size = batch_size, verbose = 1, shuffle = 1)

        # set end time
        end = time.time()
        print("Training duration: %.2fs" % (end - start))

        #training graphs
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.legend(['training', 'validation'])
        plt.title('Loss')
        plt.xlabel('epoch')
        plt.show()

        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.legend(['training','validation'])
        plt.title('Accuracy')
        plt.xlabel('epoch')
        plt.show()


    def evaluate(self, X_test, y_test):

        score = self.model.evaluate(X_test, y_test, verbose=1)
        print('Test loss', score[0])
        print('Test accuracy:', score[1])


    def save_model(self):
        model_name = 'model.h5'
        save_dir = os.path.join(os.getcwd(), 'saved_model')
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        model_path = os.path.join(save_dir,model_name)
        self.model.save_weights(model_path)
        print("Saved model.h5 into the disk")

        model_json = self.model.to_json()
        model_json_name = 'model.json'
        model_json_path = os.path.join(save_dir,model_json_name)
        with open(model_json_path, "w") as json_file:
            json_file.write(model_json)
            # serialize weights to HDF5
        print("Saved json model to disk")



    def load_model(self):
        save_dir = os.path.join(os.getcwd(), 'saved_model')
        if not os.path.isdir(save_dir):
            print("Saved model directory is not found")
            sys.exit()

        # load json and create model
        json_file = open(save_dir + '\\' + 'model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        #self.model = model_from_json(loaded_model_json)

        # load weights into new model
        self.model.load_weights(save_dir + '\\' + 'model.h5')
        print("Loaded model from disk")


    def predict(self, X):
        resp = None
        try:
            #print("Making predictions...")
            prediction = self.model.predict_classes(X)
            #print("Predictions are done!")
        except Exception as e:
            print(e)
            prediction=0
        return prediction
