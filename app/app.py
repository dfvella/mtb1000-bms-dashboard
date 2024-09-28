from app import ctypes, sys, QtWidgets, WINDOWS_APPID

from .main import MainWindow

def run():
    if sys.platform == 'win32':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(WINDOWS_APPID)
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
