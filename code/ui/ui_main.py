import sys
import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject
import threading

from code import diagram_creator
from code.ui import start, login, load_or_create_config, select_config, edit_config_file, select_plants,warning_progress_will_be_lost, error_not_a_valid_config_file, error_no_config_files_found
from PyQt5.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal
from qt_thread_task import qt_thread_task


class userinterface():
    def __init__(self):
        # windows
        self.start_window = None
        self.login_window = None
        self.load_or_create_config_window = None
        self.select_config_window = None
        self.edit_config_file_window = None
        self.select_plants_window = None
        self.data_will_be_lost_warning = None
        self.not_a_valid_config_file_error = None
        self.no_config_files_found_error = None
        # parameters
        self.threadpool = None
        self.driver = None
        self.all_plants = None
        self.config = None
        config_file_name = None
        #self.running = False


    def set_driver(self, driver):
        self.driver = driver
        print(self.driver)

    def set_all_plants(self, all_plants):
        self.all_plants = all_plants

    def set_config(self, config):
        self.config = config
    # create and display start window
    # also calls the display_file_check
    def create_start_window(self):
        self.start_window = start.Logic()
        self.start_window.show()
        self.start_window.display_file_check()
    # create and display login window
    # size and position will be taken from the previous window

    # wrapper for the diagram_creator.init_driver
    # saves the return in the class variable driver
    def create_login_window(self, previous_window):
        geometry = previous_window.geometry()
        self.login_window = login.Logic()
        self.login_window.setGeometry(geometry)
        self.login_window.show()

    # loads the load_or_create_config window, takes the geometry form the login window
    # shows the load_or_create_config windows with the geometry from the login window and closes the login window
    def create_load_or_create_config_window(self):
        print("config chose window")
        geometry = self.login_window.geometry()
        self.load_or_create_config_window = load_or_create_config.Logic()
        self.load_or_create_config_window.setGeometry(geometry)
        self.load_or_create_config_window.show()
        self.login_window.close()

    def create_select_config_window(self, previous_window):
        #geometry = previous_window.geometry()
        self.select_config_window = select_config.Logic()
        #self.select_config_window.setGeometry(geometry)
        self.select_config_window.load_config_files()
        self.select_config_window.check_if_config_files_exist()
        self.select_config_window.show()

    def create_edit_config_file_window(self, previous_window):
        geometry = previous_window.geometry()
        self.edit_config_file_window = edit_config_file.Logic()
        self.edit_config_file_window.setGeometry(geometry)
        self.edit_config_file_window.load_templates()
        self.edit_config_file_window.show()

    def create_select_plants_window(self):
        self.select_plants_window = select_plants.Logic()
        self.select_plants_window.show()

    def create_not_a_valid_config_file_error(self, previous_window):
        self.not_a_valid_config_file_error = error_not_a_valid_config_file.Logic()
        self.not_a_valid_config_file_error.previous_window = previous_window
        previous_window.setEnabled(False)
        self.not_a_valid_config_file_error.show()

    def create_no_config_files_found_error(self, previous_window):
        self.no_config_files_found_error = error_no_config_files_found.Logic()
        self.no_config_files_found_error.show()
        previous_window.setEnabled(False)

    def create_progress_will_be_lost_warning(self, previous_window):
        self.progress_will_be_lost_warning = warning_progress_will_be_lost.Logic()
        self.progress_will_be_lost_warning.previous_window = previous_window
        previous_window.setEnabled(False)
        self.progress_will_be_lost_warning.show()

    def init_driver_wrapper(self):
        self.create_load_or_create_config_window()
        #self.login_window.wait_for_website()
        #init_driver = qt_thread_task(diagram_creator.init_driver, "https://ewus.eneffco.de/ChartPage.aspx")
        #init_driver.signals.result.connect(self.init_driver_results)
        #init_driver.signals.finished.connect(self.login_wrapper)
        #self.threadpool.start(init_driver)

    def init_driver_results(self, driver):
        if driver is None:
            #Todo show error Window
            return
        self.driver = driver

    def login_wrapper(self):
        self.threadpool.clear()
        self.login_window.wait_for_login()
        login = qt_thread_task(diagram_creator.login, self.driver)
        login.signals.finished.connect(self.get_all_plants_wrapper)
        self.threadpool.start(login)

    def get_plants_with_exiting_diagram_wrapper(self):
        self.threadpool.clear()
        plants_with_existing_diagram = qt_thread_task(diagram_creator.get_plants_with_exiting_diagram, self.driver, self.config.diagram_name)
        plants_with_existing_diagram.signals.result.connect(self.select_plants_window.filtered_result)
        plants_with_existing_diagram.signals.finished.connect(self.select_plants_window.filtered_finished)
        self.threadpool.start(plants_with_existing_diagram)

    def get_all_plants_wrapper(self):
        self.threadpool.clear()
        self.login_window.wait_for_website()
        get_all_plants = qt_thread_task(diagram_creator.get_all_plants, self.driver, False)
        get_all_plants.signals.result.connect(self.get_all_plants_results)
        get_all_plants.signals.finished.connect(self.create_load_or_create_config_window)
        self.threadpool.start(get_all_plants)

    def get_all_plants_results(self, all_plants):
        print("all_platns_results")
        if all_plants is None or all_plants == []:
            # Todo show error Window
            return
        self.all_plants = all_plants
        print(self.all_plants)


# creates an object of userinterface_class
# this will be available for all scripts that import ui_main
userinterface = userinterface()

def ui_main():
    app = QtWidgets.QApplication(sys.argv)
    userinterface.threadpool = QThreadPool()
    print("Multithreading with maximum %d threads" % userinterface.threadpool.maxThreadCount())
    userinterface.create_start_window()
    sys.exit(app.exec_())

