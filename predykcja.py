
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.models import model_from_json
from keras.models import load_model

from keras.datasets import mnist 
from keras.utils import np_utils 
from keras import layers 
from keras import models 
from keras.utils import to_categorical

from matplotlib.image import imread
import numpy as np

# Wczytanie modelu z pliku
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

loaded_model = model_from_json(loaded_model_json)

# Wczytanie Wag
loaded_model.load_weights("model.h5")

# Wczytanie zdjęcia
img = imread('zdj.png')

# Funkcja przekształcająca zdjęcie kolorowe RGB do skali szarości
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

# Przekształcenie zdjęcia do skali szarości
gray = rgb2gray(img) 

# Przeształcenie zdjęcia do takiej samej stukrtury jak dane uczace, N elementowa lista zdjęć 28x28x1
gray = gray.reshape((1, 28, 28, 1)) 

# użycie modelu do przewidzenia jaki jest liczba na obrazie
prediction = loaded_model.predict(gray)

# wyświetlenie wartości zwróconych przez sieć 
print(prediction)

# wysiwetlenie indeksu najwiekszego elementu 
print(np.argmax(prediction))