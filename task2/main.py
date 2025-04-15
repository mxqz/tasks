import sys
from menu import *
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoExchangeGUI()
    window.show()
    app.exec()
