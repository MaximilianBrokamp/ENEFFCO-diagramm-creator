from PyQt5 import QtGui
from PyQt5 import uic

from code.ui import ui_main

# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("./code/ui/select_plants.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        # connects
        self.actionQuit.triggered.connect(self.close_program)
        self.select_radio_button.toggled.connect(self.radio_button_toggled)
        self.add_button.clicked.connect(self.add_ignore_item)
        self.delete_button.clicked.connect(self.delet_ignore_item)
        self.clear_all_button.clicked.connect(self.clar_ignore_items)
        self.filter_plants.clicked.connect(self.filter_plants_clicked)
        self.save_button.clicked.connect(self.save_click)
        self.cancel_button.clicked.connect(self.cancel_click)

        self.select_radio_button.setChecked(True)
        #prameters
        self.filtered = False
    def radio_button_toggled(self):
        select_state = False
        ignore_state = False
        if self.select_radio_button.isChecked():
            select_state = True
        else:
            ignore_state = True
        self.Items_for_ignore_list_edit.setEnabled(ignore_state)
        self.ignore_item_input.setEnabled(ignore_state)
        self.add_button.setEnabled(ignore_state)
        self.delete_button.setEnabled(ignore_state)
        self.clear_all_button.setEnabled(ignore_state)
        self.listWidget.setEnabled(ignore_state)
        self.filter_plants.setEnabled(select_state)
        self.plants_tree.setEnabled(select_state)

    def add_ignore_item(self):
        ignore_item = self.ignore_item_input.displayText()
        if ignore_item == "":
            return
        self.listWidget.addItem(str(ignore_item))

    def delet_ignore_item(self):
        current_item = self.listWidget.currentItem()
        row = self.listWidget.indexFromItem(current_item).row()
        if current_item is None:
            return
        self.listWidget.takeItem(row)

    def clar_ignore_items(self):
        self.listWidget.clear()

    def filter_plants_clicked(self):
        if self.filtered:
            return
        self.filtered = True
        self.setEnabled(False)
        ui_main.userinterface.create_login_window(self)
        ui_main.userinterface.login_window.wait_for_website()
        ui_main.userinterface.get_plants_with_exiting_diagram_wrapper()

    def filtered_finished(self):
        self.close_program(True)
        ui_main.userinterface.login_window.close()

    def filtered_result(self, result):
        # TODO filter plants
        pass

    def cancel_click(self):
        if ui_main.userinterface.edit_config_file_window is not None:
            ui_main.userinterface.edit_config_file_window.setEnabled(True)
            # TODO Warning
            self.close()

    def save_click(self):
        if ui_main.userinterface.edit_config_file_window is not None:
            ui_main.userinterface.edit_config_file_window.setEnabled(True)
            #TODO Save
            self.close()

    def close_program(self):
        if ui_main.userinterface.driver is not None:
            ui_main.userinterface.driver.quit()
        self.close()
        exit(0)

