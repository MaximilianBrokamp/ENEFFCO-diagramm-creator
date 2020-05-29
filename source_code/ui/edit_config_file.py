from PyQt5 import uic
from PyQt5 import QtGui
from source_code.ui import ui_main
from source_code import class_diagram, config_to_config_file
import os

# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("./source_code/ui/edit_config_file.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        # connects
        self.actionQuit.triggered.connect(self.close_program)
        self.cancel_button.clicked.connect(self.cancel_button_click)
        self.templates_list.itemSelectionChanged.connect(self.on_row_change)
        self.select_plants_button.clicked.connect(self.select_plants_click)
        self.save_button.clicked.connect(self.save_button_click)
        self.save_and_start_button.clicked.connect(self.save_and_start_button_click)
        self.cancel_button.clicked.connect(self.cancel_button_click)
        #parameters
        self.path = None
        self.templates = None
        self.row_selected = None
        self.missing_information = True

    def load_templates(self):
        self.path = os.path.abspath("./templates")
        self.templates = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        for i in self.templates:
            if i.endswith("EnEffCoDashBoard") or i.endswith("EnEffCoChart"):
                self.templates_list.addItem(str(i))

    def on_row_change(self):
        selected_row = self.templates_list.currentRow()
        template = self.templates[selected_row]
        self.selected_template_edit.clear()
        self.diagram_type_edit.clear()
        self.diagram_name_edit.clear()
        template = template.split(".")
        self.selected_template_edit.insert(template[0])
        self.diagram_type_edit.insert(template[1])
        self.diagram_name_edit.insert(template[0])
        if self.diagram_name_edit.displayText() is not None and self.diagram_name_edit.displayText() != "":
            self.select_plants_button.setEnabled(True)

    def display_config(self):
        config = ui_main.userinterface.config
        if config is None:
            return
        self.selected_template_edit.clear()
        self.diagram_type_edit.clear()
        self.diagram_name_edit.clear()
        self.config_file_name_edit.clear()
        self.report_name_edit.clear()
        self.selected_template_edit.insert(config.template_file)
        self.diagram_type_edit.insert(config.diagram_type)
        self.diagram_name_edit.insert(config.diagram_name)
        config.config_file_name = config.config_file_name.replace(".txt", "")
        self.config_file_name_edit.insert(config.config_file_name)
        self.report_name_edit.insert(config.report_name)
        if self.diagram_name_edit.displayText() is not None and self.diagram_name_edit.displayText() != "":
            self.select_plants_button.setEnabled(True)

    def cancel_button_click(self):
        self.close()
        ui_main.userinterface.load_or_create_config_window.show()

    def select_plants_click(self):
        self.update_config()
        if self.missing_information:
            ui_main.userinterface.create_not_a_valid_config_file_error(self)
            return
        if ui_main.userinterface.select_plants_window is None:
            ui_main.userinterface.create_select_plants_window()
        self.setEnabled(False)
        ui_main.userinterface.select_plants_window.show()

    def update_config(self):
        self.missing_information = False
        config = None
        if ui_main.userinterface.config is None:
            config = class_diagram.diagram()
            ui_main.userinterface.config = config
        else:
            config = ui_main.userinterface.config
        config.diagram_name = self.diagram_name_edit.displayText()
        config.diagram_type = self.diagram_type_edit.displayText()
        config.template_file = str(self.selected_template_edit.displayText() + "." + config.diagram_type)
        config.template_path = os.path.abspath("./templates/" + config.template_file)
        config.report_name = self.report_name_edit.displayText()
        ui_main.userinterface.config_file_name = self.config_file_name_edit.displayText()
        if config.diagram_name is None or config.diagram_name == "":
            self.missing_information = True
        if config.template_file is None or config.template_file == "":
            self.missing_information = True
        if config.template_path is None or config.template_path == "":
            self.missing_information = True
        if config.report_name is None or config.report_name == "":
            self.missing_information = True
        if ui_main.userinterface.config_file_name is None or ui_main.userinterface.config_file_name == "":
            self.missing_information = True
        if ui_main.userinterface.config.select_list == []:
            ui_main.userinterface.config.select_list = ui_main.userinterface.select_plants_window.all_plants_as_list


    def save_and_start_button_click(self):
        self.update_config()
        if self.missing_information:
            ui_main.userinterface.create_not_a_valid_config_file_error(self)
            return
        if ui_main.userinterface.select_plants_window is not None:
            ui_main.userinterface.select_plants_window.close()
            ui_main.userinterface.select_plants_window = None
        ui_main.userinterface.create_running_window(self)
        self.close()

    def save_button_click(self):
        self.update_config()
        if self.missing_information:
            ui_main.userinterface.create_not_a_valid_config_file_error(self)
            return
        config_to_config_file.config_to_config_file(ui_main.userinterface.config, ui_main.userinterface.config_file_name)
        #self.close()

    def cancel_button_click(self):
        if ui_main.userinterface.select_plants_window is not None:
            ui_main.userinterface.select_plants_window.close()
            ui_main.userinterface.select_plants_window = None
        ui_main.userinterface.create_load_or_create_config_window()
        self.close()

    def close_program(self):
        ui_main.userinterface.close()