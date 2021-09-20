from PyQt5.QtWidgets import *

from main_window import MainWindow

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
