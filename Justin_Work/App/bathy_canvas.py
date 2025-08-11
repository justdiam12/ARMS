import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QGridLayout, QMessageBox, QFileDialog,
    QComboBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Bathy_Canvas(FigureCanvas):
    def __init__(self, parent=None, file_path=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
    

    def update_plot(self, x, y):
        self.plot_canvas.ax.clear()
        self.plot_canvas.ax.plot(x, y)
        self.plot_canvas.draw()

