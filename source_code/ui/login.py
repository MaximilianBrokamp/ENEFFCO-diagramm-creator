from PyQt5 import QtGui
from PyQt5 import uic

from source_code.ui import ui_main

from source_code.ui import ui_main
# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("./source_code/ui/login.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)

        # connects
        self.actionQuit.triggered.connect(self.close_program)
        # add the loading_gif as a movie to the label
        self.loading_movie = QtGui.QMovie("./source_code/ui/additional_ressources/loading.gif")
        self.loading_label.setMovie(self.loading_movie)

    def wait_for_website(self):
        self.loading_label.show()
        self.loading_movie.start()
        self.loading_text_edit.clear()
        self.loading_text_edit.insertPlainText("waiting for website to finish loading")

    def wait_for_login(self):
        self.loading_movie.stop()
        self.loading_label.hide()
        self.loading_text_edit.clear()
        self.loading_text_edit.insertPlainText("Please login to the website to continue")

    def close_program(self):
        ui_main.userinterface.close()







