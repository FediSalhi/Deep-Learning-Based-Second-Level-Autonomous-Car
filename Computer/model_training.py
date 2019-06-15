import model_tr
import numpy as np
from model_tr import load_train_data, load_test_data, NeuralNetwork

train_data_path = "training_data/data.npz"
test_data_path = "training_data/test.npz"

#train configurations
epochs = 12
validation_split = 0.3 
batch_size = 10

np.random.seed(0)

"""
(X_train, y_train) = (train_images, train_labels)
(X_test, y_test) = (test_images, test_labels)
"""

X_train, X_valid, y_train, y_valid = load_train_data(train_data_path)
X_train = X_train[:,:,:, np.newaxis] #, np.newaxis


X_test, X_valid2, y_test, y_valid2 = load_test_data(test_data_path)
X_test = X_test[:,:,:, np.newaxis]


# STOP: Do not change the tests below. Your implementation should pass these tests. 

assert(X_train.shape[0] == y_train.shape[0]), "The number of images in train.npz is not equal to the number of labels."
assert(X_train.shape[1:] == (24,240,1)), "The dimensions of the images are not 120 x 240 x 1."
assert(X_test.shape[0] == y_test.shape[0]), "The number of images in test.npz is not equal to the number of labels."
assert(X_test.shape[1:] == (24,240,1)), "The dimensions of the images are not 120 x 240 x 1."	



model = NeuralNetwork()
#model.leNet_model()
model.modified_model()
model.train(X_train, y_train, epochs, validation_split, batch_size)


#save model
model.save_model()

# evaluate on test data
test_acc = model.evaluate(X_test, y_test) #(test_images, test_labels)


