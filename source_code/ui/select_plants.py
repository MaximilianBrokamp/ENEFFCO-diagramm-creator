from PyQt5 import QtGui
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem
from source_code.ui import ui_main
from source_code import extract_plants
import sip
# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("./source_code/ui/select_plants.ui")

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
        self.all_plants_as_list = None
        self.all_plants_as_tree = None

    def show_loading(self):
        ui_main.userinterface.create_loading_window()
        self.setEnabled(False)

    def hide_loading(self):
        ui_main.userinterface.loading_window.close()
        self.setEnabled(True)

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



        #ui_main.userinterface.get_all_plants_wrapper()
    def add_ignore_item(self):
        ignore_item = self.ignore_item_input.displayText()
        if ignore_item == "":
            return
        self.listWidget.addItem(str(ignore_item))

    def load_plant_tree(self, tree_list):
        tree = self.plants_tree
        #tree.clear()
        head = QTreeWidgetItem(tree)
        head.setFlags(head.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        head.setCheckState(0, Qt.Unchecked)
        head.setText(0, "Alle Anlagen")
        for element in tree_list:
            item = QTreeWidgetItem(head)
            item.setText(0, element[0])
            item.setFlags(item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Unchecked)
            if type(element) == list:
                self.add_element_to_tree(element[1], item)

    def update_tree(self):
        self.plants_tree.clear()
        self.load_plant_tree(self.all_plants_as_tree)

    def add_element_to_tree(self, element, parent_item):
        for e in element:
            item = QTreeWidgetItem(parent_item)
            if type(e) == list:
                item.setText(0, e[0])
                item.setFlags(item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                item.setCheckState(0, Qt.Unchecked)
                self.add_element_to_tree(e[1], item)
            else:
                item.setText(0, e)
                item.setFlags(item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                item.setCheckState(0, Qt.Unchecked)


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
        self.show_loading()
        self.setEnabled(False)
        ui_main.userinterface.get_plants_with_exiting_diagram_wrapper()

    def filtered_finished(self):
        ui_main.userinterface.threadpool.clear()
        self.hide_loading()

    def filtered_result(self, result):
        tree = self.all_plants_as_tree
        i = 0
        while i < len(tree):
            element = tree[i]
            self.remove_elements_from_tree(element, result)
            i += 1
        for element in tree:
            if type(element) == list:
                if element[1] == []:
                    tree.remove(element)
                else:
                    for e in element[1]:
                        if type(e) == list:
                            if e[1] == []:
                                element[1].remove(e)

        self.update_tree()

    def remove_elements_from_tree(self, tree, remove_list):
        k = 0
        while k < len(tree):
            if type(tree[k]) == list:
                if tree[k] != []:
                    self.remove_elements_from_tree(tree[k], remove_list)
            else:
                i = 0
                while i < len(tree):
                    j = 0
                    if type(tree[i]) == list:
                        self.remove_elements_from_tree(tree[i], remove_list)
                        i += 1
                        continue
                    while j < len(remove_list):
                        if remove_list[j] == tree[i]:
                            tree.remove(remove_list[j])
                            remove_list.remove(remove_list[j])
                            i -= 1
                            break
                        j += 1
                    i += 1
            k += 1

    def cancel_click(self):
        if ui_main.userinterface.edit_config_file_window is not None:
            ui_main.userinterface.edit_config_file_window.setEnabled(True)
            self.hide()

    def get_selected_items(self):
        selected_list = []
        tree = self.plants_tree
        root = tree.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            retult = self.get_child_list(item)
            selected_list = selected_list + retult
        return selected_list

    def get_child_list(self, item):
        list = []

        child_count = item.childCount()
        if child_count > 0:
            for i in range(child_count):
                new_item = item.child(i)
                result = self.get_child_list(new_item)
                list = list + result
        else:
            if item.checkState(0) == 2:
                list.append(item.text(0))
        return list

    def save_click(self):
        ignore_list = []
        for index in range(self.listWidget.count()):
            ignore_list.append(self.listWidget.item(index).text())

        valid_selected_items = []
        selected_items = self.get_selected_items()
        all_plants = self.all_plants_as_list
        for item in selected_items:
            if item in all_plants:
                valid_selected_items.append(item)

        ui_main.userinterface.config.ignore_list = ignore_list
        ui_main.userinterface.config.select_list = valid_selected_items

        if ui_main.userinterface.edit_config_file_window is not None:
            ui_main.userinterface.edit_config_file_window.setEnabled(True)
            self.hide()

    def close_program(self):
        ui_main.userinterface.close()

