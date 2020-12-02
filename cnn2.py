import numpy as np 
import pandas as pd 

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data
import csv
from torch.autograd import Variable

from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten
from keras.utils import np_utils

#used for the f1-score (get_f1)
from keras.callbacks import Callback,ModelCheckpoint
from keras.wrappers.scikit_learn import KerasClassifier
import keras.backend as K

# to calculate accuracy
from sklearn.metrics import accuracy_score

# to calculate confusion matrix
from sklearn.metrics import confusion_matrix

#an alternative metric to accuracy
def get_f1(y_true, y_pred): #taken from old keras source code
	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
	possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
	predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
	precision = true_positives / (predicted_positives + K.epsilon())
	recall = true_positives / (possible_positives + K.epsilon())
	f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
	return f1_val

def main():
	ydf = pd.read_csv('y.csv')
	Y = ydf['Label'].values
	for i in range(len(Y)):
		if (Y[i] == 4) or (Y[i] == 5):
			Y[i] = 1
		if Y[i] > 5:
			Y[i] -= 2
	
	X = []
	with open("X0.csv", 'r', newline='') as myfile:
		rr = csv.reader(myfile)
		for x in rr:
			x = [int(x_temp) for x_temp in x]
			x = np.reshape(x, (28,28,1))
			X.append(x)
	
	with open("X1.csv", 'r', newline='') as myfile:
		rr = csv.reader(myfile)
		for x in rr:
			x = [int(x_temp) for x_temp in x]
			x = np.reshape(x, (28,28,1))
			X.append(x)
			
	with open("X2.csv", 'r', newline='') as myfile:
		rr = csv.reader(myfile)
		for x in rr:
			x = [int(x_temp) for x_temp in x]
			x = np.reshape(x, (28,28,1))
			X.append(x)
			
	with open("X3.csv", 'r', newline='') as myfile:
		rr = csv.reader(myfile)
		for x in rr:
			x = [int(x_temp) for x_temp in x]
			x = np.reshape(x, (28,28,1))
			X.append(x)

	X_data = np.array(X)
	Y_data = np.array(Y)

	X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=0.15)


	# building the input vector from the 28x28 pixels
	X_train = X_train.astype('float32')
	X_test = X_test.astype('float32')

	# normalizing the data to help with the training 
	X_train /= 255
	X_test /= 255

# one-hot encoding using keras' numpy-related utilities
	n_classes = 7
	print("Shape before one-hot encoding: ", y_train.shape)
	Y_train = np_utils.to_categorical(y_train, n_classes)
	Y_test = np_utils.to_categorical(y_test, n_classes)
	print("Shape after one-hot encoding: ", Y_train.shape)

# building a linear stack of layers with the sequential model
	model = Sequential()
# convolutional layer
	model.add(Conv2D(25, kernel_size=(3,3), strides=(1,1), padding='valid', activation='relu', input_shape=(28,28,1)))
	model.add(MaxPool2D(pool_size=(1,1)))
# flatten output of conv
	model.add(Flatten())
# hidden layer
	model.add(Dense(100, activation='relu'))
# output layer
	model.add(Dense(n_classes, activation='softmax'))

# compiling the sequential model
	model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
	#use [get_f1] to do the f1-score instead of accuracy

# training the model for 10 epochs
	model.fit(X_train, Y_train, batch_size=128, epochs=1, validation_data=(X_test, Y_test))
	pred_probs = model.predict(X_test)

	pred_labels = pred_probs.argmax(axis=-1)
	cm = confusion_matrix(y_test, pred_labels)
	print(cm)

	model.save('cnn2_model')


if __name__ == "__main__":
	main()
