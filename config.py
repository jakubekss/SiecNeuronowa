from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QLineEdit, QPushButton, QMessageBox, QFileDialog
import sys
import math
#import network

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



class Aplikacja(QWidget):
    def __init__(self):
        super(Aplikacja, self).__init__()
        
        self.interfejs()
        

    def interfejs(self):

        # etykiety
        etykieta1 = QLabel("Ilość epok", self)
        etykieta2 = QLabel("Batch size", self)
        etykieta3 = QLabel("Ilość neuronów", self)
        etykieta4 = QLabel("Wybierz model",self)
        etykieta5 = QLabel("Wykryta liczba",self)
        
        # przypisanie widgetów do układu tabeli
        ukladT = QGridLayout()
        ukladT.addWidget(etykieta1, 0, 0)
        ukladT.addWidget(etykieta2, 1, 0)
        ukladT.addWidget(etykieta3, 2, 0)
        ukladT.addWidget(etykieta4, 4, 0)
        ukladT.addWidget(etykieta5, 5, 0)
        
        # 1-liniowe pola edycyjne
        self.epoki = QLineEdit()
        self.batch = QLineEdit()
        self.neurony = QLineEdit()  
        self.liczba = QLineEdit() 
        
        self.liczba.setDisabled(True)     
        

        ukladT.addWidget(self.epoki, 0, 1)
        ukladT.addWidget(self.batch, 1, 1)
        ukladT.addWidget(self.neurony, 2, 1)
        ukladT.addWidget(self.liczba, 5, 1)
        

        # przyciski
        wybierzBtn = QPushButton("&Wybierz", self)
        wybierzBtn.clicked.connect(self.wyborSieci)

        uczBtn = QPushButton("&Stwórz model", self)
        #uczBtn.clicked.connect(self.tworzenieModelu)
        uczBtn.resize(uczBtn.sizeHint())

        zamknijBtn = QPushButton("&Zamknij", self)
        zamknijBtn.clicked.connect(quit)

        ukladT.addWidget(wybierzBtn, 4, 1)
        ukladT.addWidget(uczBtn, 3, 0, 1, 2)
        ukladT.addWidget(zamknijBtn, 6, 1)

        # przypisanie utworzonego układu do okna
        self.setLayout(ukladT)
    
        self.setGeometry(928, 400, 300, 150)
        self.setWindowTitle("Tworzenie Modelu")
        self.show()

    def wyborSieci(self):
        # Wczytanie modelu z pliku
        json_file, _ = QFileDialog.getOpenFileName(self, "Wybierz model", "", "Modele(*.json)")
        #json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()

        loaded_model = model_from_json(loaded_model_json)

        # Wczytanie wag
        h5_file, _ = QFileDialog.getOpenFileName(self, "Wybierz wagi", "", "Wagi(*.h5)")
        loaded_model.load_weights(h5_file)

    
    def tworzenieModelu(self):

        nadawca = self.sender()

        # try:
        #     epoch = float(self.epoki.text())
        #     batching = float(self.batch.text())
        #     neuronsNumber = float(self.neurony.text())
            
        #     if nadawca.text() == "&Stwórz model":
        #         network.tworzenieModelu(epoch, batching, neuronsNumber, ) 
                     

        # except ValueError:
        #     QMessageBox.warning(self, "Błąd", "Błędne dane", QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Aplikacja = Aplikacja()
    sys.exit(app.exec_())