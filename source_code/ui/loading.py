from PyQt5 import uic, QtGui
from PyQt5.QtGui import QColor

from source_code.ui import ui_main
from source_code import check_all_files
from PyQt5 import  QtCore
# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("./source_code/ui/loading.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)


        self.loading_movie = QtGui.QMovie("./source_code/ui/additional_ressources/loading.gif")
        self.loading_label.setMovie(self.loading_movie)

    def show_loading(self):
        #self.loading_label.show()
        self.loading_movie.start()


