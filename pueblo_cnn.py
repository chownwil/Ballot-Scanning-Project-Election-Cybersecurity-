import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import sys
import cv2
import os
from PIL import Image

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, plot_confusion_matrix

from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten
from keras.utils import np_utils
from keras.callbacks import Callback,ModelCheckpoint
from keras.wrappers.scikit_learn import KerasClassifier
import keras.backend as K
from data_class import DataGenerator

#an alternative metric to accuracy
def get_f1(y_true, y_pred): #taken from old keras source code
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

def get_pueblo_data():
    paths_and_labels = pd.read_csv('labels_all.csv')
    Y = paths_and_labels['result'].values
    paths = paths_and_labels['path'].values
    Filter = []
    for i, value in enumerate(Y):
        Filter.append(value != 5)
        if value == 3:
	        Y[i] = 2
        elif value == 4:
	        Y[i] = 3
        elif value == 6:
	        Y[i] = 1
    Y = Y[Filter]
    paths = paths[Filter]
    return [('bubbles_2/' + i[0:5] + '/' + i[6:11] + '/' + i) for i in paths], np.array(Y)


def get_model(metric, n_classes):
# building a linear stack of layers with the sequential model
    model = Sequential()
# convolutional layer
    model.add(Conv2D(25, kernel_size=(3,3), strides=(1,1), padding='valid', activation='relu', input_shape=(50,50,1)))
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

    print('Metric: ', metric)
    print('Batch Size: ', batch_size)
    print('Epochs: ', epochs)
    print('Confidence: ', confidence)

    bubble_files, Y_data = get_pueblo_data()
    X_data = []
    
    for bubble in bubble_files:
        img = np.asarray(Image.open(bubble))
        X_data.append(img)
    X_data = np.array([np.reshape(x, (50,50,1)) for x in X_data])

    print(X_data.shape)
    X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=0.15)
    
    # building the input vector from the 28x28 pixels
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')

    # normalizing the data to help with the training
    X_train /= 255
    X_test /= 255

    # one-hot encoding using keras' numpy-related utilities
    #0, (1,6), (2,3), 4, ignore 5
    n_classes = 4
    
    print("Shape before one-hot encoding: ", y_train.shape)
    Y_train = np_utils.to_categorical(y_train, n_classes)
    Y_test = np_utils.to_categorical(y_test, n_classes)
    print("Shape after one-hot encoding: ", Y_train.shape)

    model = get_model(metric, n_classes)
    kick_count, accuracy = train_model(model, X_train, Y_train, X_test, Y_test, y_test, batch_size, epochs, confidence)
    print('Kick Count: ', kick_count, 'out of ', len(y_test))
    print('Accuracy: ', accuracy)
	
    model.save('cnn_model_pueblo')


    #pred_probs = model.predict(X_data)
    #pred_labels = pred_probs.argmax(axis=-1)


if __name__ == "__main__":
    main()
