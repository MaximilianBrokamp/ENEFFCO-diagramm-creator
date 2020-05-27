from PyQt5.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal

# defines signals for the qt_thread_task to use
class thread_signals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)

#defines a aubclass to QRunnable wich tasks that can be executed through the QT thread pool
class qt_thread_task(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(qt_thread_task, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = thread_signals()

    # if an instance of qt_thread_task is executed the run function will be called
    # the run function calls the function that was set during the creation of the instance in the init method
    def run(self):
        result = self.fn(*self.args, **self.kwargs)
        self.signals.result.emit(result)
        self.signals.finished.emit()
