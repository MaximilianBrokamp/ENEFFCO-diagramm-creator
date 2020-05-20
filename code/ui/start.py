from PyQt5 import  QtWidgets
from PyQt5 import uic
import ui_main
import check_all_files
from PyQt5.QtGui import QColor


# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("start.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        # connects
        self.start_button.clicked.connect(self.button_close)

    # cheks if all necessary files are existing and in the right place
    # it will display the result in a text box
    # if the reult is negative it will also deactivate the "Start" Button and ask the user to close the program
    def display_file_check(self):
        retrun_value = check_all_files.check_all_files()
        if retrun_value[0]:
            self.check_files_text.setTextColor(QColor("darkGreen"))
            self.check_files_text.insertPlainText("All necessary files available \n you can now start")
        #Todo
        # add else case
    def button_close(self):
        ui_main.userinterface.create_login_window(self)
        self.close()




