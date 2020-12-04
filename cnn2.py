import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import sys
import cv2

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, plot_confusion_matrix

from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten
from keras.utils import np_utils
from keras.callbacks import Callback,ModelCheckpoint
from keras.wrappers.scikit_learn import KerasClassifier
import keras.backend as K

#an alternative metric to accuracy
def get_f1(y_true, y_pred): #taken from old keras source code
	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
	possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
	predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
	precision = true_positives / (predicted_positives + K.epsilon())
	recall = true_positives / (possible_positives + K.epsilon())
	f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
	return f1_val

def get_X_and_Y():
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
	
	breakpoint()
	ptdf = pd.read_csv('pages.csv')
	remove = []
	for i in range(len(Y_data)):
		if ptdf['PageType'][ptdf['JPGNumber'] == ydf['JPG'][i]].to_numpy()[0] == 'Sherry Dalziel':
			remove.append(i)
	breakpoint()
	X_data = np.delete(X_data, remove, axis=0)
	Y_data = np.delete(Y_data, remove, axis=0)
	breakpoint()
	return X_data, Y_data

def get_model(metric, n_classes):
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
	if metric == 'accuracy':
		model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
	elif metric == 'f1':
		model.compile(loss='categorical_crossentropy', metrics=[get_f1], optimizer='adam')
	return model

def train_model(model, X_train, Y_train, X_test, Y_test, y_test, batch_size, epochs, confidence):
	# training the model for 10 epochs
	model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs, validation_data=(X_test, Y_test))
	breakpoint()
	pred_probs = model.predict(X_test)
	pred_labels = pred_probs.argmax(axis=-1)
	count = 0
	for i in range(len(pred_probs)):
		if pred_probs[i][pred_labels[i]] <= confidence:
			pred_labels[i] = y_test[i]
			count += 1
	cm = confusion_matrix(y_test, pred_labels)
	accuracy = np.trace(cm)/np.sum(cm)
	print(cm)
	plt.imshow(cm/cm.sum(axis=1, keepdims=True), cmap='hot', interpolation='nearest')
	plt.show()

	return count, accuracy

def main():
	print("Starting model...")
	metric = 'accuracy'
	batch_size = 32
	epochs = 10
	confidence = 0

	for i in range(0, len(sys.argv)):
		if sys.argv[i] == '-m':
			metric = sys.argv[i + 1]
		elif sys.argv[i] == '-b':
			batch_size = int(sys.argv[i + 1])
		elif sys.argv[i] == '-e':
			epochs = int(sys.argv[i + 1])
		elif sys.argv[i] == '-c':
			confidence = float(sys.argv[i + 1])

	print('Metric: ', metric)
	print('Batch Size: ', batch_size)
	print('Epochs: ', epochs)
	print('Confidence: ', confidence)

	X_data, Y_data = get_X_and_Y()

	X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=0.15)


	# building the input vector from the 28x28 pixels
	X_train = X_train.astype('float32')
	X_test = X_test.astype('float32')

	# normalizing the data to help with the training
	X_train /= 255
	X_test /= 255

# one-hot encoding using keras' numpy-related utilities
	n_classes = 7
	#n_classes = 9
	print("Shape before one-hot encoding: ", y_train.shape)
	Y_train = np_utils.to_categorical(y_train, n_classes)
	Y_test = np_utils.to_categorical(y_test, n_classes)
	print("Shape after one-hot encoding: ", Y_train.shape)

	model = get_model(metric, n_classes)
	kick_count, accuracy = train_model(model, X_train, Y_train, X_test, Y_test, y_test, batch_size, epochs, confidence)
	print('Kick Count: ', kick_count, 'out of ', len(y_test))
	print('Accuracy: ', accuracy)

	# Change this back
	model.save('cnn2_model_sherry_dalziel')

	# Remove after this line

	#FIX ME change filepath
	img = cv2.imread("bubbles_final/014205_0_0_4.jpg", cv2.IMREAD_GRAYSCALE) 

	bubbles = []

	bubbles.append(img)

	X = [cv2.resize(bubble, (28, 28)) for bubble in bubbles]

	X = [np.reshape(x, (28,28,1)) for x in X]

	X_data = np.array(X)
	breakpoint()

	X_data = X_data.astype('float32')
	X_data /= 255

	pred_probs = model.predict(X_data)
	pred_labels = pred_probs.argmax(axis=-1)


if __name__ == "__main__":
	main()
