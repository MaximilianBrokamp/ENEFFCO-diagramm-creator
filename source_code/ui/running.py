from PyQt5 import uic
from PyQt5.QtGui import QColor
from source_code.ui import ui_main
from source_code import check_all_files

from PyQt5 import  QtCore
# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("./source_code/ui/running.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        print("entering running window ini")
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        # connects
        print("connects")
        self.actionQuit.triggered.connect(self.close_program)
        self.terminate_button.clicked.connect(self.terminate_button_click)
        self.pause_button.clicked.connect(self.pause_button_click)
        self.diagram_info.insert(ui_main.userinterface.config.diagram_name)
        print("leaving running window ini")

    def pause_button_click(self):
        if not ui_main.userinterface.pause:
            self.terminate_button.setEnabled(False)
            ui_main.userinterface.pause = True
            self.info_label.clear()
            self.info_label.setText("Will pause after current diagram is finished")
        else:
            self.info_label.clear()
            self.info_label.setText("Programm Running")
            ui_main.userinterface.pause = False
            self.terminate_button.setEnabled(True)

    def terminate_button_click(self):
        if not ui_main.userinterface.end:
            self.pause_button.setEnabled(False)
            ui_main.userinterface.end = True
            self.info_label.clear()
            self.info_label.setText("Will Terminate after current diagram is finished")
        else:
            self.info_label.clear()
            self.info_label.setText("Programm Running")
            ui_main.userinterface.end = False
            self.pause_button.setEnabled(True)

    def close_program(self):
        ui_main.userinterface.close()


