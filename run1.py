from PyQt5 import QtWidgets
import sys
from gui_file import Ui_MainWindow
from opt_gui import Ui_Dialog
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog


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



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    guix = GUIX()
    guix.show()

    sys.exit(app.exec_())
