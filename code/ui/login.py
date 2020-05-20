from PyQt5 import  QtWidgets
from PyQt5 import uic
import ui_main


# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("login.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)




