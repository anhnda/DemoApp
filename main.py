# from PyQt5 import QtWidgets
import os.path
import sys
from gui_file import Ui_MainWindow
from opt_gui import Ui_Dialog
from gplt import Ui_popDialog
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QApplication, QVBoxLayout
from PyQt5.QtCore import QTranslator, QCoreApplication
from matplotlib.backends.backend_qtagg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
# import numpy as np
import time
import importlib
from numpy import linspace
from numpy import sin
from PyQt5.QtGui import QFont

class GUIX:
    def __init__(self, app : QApplication):
        self.app = app
        self.mainWindow = QMainWindow()
        self.uiWinDow = Ui_MainWindow()

        self.mainWindow.openFileDialog = self.openFileDialog
        self.mainWindow.myclick = self.myclick
        self.mainWindow.setting = self.openSetting
        self.mainWindow.xplot = self.xplot
        self.mainWindow.changLanguage = self.changeLanguage
        self.translator = QTranslator()
        # file = "/Users/anhnd/PycharmProjects/QTGUI" +"/rr.qm"
        # print(file)
        # print(translator.load(file))
        # print("R", translator.translate("MainWindow", "MainWindow"))
        self.app.installTranslator(self.translator)
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

    def changeLanguage(self, b):
        if not b:
            return
        sender = self.mainWindow.sender()
        print(sender.objectName())
        if sender.objectName().startswith("en"):
            self.translator.load("")
        else:
            path = os.path.dirname(os.path.abspath(__file__)) +"/langx/rr.qm"
            print(path)
            self.uiWinDow.textBrowser.setText(path + " + " + self.app.applicationDirPath())

            print(self.translator.load(path))
        # self.app.installTranslator(self.translator)
        self.uiWinDow.retranslateUi(self.mainWindow)
    def xplot(self):
        dialog = QDialog()
        ui_plotDialog = Ui_popDialog()
        ui_plotDialog.setupUi(dialog)
        layout = QVBoxLayout(ui_plotDialog.widget)
        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        layout.addWidget(NavigationToolbar(dynamic_canvas, ui_plotDialog.widget))


        # self._static_ax = static_canvas.figure.subplots()
        # t = np.linspace(0, 10, 501)
        # self._static_ax.plot(t, np.tan(t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        t = linspace(0, 10, 101)
        # Set up a Line2D.
        self._line, = self._dynamic_ax.plot(t, sin(t + time.time()))
        self._timer = dynamic_canvas.new_timer(50)
        self._timer.add_callback(self._update_canvas)
        self._timer.start()
        def func(event):
            self._timer.stop()
            print("Close ")
            return event.accept()
        dialog.closeEvent = lambda event : func(event)

        dialog.exec_()

    def plot(self):
        layout = QVBoxLayout(self.uiWinDow.widget)
        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        layout.addWidget(NavigationToolbar(dynamic_canvas, self.uiWinDow.widget))

        # self._static_ax = static_canvas.figure.subplots()
        # t = np.linspace(0, 10, 501)
        # self._static_ax.plot(t, np.tan(t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        t = linspace(0, 10, 101)
        # Set up a Line2D.
        self._line, = self._dynamic_ax.plot(t, sin(t + time.time()))
        self._timer = dynamic_canvas.new_timer(50)
        self._timer.add_callback(self._update_canvas)
        self._timer.start()

    def _update_canvas(self):
        t = linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._line.set_data(t, sin(t + time.time()))
        self._line.figure.canvas.draw()


if __name__ == "__main__":
    if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
        import pyi_splash
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()

    # QFont.setPixelSize(5)
    app = QApplication(sys.argv)

    guix = GUIX(app)
    guix.show()

    sys.exit(app.exec_())
