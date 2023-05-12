from PyQt5 import QtWidgets
from UI.mainapp import MainApp  #ui-class
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
