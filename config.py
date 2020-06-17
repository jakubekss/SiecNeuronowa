from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QLineEdit, QPushButton, QMessageBox, QFileDialog
import sys
import math
import network
from paint import Paint

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
from keras import layers 
from keras import models 
from keras.utils import to_categorical
from keras import backend as K
from keras.models import model_from_json
from keras.models import load_model
from keras.utils import np_utils 
from matplotlib.image import imread
import numpy as np
from matplotlib import pyplot as plt

class Aplikacja(QWidget):
    def __init__(self):
        super(Aplikacja, self).__init__()
        
        self.interfejs()
        self.paint = Paint(self.predict)
        self.paint.show()  

        self.loaded_model = 0  
        
    def predict(self, image):

        if self.loaded_model == 0:
            pass
        else:
            # użycie modelu do przewidzenia jaki jest liczba na obrazie
            prediction = self.loaded_model.predict(image)

            # wyświetlenie wartości zwróconych przez sieć 
            print(prediction)        

            # wysiwetlenie indeksu najwiekszego elementu 
            self.liczba.setText(str(np.argmax(prediction)))


    def interfejs(self):

        # etykiety
        etykieta1 = QLabel("Ilość epok", self)
        etykieta2 = QLabel("Batch size", self)
        etykieta3 = QLabel("Ilość neuronów", self)        
        etykieta4 = QLabel("Wybierz model",self)
        etykieta5 = QLabel("Wykryta liczba",self)
        etykieta6 = QLabel("Odczytywane pixele", self)
        etykieta7 = QLabel("Nazwa pliku modelu", self)
        etykieta8 = QLabel("Nazwa pliku z wagami", self)

        # przypisanie widgetów do układu tabeli
        ukladT = QGridLayout()
        ukladT.addWidget(etykieta1, 0, 0)
        ukladT.addWidget(etykieta2, 1, 0)
        ukladT.addWidget(etykieta3, 2, 0)
        ukladT.addWidget(etykieta4, 7, 0)
        ukladT.addWidget(etykieta5, 8, 0)
        ukladT.addWidget(etykieta6, 3, 0)
        ukladT.addWidget(etykieta7, 4, 0)
        ukladT.addWidget(etykieta8, 5, 0)

        # 1-liniowe pola edycyjne
        self.epoki = QLineEdit()
        self.batch = QLineEdit()
        self.neurony = QLineEdit()  
        self.pixels = QLineEdit() 
        self.liczba = QLineEdit() 
        self.nmodel = QLineEdit()
        self.nwagi = QLineEdit()
        
        self.liczba.setDisabled(True)     
        

        ukladT.addWidget(self.epoki, 0, 1)
        ukladT.addWidget(self.batch, 1, 1)
        ukladT.addWidget(self.neurony, 2, 1)
        ukladT.addWidget(self.liczba, 8, 1)
        ukladT.addWidget(self.pixels, 3, 1)
        ukladT.addWidget(self.nmodel, 4, 1)
        ukladT.addWidget(self.nwagi, 5, 1)
        

        # przyciski
        wybierzBtn = QPushButton("&Wybierz", self)
        wybierzBtn.clicked.connect(self.wyborSieci)

        uczBtn = QPushButton("&Stwórz model", self)
        uczBtn.clicked.connect(self.tworzenieModelu)
        uczBtn.resize(uczBtn.sizeHint())

        zamknijBtn = QPushButton("&Zamknij", self)
        zamknijBtn.clicked.connect(quit)

        ukladT.addWidget(wybierzBtn, 7, 1)
        ukladT.addWidget(uczBtn, 6, 0, 1, 2)
        ukladT.addWidget(zamknijBtn, 9, 1)

        # przypisanie utworzonego układu do okna
        self.setLayout(ukladT)
    
        self.setGeometry(928, 400, 300, 150)
        self.setWindowTitle("Tworzenie Modelu")
        self.show()

    def wyborSieci(self):
        # Wczytanie modelu z pliku
        json_file, _ = QFileDialog.getOpenFileName(self, "Wybierz model", "", "Modele(*.json)")
        with open(json_file, 'r') as plik:
            loaded_model_json = plik.read()
        
        self.loaded_model = model_from_json(loaded_model_json)

        # Wczytanie wag
        h5_file, _ = QFileDialog.getOpenFileName(self, "Wybierz wagi", "", "Wagi(*.h5)")
        self.loaded_model.load_weights(h5_file)            

                
    def tworzenieModelu(self):

        nadawca = self.sender()

        try:
            epoch = int(self.epoki.text())
            batching = int(self.batch.text())
            neuronsNumber = int(self.neurony.text())
            pixelRead = int(self.pixels.text())
            nmodel = self.nmodel.text()
            nwagi = self.nwagi.text()
            
            if nadawca.text() == "&Stwórz model":
                network.tworzenieModelu(pixelRead, neuronsNumber, epoch, batching, nmodel, nwagi) 
                     

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Błędne dane", QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Aplikacja = Aplikacja()
    sys.exit(app.exec_())