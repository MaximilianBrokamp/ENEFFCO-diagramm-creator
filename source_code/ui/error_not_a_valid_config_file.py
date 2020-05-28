from PyQt5 import uic
import sys, os
sys.path.append(os.path.dirname(os.path.abspath("./source_code/ui/icons_rc")))
from source_code.ui import ui_main
import icons_rc
# load ui file

baseUIClass, baseUIWidget = uic.loadUiType("./source_code/ui/error_not_a_valid_config_file.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        self.previous_window = None
        # connects
        self.ok_button.clicked.connect(self.ok_button_click)

    def ok_button_click(self):
        self.previous_window.setEnabled(True)

    def close_program(self):
        ui_main.userinterface.close()
