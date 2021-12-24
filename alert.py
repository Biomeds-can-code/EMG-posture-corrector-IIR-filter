import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setGeometry(800,300,400,300)

        self.layout = QVBoxLayout()
        self.label = QLabel("Correct Posture!")
        self.label.setFont(QFont('Times font', 30))
        self.label.move(200,300)
        self.label.setStyleSheet("background-color: lightgreen; color: black; border: 1px solid black")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.layout.addWidget(self.label)
        self.setWindowTitle("Sitting properly")
        self.setLayout(self.layout)
        

class AlertWindow(QWidget):

    def __init__(self):
        super(AlertWindow, self).__init__()
        
        self.setGeometry(400,300,400,300)

        self.layout = QVBoxLayout()
        self.label = QLabel("Stop Slouching!")
        self.label.setFont(QFont('Times font', 30))
        self.label.move(200,300)
        self.label.setStyleSheet("background-color: red; color: white; border: 1px solid black")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.layout.addWidget(self.label)
        self.setWindowTitle("Alert")
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    aw = AlertWindow()
    aw.show()
    sys.exit(app.exec_())
