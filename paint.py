from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QAction, QFileDialog, QGridLayout, QLineEdit, QWidget, QDockWidget, QLabel
from PyQt5.QtGui import QImage, QPainter, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt, QPoint
import sys
import qimage2ndarray 
import cv2

import numpy as np

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

epoki = 0

# Funkcja przekształcająca zdjęcie kolorowe RGB do skali szarości
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
 
        title = "Aplikacja do rysowania"
        
        self.setWindowTitle(title)
        self.setGeometry(800, 400, 128, 128)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.black)
          
        self.drawing = False
        self.brushSize = 9
        self.brushColor = Qt.white
        self.lastPoint = QPoint()
 
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("Plik")
        brushSize = mainMenu.addMenu("Rozmiar pisaka")
        brushColor = mainMenu.addMenu("Kolor pisaka")
 
        saveAction = QAction("Zapisz",self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)
 
        clearAction = QAction("Wyczyść", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)
 
        threepxAction = QAction("3px", self)
        brushSize.addAction(threepxAction)
        threepxAction.triggered.connect(self.threePixel)
 
        fivepxAction = QAction("5px", self)
        brushSize.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivePixel)
 
        sevenpxAction = QAction("7px", self)
        brushSize.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenPixel)
 
        ninepxAction = QAction("9px", self)
        brushSize.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninePixel)

 
        blackAction = QAction("Czarny", self)
        blackAction.setShortcut("Ctrl+B")
        brushColor.addAction(blackAction)
        blackAction.triggered.connect(self.blackColor) 
         
        whitekAction = QAction("Biały", self)
        whitekAction.setShortcut("Ctrl+W")
        brushColor.addAction(whitekAction)
        whitekAction.triggered.connect(self.whiteColor) 
 
        redAction = QAction("Czerwony", self)
        redAction.setShortcut("Ctrl+R")
        brushColor.addAction(redAction)
        redAction.triggered.connect(self.redColor)
 
        greenAction = QAction("Zielony", self)
        greenAction.setShortcut("Ctrl+G")
        brushColor.addAction(greenAction)
        greenAction.triggered.connect(self.greenColor)
 
        yellowAction = QAction("Żółty", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColor.addAction(yellowAction)
        yellowAction.triggered.connect(self.yellowColor) 
        
                
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()            
 
 
    def mouseMoveEvent(self, event):
        if(event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    
    def getNumpyImage(self):
        image = self.image.convertToFormat(4)

        width = self.image.width()
        height = self.image.height()

        ptr = self.image.bits()
        ptr.setsize(self.image.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)
        arr = cv2.resize(arr, (28,28))
        return arr
     
    def mouseReleaseEvent(self, event):
 
        if event.button() == Qt.LeftButton:
            self.drawing = False

        numpyImage = self.getNumpyImage()

        # Przekształcenie zdjęcia do skali szarości
        gray = rgb2gray(numpyImage) 

        # Przeształcenie zdjęcia do takiej samej stukrtury jak dane uczace, N elementowa lista zdjęć 28x28x1
        gray = gray.reshape((1, 28, 28, 1)) 

        if epoki == 0:
            pass
        
        else:
            # użycie modelu do przewidzenia jaki jest liczba na obrazie
            prediction = loaded_model.predict(gray)

            # wyświetlenie wartości zwróconych przez sieć 
            print(prediction)

            # wysiwetlenie indeksu najwiekszego elementu 
            print(np.argmax(prediction))

        
    def paintEvent(self, event):
        canvasPainter  = QPainter(self)
        canvasPainter.drawImage(self.rect(),self.image, self.image.rect() )
    
       
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Zapisz obraz", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
 
        if filePath == "":
            return
        self.image.save(filePath) 
 
 
    def clear(self):
        self.image.fill(Qt.black)
        self.update()
 
 
    def threePixel(self):
        self.brushSize = 3
 
    def fivePixel(self):
        self.brushSize = 5
 
    def sevenPixel(self):
        self.brushSize = 7
 
    def ninePixel(self):
        self.brushSize = 9
 
 
    def blackColor(self):
        self.brushColor = Qt.black
 
    def whiteColor(self):
        self.brushColor = Qt.white
 
    def redColor(self):
        self.brushColor = Qt.red
 
    def greenColor(self):
        self.brushColor = Qt.green
 
    def yellowColor(self):
        self.brushColor = Qt.yellow
 
 
 
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()