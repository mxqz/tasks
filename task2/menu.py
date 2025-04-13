import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QDateEdit, QPushButton, QComboBox
from PyQt6.QtCore import QDate
import pyqtgraph as pg
import json

class CryptoExchangeGUI(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.data = df
        self.locals = json.load(open("config\\en.json", "r"))
        
        self.setWindowTitle(locals["window"])
        self.setGeometry(100, 100, 800, 600)

        self.darkTheme = True  # By default, use dark theme

        self.setStyleSheet("background-color: black; color: white;")  # Dark theme by default

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QHBoxLayout(self.centralWidget)  # <-- головне компонування горизонтальне

        # Left panel for controls
        self.leftPanel = QVBoxLayout()

        self.comboBank = QComboBox()
        self.comboBank.addItems(sorted(self.data["bank"].unique()))
        self.comboBank.setObjectName("comboBank")
        self.comboBank.setStyleSheet("font-size: 14px; border: 2px solid white; border-radius: 5px; padding: 5px;")
        self.comboBank.currentIndexChanged.connect(self.updateSelectionCurrency)
        self.leftPanel.addWidget(QLabel(self.locals["choose"]["bank"]))
        self.leftPanel.addWidget(self.comboBank)

        self.comboCurrency = QComboBox()
        self.comboCurrency.addItems(sorted(self.data[self.data["bank"] == self.comboBank.currentText()]["currency"].unique()))
        self.comboCurrency.setStyleSheet("font-size: 14px; border: 2px solid white; border-radius: 5px; padding: 5px;")
        self.comboCurrency.currentIndexChanged.connect(self.updatePlot)
        self.leftPanel.addWidget(QLabel(self.locals["choose"]["currency"]))
        self.leftPanel.addWidget(self.comboCurrency)

        self.pickerDateStart = QDateEdit()
        self.setupPicker(self.pickerDateStart, QDate.currentDate().addDays(-10))
        self.pickerDateEnd = QDateEdit()
        self.setupPicker(self.pickerDateEnd, QDate.currentDate())

        self.leftPanel.addWidget(QLabel(self.locals["date"]["start"]))
        self.leftPanel.addWidget(self.pickerDateStart)
        self.leftPanel.addWidget(QLabel(self.locals["date"]["end"]))
        self.leftPanel.addWidget(self.pickerDateEnd)

        # self.update_button = QPushButton(self.locals["update"])
        # self.update_button.clicked.connect(self.update_chart)
        # self.update_button.setStyleSheet("""
        #     QPushButton {
        #         border: 2px solid white; 
        #         border-radius: 5px; 
        #         padding: 5px;
        #         background-color: #333; 
        #         color: white;
        #     }
        #     QPushButton:hover {
        #         background-color: #555;
        #     }
        # """)
        # self.update_button.setFixedSize(120, 35)
        # self.leftPanel.addWidget(self.update_button)

        # self.reset_button = QPushButton(self.locals["reset"])
        # self.reset_button.clicked.connect(self.reset_filters)
        # self.reset_button.setObjectName("reset_button")
        # self.reset_button.setStyleSheet("""
        #     #reset_button {
        #         border: 2px solid white; 
        #         border-radius: 5px; 
        #         padding: 5px;
        #         background-color: #900; 
        #         color: white;
        #     }
        #     #reset_button:hover {
        #         background-color: #c00;
        #     }
        # """)
        # self.reset_button.setFixedSize(120, 35)
        # self.leftPanel.addWidget(self.reset_button)

        self.leftPanel.addStretch()  # Для вирівнювання елементів вгору
        self.mainLayout.addLayout(self.leftPanel)

        # Right panel for plot
        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setBackground("black")
        self.plotWidget.setStyleSheet("border: 2px solid white;")
        self.plotWidget.showGrid(x=True, y=True)
        self.mainLayout.addWidget(self.plotWidget)

        # Theme toggle button
        self.buttonTheme = QPushButton(self.locals["theme"]["light"])
        self.buttonTheme.clicked.connect(self.toggleTheme)
        self.buttonTheme.setStyleSheet("""
            QPushButton {
                border: 2px solid white;
                border-radius: 5px;
                padding: 5px;
                background-color: #333;
                color: white;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.leftPanel.addWidget(self.buttonTheme)

        self.updatePlot()

    def setupPicker(self, picker: QDateEdit, date: QDate):
        picker.setCalendarPopup(True)
        picker.setDate(date)
        picker.dateChanged.connect(self.updatePlot)

    def toggleTheme(self):
        if self.darkTheme:
            self.setStyleSheet("""
                background-color: #f0f0f0; 
                color: black;
            """)
            self.plotWidget.setBackground('#ffffff')
            # self.update_button.setStyleSheet("""
            #     QPushButton {
            #         border: 2px solid black;
            #         border-radius: 5px;
            #         padding: 5px;
            #         background-color: #ccc;
            #         color: black;
            #     }
            #     QPushButton:hover {
            #         background-color: #bbb;
            #     }
            # """)
            # self.reset_button.setStyleSheet("""
            #     QPushButton {
            #         border: 2px solid black;
            #         border-radius: 5px;
            #         padding: 5px;
            #         background-color: #e94e77;
            #         color: black;
            #     }
            #     QPushButton:hover {
            #         background-color: #d42f60;
            #     }
            # """)
            self.buttonTheme.setStyleSheet("""
                QPushButton {
                    border: 2px solid black;
                    border-radius: 5px;
                    padding: 5px;
                    background-color: #ccc;
                    color: black;
                }
                QPushButton:hover {
                    background-color: #bbb;
                }
            """)
        else:
            self.setStyleSheet("""
                background-color: black;
                color: white;
            """)
            self.plotWidget.setBackground('black')
            # self.update_button.setStyleSheet("""
            #     QPushButton {
            #         border: 2px solid white;
            #         border-radius: 5px;
            #         padding: 5px;
            #         background-color: #333;
            #         color: white;
            #     }
            #     QPushButton:hover {
            #         background-color: #555;
            #     }
            # """)
            # self.reset_button.setStyleSheet("""
            #     QPushButton {
            #         border: 2px solid white;
            #         border-radius: 5px;
            #         padding: 5px;
            #         background-color: #900;
            #         color: white;
            #     }
            #     QPushButton:hover {
            #         background-color: #c00;
            #     }
            # """)
            self.buttonTheme.setStyleSheet("""
                QPushButton {
                    border: 2px solid white;
                    border-radius: 5px;
                    padding: 5px;
                    background-color: #333;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #555;
                }
            """)

        theme = "dark" if self.darkTheme else "light"
        self.buttonTheme.setText(self.locals["theme"][theme])
        self.darkTheme = not self.darkTheme
        self.updatePlot()  # Re-draw the chart with the new theme

    def addPlot(self, widget: pg.PlotWidget, x: list, y: list, color: str, name: str):
        widget.plot(list(range(len(x))), y,
                    pen=pg.mkPen(color=color, width=2),
                    symbol='o', symbolBrush=color, symbolPen=None, name=name)

    def updatePlot(self):
        selectedBank = self.comboBank.currentText()
        selectedCurrency = self.comboCurrency.currentText()
        start = self.pickerDateStart.date().toPyDate()
        end = self.pickerDateEnd.date().toPyDate()

        if start > end:
            return

        selection = self.data[
            (self.data["bank"] == selectedBank) &
            (self.data["currency"] == selectedCurrency) &
            (self.data["date"].dt.date.between(start, end))]
        
        # rates = [sum(i) / len(i) for i in zip(selection["rate_buy"], selection["rate_sell"])]
        rates_buy = list(selection["rate_buy"])
        rates_sell = list(selection["rate_sell"])

        labels = selection["date"].apply(lambda date: date.strftime("%d.%m"))

        self.plotWidget.clear()
        self.addPlot(self.plotWidget, labels, rates_buy, 'g', name=f"{selectedBank} Buy Rate")
        self.addPlot(self.plotWidget, labels, rates_sell, 'g', name=f"{selectedBank} Sell Rate")
        
        # self.plotWidget.setLabel("left", self.locals["exchange"].format(selectedCurrency), color='r')
        # self.plotWidget.setLabel("bottom", self.locals["plot"]["bottom"], color='r')
        self.plotWidget.setTitle(self.locals["plot"]["title"].format(selectedBank), color='r')
        self.plotWidget.getPlotItem().getAxis("bottom").setTicks([list(enumerate(labels))])
        self.plotWidget.addLegend()
        self.plotWidget.plotItem.vb.autoRange()

    def updateSelectionCurrency(self):
        currencies = sorted(self.data[self.data["bank"] == self.comboBank.currentText()]["currency"].unique())
        self.comboCurrency.clear()
        self.comboCurrency.addItems(currencies)
        self.comboCurrency.setCurrentIndex(0)
        self.updatePlot()

    # def resetFilters(self):
    #     self.pickerDateStart.setDate(QDate.currentDate().addDays(-10))
    #     self.pickerDateEnd.setDate(QDate.currentDate())
    #     self.comboBank.setCurrentIndex(0)
    #     self.comboCurrency.setCurrentIndex(0)
    #     self.updateChart()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoExchangeGUI()
    window.show()
    sys.exit(app.exec())
