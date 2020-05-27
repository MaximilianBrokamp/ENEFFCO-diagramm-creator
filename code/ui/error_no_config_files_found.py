from PyQt5 import uic
import icons_rc
from code.ui import ui_main

# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("./code/ui/error_no_config_files_found.ui")

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
