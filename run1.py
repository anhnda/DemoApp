from PyQt5 import QtWidgets
import sys
from gui_file import Ui_MainWindow
from opt_gui import Ui_Dialog
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog

from matplotlib.backends.backend_qtagg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import numpy as np
import time

class GUIX:
    def __init__(self):
        self.mainWindow = QMainWindow()
        self.uiWinDow = Ui_MainWindow()

        self.mainWindow.openFileDialog = self.openFileDialog
        self.mainWindow.myclick = self.myclick
        self.mainWindow.setting = self.openSetting

        self.uiWinDow.setupUi(self.mainWindow)

    def show(self):
        self.mainWindow.show()

    def myclick(self):
        print("My click")

    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self.mainWindow, "QFileDialog.getOpenFileName()", "", "All Files (*)",
                                                  options=options)
        if fileName:
            self.uiWinDow.textBrowser.setText("Current file: " + fileName)

    def openSetting(self):
        dialog = QDialog()
        optionUI = Ui_Dialog()
        optionUI.setupUi(dialog)
        optionUI.lineEdit.setText(self.uiWinDow.label.text())
        re = dialog.exec_()
        print("Res: ", re)
        if re == QDialog.Accepted:
            text = optionUI.lineEdit.text()
            self.uiWinDow.label.setText(text)
        del optionUI
        self.plot()

    def plot(self):
        layout = QtWidgets.QVBoxLayout(self.uiWinDow.widget)
        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        layout.addWidget(NavigationToolbar(dynamic_canvas, self.uiWinDow.widget))

        # self._static_ax = static_canvas.figure.subplots()
        # t = np.linspace(0, 10, 501)
        # self._static_ax.plot(t, np.tan(t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        t = np.linspace(0, 10, 101)
        # Set up a Line2D.
        self._line, = self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._timer = dynamic_canvas.new_timer(50)
        self._timer.add_callback(self._update_canvas)
        self._timer.start()

    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._line.set_data(t, np.sin(t + time.time()))
        self._line.figure.canvas.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    guix = GUIX()
    guix.show()

    sys.exit(app.exec_())
