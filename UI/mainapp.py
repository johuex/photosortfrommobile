import threading
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QCoreApplication, QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from UI.mainwindow import Ui_MainWindow
import os
import shutil


class Sorter(QObject):
    progress = Signal(int)
    actual_file = Signal(str)
    completed = Signal(bool)

    @Slot(str, str)
    def sorting(self, input_folder: str, output_folder: str):
        # Create target Directory if don't exist
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
            print("Directory ", output_folder, " Created ")
        else:
            print("Directory ", output_folder, " already exists")
        i = 0
        # iterate files in folder
        for filename in os.listdir(input_folder):  # TODO check what return (only files or with dirs)
            count_files = len(os.listdir(input_folder)) # for progressbar
            i += 1
            progress = int(i/count_files*100)
            self.progress.emit(progress)  # value for progressBar
            
            '''THIS METHOD IS ONLY FOR SAMSUNG GALAXY S7'''
            # TODO work with dynamic mask
            self.actual_file.emit(input_folder+"/"+filename)
            file_year = filename[:4]
            if not file_year.isdigit():
                if not os.path.exists(output_folder + "/not_sorted"):
                    os.mkdir(output_folder + "/not_sorted")
                shutil.copy2(input_folder + "/" + filename, output_folder + "/not_sorted")  # add filename
                continue
            file_month = filename[4:6]
            if not file_year.isdigit():
                if not os.path.exists(output_folder + "/not_sorted"):
                    os.mkdir(output_folder + "/not_sorted")
                shutil.copy2(input_folder + "/" + filename, output_folder + "/not_sorted")  # add filename
                continue
            else:
                file_month = file_year + "_" + file_month
            
            # check year-folder
            if not os.path.exists(output_folder+"/"+file_year):
                os.mkdir(output_folder+"/"+file_year)
                print("Directory ", output_folder, " Created ")
            
            # check month-folder in year-folder
            if not os.path.exists(output_folder+"/"+file_year+"/"+file_month):
                os.mkdir(output_folder+"/"+file_year+"/"+file_month)
                print("Directory ", output_folder, " Created ")
            temp_out = output_folder+"/"+file_year+"/"+file_month
            shutil.copy2(input_folder+"/"+filename, temp_out)  # add filename
            if i == count_files:
                self.actual_file.emit("Done!")
                self.completed.emit(True)


class MainApp(Ui_MainWindow):
    sort_requested = Signal(str, str)
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.folder_in = ""
        self.folder_out = ""
        self.progressBar.setValue(0)
        self.pushButton.pressed.connect(self.select_input)  # select path of input folder
        self.pushButton_2.pressed.connect(self.select_output)  # select path of output folder
        self.pushButton_3.pressed.connect(self.sort)  # start sorting

        self.sorter_worker = Sorter()
        self.sorter_thread = QThread()
        self.sorter_worker.progress.connect(self.update_progress_bar)
        self.sorter_worker.actual_file.connect(self.set_actual_sorting_filename)
        self.sorter_worker.completed.connect(self.sort_completed)

        self.sort_requested.connect(self.sorter_worker.sorting)
        self.sorter_worker.moveToThread(self.sorter_thread)
        self.sorter_thread.start()

    def select_input(self):
        """
        Select path of input folder
        """
        root_folder = '~' if os.name == 'posix' else 'C:\\'
        self.folder_in = QFileDialog.getExistingDirectory(None, 'Select a folder:', root_folder, QFileDialog.ShowDirsOnly)
        self.label_3.setText(self.folder_in)
        if self.folder_out != "":
            # add subfolder name in destination
            self.folder_out = self.folder_out+self.folder_in[self.folder_in.rfind("/"):]
            self.label_4.setText(self.folder_out)

    def select_output(self):
        """
        Select path of output folder
        """
        root_folder = '~' if os.name == 'posix' else 'C:\\'
        self.folder_out = QFileDialog.getExistingDirectory(None, 'Select a folder:', root_folder, QFileDialog.ShowDirsOnly)
        if self.folder_in != "":
            self.label_4.setText(self.folder_out)

    def sort(self):
        """
        Sorting photos by month/year
        """
        QCoreApplication.processEvents()
        if self.folder_in == "":
            self.label_3.setText("SET DIRECTORY!!!")
            return
        if self.folder_out == "":
            self.label_4.setText("SET DIRECTORY!!!")
            return

        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.sort_requested.emit(self.folder_in, self.folder_out)

    def update_progress_bar(self, value: int):
        self.progressBar.setValue(value)
        self.progressBar.repaint()

    def set_actual_sorting_filename(self, value: str):
        self.label_7.setText(value)
    
    def sort_completed(self, value: bool):
        self.pushButton.setEnabled(value)
        self.pushButton_2.setEnabled(value)
        self.pushButton_3.setEnabled(value)
