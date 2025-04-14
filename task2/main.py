from menu import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoExchangeGUI()
    window.show()
    app.exec()
