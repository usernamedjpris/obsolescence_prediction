import sys

from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize    
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QApplication, QPushButton
from PyQt5.QtWidgets import QLabel, QComboBox, QVBoxLayout

import numpy as np
import pandas as pd
import pandas as pd
import numpy as np
import os
import math
import matplotlib.pyplot as plt
import csv
from scipy.stats import norm
from scipy.stats import alpha
from scipy.stats import lognorm
from scipy.stats import weibull_min
from scipy.stats import exponweib
from scipy.stats import triang
from scipy.optimize import minimize
from datetime import date

#import optimizer



class MainWindow(QMainWindow):

    
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 200))    
        self.setWindowTitle("PyQt button example - pythonprogramminglanguage.com") 

        
        
        
        pybutton1 = QPushButton('Distribution', self)
        pybutton1.clicked.connect(self.data)
        pybutton1.resize(100,32)
        pybutton1.move(150, 50)
        
        
        pybutton = QPushButton('Prediction', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(100,32)
        pybutton.move(50, 50) 
        
       
        
        
    def close_window(self): 
        MainWindow.destroy()

    def data(self):
        import optimizer
    
    def clickMethod(self):
        import ML_spyder 
        


     
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Obsolescence')
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )