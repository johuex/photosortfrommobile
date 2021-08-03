from UI.mainwindow import Ui_MainWindow
import os


class MainApp(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.folder_in = ""
        self.folder_out = ""
        self.pushButton.pressed.connect(self.select_in)  # select path of input folder
        self.pushButton_2.pressed.connect(self.select_out)  # select path of output folder
        self.pushButton_3.pressed.connect(self.sort)  # start sorting

    def select_in(self):
        """
        Select path of input folder
        """
        pass

    def select_out(self):
        """
        Select path of output folder
        """
        pass

    def sort(self):
        """
        Sorting photos by month/year
        """
        pass
