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
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.datasets import mnist 
from keras import layers 
from keras import models 
from keras.utils import to_categorical

from matplotlib.image import imread


from paint import Window
from config import Aplikacja

if __name__ == "__main__":
    app = QApplication(sys.argv)
    aplikacja = Aplikacja()
    aplikacja.show()
    window = Window()
    window.show()
    app.exec()