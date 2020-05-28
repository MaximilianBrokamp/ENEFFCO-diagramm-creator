from PyQt5 import uic
import sys, os
sys.path.append(os.path.dirname(os.path.abspath("./source_code/ui/icons_rc")))

from source_code.ui import ui_main
import icons_rc

# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("./source_code/ui/error_no_config_files_found.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        # connects
        self.ok_button.clicked.connect(self.ok_button_click)

    def ok_button_click(self):
        self.close()
        ui_main.userinterface.load_or_create_config_window.show()
        ui_main.userinterface.select_config_window.close()

    def close_program(self):
        ui_main.userinterface.close()
