from PyQt5 import uic
from code.ui import ui_main


# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("./code/ui/load_or_create_config.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        # connects
        self.actionQuit.triggered.connect(self.close_program)
        self.load_config_button.clicked.connect(self.load_config_button_click)
        self.create_config_button.clicked.connect(self.create_config_button_click)

    def load_config_button_click(self):
        ui_main.userinterface.create_select_config_window(self)
        self.hide()

    def create_config_button_click(self):
        ui_main.userinterface.create_edit_config_file_window(self)
        self.close()



    def close_program(self):
        if ui_main.userinterface.driver is not None:
            ui_main.userinterface.driver.quit()
        self.close()
        exit(0)