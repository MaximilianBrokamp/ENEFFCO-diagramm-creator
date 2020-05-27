from PyQt5 import uic
import icons_rc
# load ui file

baseUIClass, baseUIWidget = uic.loadUiType("./code/ui/warning_progress_will_be_lost.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        self.previous_window = None
        # connects
        self.ok_button.clicked.connect(self.ok_button_click)
        self.ok_button.clicked.connect(self.ok_button_click)

    def cancel_button_click(self):
        self.previous_window.setEnabled(True)

    def ok_button_click(self):
        self.previous_window.setEnabled(True)


