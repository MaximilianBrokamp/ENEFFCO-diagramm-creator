import sys
import time
import datetime
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject
import threading

from source_code.qt_thread_task import qt_thread_task
from source_code import diagram_creator
from source_code.ui import start, login, load_or_create_config, select_config, edit_config_file, select_plants, loading,running, finished, warning_progress_will_be_lost, error_not_a_valid_config_file, error_no_config_files_found
from PyQt5.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal


class userinterface():
    def __init__(self):
        # windows
        self.start_window = None
        self.login_window = None
        self.load_or_create_config_window = None
        self.select_config_window = None
        self.edit_config_file_window = None
        self.select_plants_window = None
        self.loading_window = None
        self.running_window = None
        self.finished_window = None
        self.data_will_be_lost_warning = None
        self.not_a_valid_config_file_error = None
        self.no_config_files_found_error = None
        # parameters
        self.threadpool = None
        self.driver = None
        self.all_plants = None
        self.config = None
        config_file_name = None
        self.pause = False
        self.end = False
        self.to_creat_list = None
        self.current_plant_number = None
        self.real_report_path = None
        #self.running = False


    def set_driver(self, driver):
        self.driver = driver

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

    def create_loading_window(self):
        self.loading_window = loading.Logic()
        self.loading_window.show()
        self.loading_window.show_loading()

    def create_running_window(self, previous_window):
        geometry = previous_window.geometry()
        self.running_window = running.Logic()
        self.running_window.setGeometry(geometry)
        self.running_window.show()
        self.init_diagram_creation_loop()

    def create_finished_window(self, previous_window):
        geometry = previous_window.geometry()
        self.finished_window = finished.Logic()
        self.finished_window.setGeometry(geometry)
        self.finished_window.show()

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
        self.login_window.wait_for_website()
        init_driver = qt_thread_task(diagram_creator.init_driver, "https://ewus.eneffco.de/ChartPage.aspx")
        init_driver.signals.result.connect(self.init_driver_results)
        init_driver.signals.finished.connect(self.login_wrapper)
        self.threadpool.start(init_driver)

    def init_driver_results(self, driver):
        if driver is None:
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
        get_all_plants.signals.finished.connect(self.get_all_plants_finished)
        self.threadpool.start(get_all_plants)

    def get_all_plants_results(self, all_plants_lists):
        self.create_select_plants_window()
        self.select_plants_window.all_plants_as_list = all_plants_lists[1]
        self.select_plants_window.all_plants_as_tree = all_plants_lists[0]
        self.select_plants_window.load_plant_tree(all_plants_lists[0])

    def get_all_plants_finished(self):
        self.threadpool.clear()
        self.create_load_or_create_config_window()




    def init_diagram_creation_loop(self):
        self.current_plant_number = 0
        to_create_list = []
        if self.config.ignore_list== []:
            to_create_list = self.config.select_list
        else:
            for element in self.config.select_list:
                for ignore in self.config.ignore_list:
                    if element.find(ignore) == -1:
                        to_create_list.append(element)
        self.to_creat_list = to_create_list
        diagram_loop = qt_thread_task(self.diagram_creation_loop)
        diagram_loop.signals.result.connect(self.create_report_wrapper)
        diagram_loop.signals.finished.connect(self.diagram_creation_loop_finihsed)
        self.threadpool.start(diagram_loop)

    def diagram_creation_loop(self):
        report_data = []
        successfull_created_diagrams = 0
        failed_diagrams = 0
        warnings = 0
        number_created_diagrams = 0
        number_diagrams_to_create = len(self.to_creat_list)
        start = datetime.datetime.now()
        for element in self.to_creat_list:
            self.running_window.plant_info.clear()
            self.running_window.plant_info.insert(element)
            self.running_window.number_info.clear()
            self.running_window.number_info.insert("Number " + str(number_created_diagrams + 1) + " of " + str(len(self.to_creat_list)))
            while self.pause:
                time.sleep(0.5)
            if self.end:
                break
            return_value = diagram_creator.create_diagram(self.driver,  self.config.diagram_type, self.config.diagram_name, element, self.config.template_path, self.config)
            #report_data.append(return_value[0])
            if return_value[1]:
                successfull_created_diagrams += 1
            else:
                failed_diagrams += 1
            if return_value[2]:
                warnings += 1
            number_created_diagrams += 1

        task_complete = False
        if number_created_diagrams == len(self.to_creat_list):
            task_complete = True
        end = datetime.datetime.now()

        duration = round((end - start).total_seconds()/60, 2)
        return [self.config,  task_complete, duration, number_created_diagrams,
                      number_diagrams_to_create, successfull_created_diagrams, failed_diagrams, warnings]

    def diagram_creation_loop_finihsed(self):
        self.threadpool.clear()
        self.create_finished_window(self.running_window)
        self.finished_window.display_report()
        self.running_window.close()

    def create_report_wrapper(self, report_data):
        real_report_path = diagram_creator.create_report(report_data[0], report_data[1], report_data[2], report_data[3], report_data[4], report_data[5], report_data[6], report_data[7])
        self.real_report_path = real_report_path

    def close(self):
        if self.start_window is not None:
            self.start_window.close()

        if self.login_window is not None:
            self.login_window.close()

        if self.load_or_create_config_window is not None:
            self.load_or_create_config_window.close()

        if self.select_config_window is not None:
            self.select_config_window.close()

        if self.edit_config_file_window is not None:
            self.edit_config_file_window.close()

        if self.select_plants_window is not None:
            self.select_plants_window.close()

        if self.loading_window is not None:
            self.loading_window.close()

        if self.running_window is not None:
            self.running_window.close()

        if self.finished_window is not None:
            self.finished_window.close()

        if self.data_will_be_lost_warning is not None:
            self.data_will_be_lost_warning.close()

        if self.not_a_valid_config_file_error is not None:
            self.not_a_valid_config_file_error.close()

        if self.no_config_files_found_error is not None:
            self.no_config_files_found_error.close()

        if self.driver is not None:
            self.driver.quit()

        exit(0)
# creates an object of userinterface_class
# this will be available for all scripts that import ui_main
userinterface = userinterface()

def ui_main():
    app = QtWidgets.QApplication(sys.argv)
    userinterface.threadpool = QThreadPool()
    userinterface.threadpool.clear()
    userinterface.create_start_window()
    sys.exit(app.exec_())

