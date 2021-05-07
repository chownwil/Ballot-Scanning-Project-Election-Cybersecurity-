import numpy as np
import keras
from PIL import Image

class DataGenerator(keras.utils.Sequence):
    #need to fix n_classes
    'Generates data for Keras'
    def __init__(self, paths_and_labels, batch_size=32, dim=(32,32,1), n_channels=1,
                 n_classes=10, shuffle=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.labels = paths_and_labels['result'].values
        self.paths =  paths_and_labels['path'].values
        self.list_IDs = range(0,len(self.labels))
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.labels) / self.batch_size))

    def get_file_name(path):
        return 'bubbles_2/' + path[0:5] + '/' + path[6:11] + '/' + path


    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of bubble filenames
        temp_data = [[self.get_file_name(self.paths[k]), self.labels[k]] for k in indexes]

        # Generate data
        X, y = self.__data_generation(temp_data)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, temp_data):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, *self.dim, self.n_channels))
        y = np.array([i[1] for i in temp_data])

        # Generate data
        for i, bubble in enumerate([i[0] for i in temp_data]):
            # Store sample
            X[i,] = np.asarray(Image.open(bubble))

        return X, keras.utils.to_categorical(y, num_classes=self.n_classes)