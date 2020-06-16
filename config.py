from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QLineEdit, QPushButton, QMessageBox
import sys
import math
import network

class Aplikacja(QWidget):
    def __init__(self):
        super(Aplikacja, self).__init__()
        
        self.interfejs()
        

    def interfejs(self):

        # etykiety
        etykieta1 = QLabel("Ilość epok", self)
        etykieta2 = QLabel("Batch size", self)
        etykieta3 = QLabel("Ilość neuronów", self)
        
        # przypisanie widgetów do układu tabeli
        ukladT = QGridLayout()
        ukladT.addWidget(etykieta1, 0, 0)
        ukladT.addWidget(etykieta2, 1, 0)
        ukladT.addWidget(etykieta3, 2, 0)
        
        # 1-liniowe pola edycyjne
        self.epoki = QLineEdit()
        self.batch = QLineEdit()
        self.neurony = QLineEdit()           
        

        ukladT.addWidget(self.epoki, 0, 1)
        ukladT.addWidget(self.batch, 1, 1)
        ukladT.addWidget(self.neurony, 2, 1)
        

        # przyciski
        uczBtn = QPushButton("&Stwórz model", self)
        uczBtn.clicked.connect(self.tworzenieModelu)
        uczBtn.resize(uczBtn.sizeHint())

        zamknijBtn = QPushButton("&Zamknij", self)
        zamknijBtn.clicked.connect(quit)

        ukladT.addWidget(uczBtn, 6, 0, 1, 2)
        ukladT.addWidget(zamknijBtn, 7, 1)

        # przypisanie utworzonego układu do okna
        self.setLayout(ukladT)
    
        self.resize(300, 150)
        self.setWindowTitle("Tworzenie Modelu")
        self.show()
    
    def obliczenia(self):

        nadawca = self.sender()

        try:
            x = float(self.epoki.text())
            y = float(self.batch.text())
            z = float(self.neurony.text())
            
            if nadawca.text() == "&Stwórz model":
                network.tworzenieModelu(x, y, z) 
                     

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Błędne dane", QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Aplikacja = Aplikacja()
    sys.exit(app.exec_())