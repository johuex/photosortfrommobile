from PyQt5 import QtWidgets
import MainApp  #ui-class



app = QtWidgets.QApplication([])
window = MainApp()
window.show()
app.exec_()
