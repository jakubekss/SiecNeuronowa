import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import pickle
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.datasets import mnist 
from keras import layers 
from keras import models 
from keras.utils import to_categorical

from matplotlib.image import imread
import numpy as np
from matplotlib import pyplot as plt



def tworzenieModelu(pixelRead, neuronsNumber, epoch, batching):

    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    trainImages = X_train.reshape((60000, 28, 28, 1))
    testImages = X_test.reshape((10000, 28, 28, 1))
    print(X_train.shape)

    trainImages = trainImages.astype('float32')/255
    testImages = testImages.astype('float32')/255

    trainLabels = to_categorical(y_train)
    testLabels = to_categorical(y_test)

   
    model = Sequential()
    model.add(Conv2D(10, (pixelRead, pixelRead), padding="same", input_shape=(28, 28, 1), activation="relu"))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
    model.add(Flatten())
    model.add(Dense(neuronsNumber, activation="relu"))
    model.add(Dense(10, activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

    history = model.fit(trainImages, trainLabels, validation_data=(testImages, testLabels), batch_size=batching, epochs=epoch , verbose=1)


    model_json = model.to_json()
    with open('model.json', 'w') as json_file:
        json_file.write(model_json)

    model.save_weights('model.h5')
    print('Model zapisany')


    plt.subplot(2, 1, 1)
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')

    # loss - dla danych treningowych
    # val_loss - dla danych testowych

    # loss/val_loss - Wartość skalarna, którą próbuje sie zminimalizować podczas szkolenia modelu. 
    # Im niższa strata (loss), tym bardziej predykcja modelu jest bliższa prawdziwym etykietom.
    # Jak w regresji - różnica między przewidywaniami, a rzeczywistą wysokością.

    plt.subplot(2, 1, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()