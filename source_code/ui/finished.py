from PyQt5 import uic
from PyQt5.QtGui import QColor
import os
from source_code.ui import ui_main
from source_code import check_all_files
from PyQt5 import  QtCore
# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("./source_code/ui/finished.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        # connects
        self.actionQuit.triggered.connect(self.close_program)
        self.end_button.clicked.connect(self.close_program)

    def display_report(self):
        self.report_name.insert(ui_main.userinterface.config.report_name)
        report_path = ui_main.userinterface.real_report_path
        report = open(report_path, "r", encoding="utf-8")
        for line in report.readlines():
            self.report_text.insertPlainText(line)
        report.close()

    def close_program(self):
        ui_main.userinterface.close()


