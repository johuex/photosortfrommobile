import threading
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore
from UI.mainwindow import Ui_MainWindow
import os
import shutil


class MainApp(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.folder_in = ""
        self.folder_out = ""
        self.progressBar.setValue(0)
        self.pushButton.pressed.connect(self.select_in)  # select path of input folder
        self.pushButton_2.pressed.connect(self.select_out)  # select path of output folder
        self.pushButton_3.pressed.connect(self.new_thread_sort)  # start sorting
        #self.close(MainApp.Exit(0))

    def select_in(self):
        """
        Select path of input folder
        """
        self.folder_in = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        self.label_3.setText(self.folder_in)
        if self.folder_out != "":
            # add subfolder name in destination
            self.folder_out = self.folder_out+self.folder_in[self.folder_in.rfind("/"):]
            self.label_4.setText(self.folder_out)

    def select_out(self):
        """
        Select path of output folder
        """
        self.folder_out = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        if self.folder_in == "":
            self.label_4.setText(self.folder_out)
        else:
            # add subfolder name in destination
            self.folder_out = self.folder_out + self.folder_in[self.folder_in.rfind("/"):]
            self.label_4.setText(self.folder_out)

    def new_thread_sort(self):
        threading.Thread(target=self.sort).start()

    def sort(self):
        """
        Sorting photos by month/year
        """
        QtCore.QCoreApplication.processEvents()
        if self.folder_in == "":
            self.label_3.setText("SET DIRECTORY!!!")
            return
        if self.folder_out == "":
            self.label_4.setText("SET DIRECTORY!!!")
            return

        # Create target Directory if don't exist
        if not os.path.exists(self.folder_out):
            os.mkdir(self.folder_out)
            print("Directory ", self.folder_out, " Created ")
        else:
            print("Directory ", self.folder_out, " already exists")
        i = 0
        # iterate files in folder
        for filename in os.listdir(self.folder_in):
            count_files = len(os.listdir(self.folder_in)) # for progressbar
            i += 1
            self.progressBar.setValue(int(i//count_files)*100)
            '''THIS METHOD IS ONLY FOR SAMSUNG GALAXY S7'''
            self.label_7.setText(self.folder_in+"/"+filename)
            file_year = filename[:4]
            if file_year.isdigit() is not True:
                continue
            file_month = filename[4:6]
            if file_year.isdigit() is not True:
                continue
            else:
                file_month = file_year + "_" + file_month
            # check year-folder
            if not os.path.exists(self.folder_out+"/"+file_year):
                os.mkdir(self.folder_out+"/"+file_year)
                print("Directory ", self.folder_out, " Created ")
            # check month-folder in year-folder
            if not os.path.exists(self.folder_out+"/"+file_year+"/"+file_month):
                os.mkdir(self.folder_out+"/"+file_year+"/"+file_month)
                print("Directory ", self.folder_out, " Created ")
            temp_out = self.folder_out+"/"+file_year+"/"+file_month
            shutil.copy2(self.folder_in+"/"+filename, temp_out)  # add filename
            if i == count_files:
                self.label_7.setText("Done!")


