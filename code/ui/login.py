from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
import ui_main


# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("login.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)

        # connects
        self.actionQuit.triggered.connect(self.close_program)
        # add the loading_gif as a movie to the label
        self.loading_movie = QtGui.QMovie("./loading.gif")
        self.loading_label.setMovie(self.loading_movie)

    def diplay_loading_movie(self):
        self.loading_movie.start()

    def hide_loading_movie(self):
        self.loading_movie.hide()

    def diplay_wait_login(self):
        pass

    def hide_wait_login(self):
        pass

    def dsiplay_wait_for_website(self):
        pass

    def hide_wait_for_website(self):
        pass

    def close_program(self):
        self.close()
        exit(0)







