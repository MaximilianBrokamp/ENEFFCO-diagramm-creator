import sys
from PyQt5 import QtWidgets
import start
import login


class userinterface_class():
    def __init__(self):
        self.running = False
        self.start_window = None
        self.login_window = None

    # create and display start window
    # also calls the display_file_check
    def create_start_window(self):
        self.start_window = start.Logic()
        self.start_window.show()
        self.start_window.display_file_check()
    # create and display login window
    # size and position will be taken from the previous window
    def create_login_window(self, previous_window):
        geometry = previous_window.geometry()
        self.login_window = login.Logic()
        self.login_window.setGeometry(geometry)
        self.login_window.show()
        self.login_window.diplay_loading_movie()


# creates an object of userinterface_class
# this will be available for all scripts that impot ui_main
userinterface = userinterface_class()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #userinterface = userinterface_class()
    userinterface.create_start_window()
    sys.exit(app.exec_())
