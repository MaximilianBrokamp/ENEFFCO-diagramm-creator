from PyQt5 import uic
from source_code.ui import ui_main
from os import listdir
import os.path
from PyQt5 import QtGui
from source_code import load_config
# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("./source_code/ui/select_config.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        self.model = QtGui.QStandardItemModel()
        self.config_files_list.setModel(self.model)
        # connects
        self.cancel_button.clicked.connect(self.cancel_button_click)
        self.ok_button.clicked.connect(self.ok_button_click)
        #parameters
        self.config_files = []
        self.path = None

    def load_config_files(self):
        self.path = os.path.abspath("./configs")
        self.config_files = [f for f in listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        print(self.config_files)
        for i in self.config_files:
            item = QtGui.QStandardItem(str(i))
            self.model.appendRow(item)

    def check_if_config_files_exist(self):
        if self.config_files == []:
            ui_main.userinterface.create_no_config_files_found_error(self)
            return False
        return True

    def ok_button_click(self):
        selected_row = self.config_files_list.currentIndex().row()
        config_file = self.config_files[selected_row]
        config_file_path = os.path.join(self.path, config_file)
        config = load_config.load_config(config_file)
        if config is None:
            ui_main.userinterface.create_not_a_valid_config_file_error(self)
        else:
            ui_main.userinterface.set_config(config)
            ui_main.userinterface.create_edit_config_file_window(self)
            ui_main.userinterface.edit_config_file_window.display_config()
            self.close()


    def cancel_button_click(self):
        self.close()
        ui_main.userinterface.load_or_create_config_window.show()


