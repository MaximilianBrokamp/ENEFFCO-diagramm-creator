from PyQt5 import uic
from PyQt5.QtGui import QColor

from source_code.ui import ui_main
from source_code import check_all_files
from PyQt5 import  QtCore
# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("./source_code/ui/start.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        # connects
        self.actionQuit.triggered.connect(self.close_program)
        self.start_button.clicked.connect(self.start_button_click)
    # cheks if all necessary files are existing and in the right place
    # it will display the result in a text box
    # if the reult is negative it will also deactivate the "Start" Button and ask the user to close the program
    def display_file_check(self):
        retrun_value = check_all_files.check_all_files()
        if retrun_value[0]:
            self.check_files_text.setTextColor(QColor("darkGreen"))
            self.check_files_text.insertPlainText("All necessary files available \nyou can now start")
        else:
            self.check_files_text.setTextColor(QColor("red"))
            self.check_files_text.insertPlainText("ERROR: Missing Files\n\nMissing Files:")
            for element in retrun_value[1]:
                self.check_files_text.insertPlainText("\n")
                for key in element:
                    self.check_files_text.insertPlainText("      " + key + ": " + element[key] + "\n")
            self.start_button.setEnabled(False)

    #opens the loading window and closes the current one
    def start_button_click(self):
        ui_main.userinterface.create_login_window(self)
        self.close()
        ui_main.userinterface.init_driver_wrapper()

    def close_program(self):
        ui_main.userinterface.close()


