import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QDateEdit, QPushButton, QComboBox
from PyQt6.QtCore import QDate
import api_requests_and_dump as api
import pyqtgraph as pg

class CryptoExchangeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.isAxisBottomUpdated = True
        self.setWindowTitle(api.locals["window"])
        self.setGeometry(100, 100, 800, 600)

        self.darkTheme = True  # By default, use dark theme

        self.setStyleSheet("background-color: #000000; color: #ffffff;")  # Dark theme by default

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QHBoxLayout(self.centralWidget)  # <-- головне компонування горизонтальне

        # Left panel for controls
        self.leftPanel = QVBoxLayout()

        self.comboBank = QComboBox()
        self.comboBank.addItems(api.sorted_unique(api.data["bank"]))
        # self.comboBank.setStyleSheet("font-size: 14px; border: 2px solid white; border-radius: 5px; padding: 5px;")
        self.comboBank.currentIndexChanged.connect(self.updateSelectionCurrency)
        self.leftPanel.addWidget(QLabel(api.locals["choose"]["bank"]))
        self.leftPanel.addWidget(self.comboBank)

        self.comboCurrency = QComboBox()
        self.comboCurrency.addItems(api.sorted_unique(api.data[api.data["bank"] == self.comboBank.currentText()]["currency"]))
        # self.comboCurrency.setStyleSheet("font-size: 14px; border: 2px solid white; border-radius: 5px; padding: 5px;")
        self.comboCurrency.currentIndexChanged.connect(self.updatePlot)
        self.leftPanel.addWidget(QLabel(api.locals["choose"]["currency"]))
        self.leftPanel.addWidget(self.comboCurrency)

        self.pickerDateStart = QDateEdit()
        self.setupPicker(self.pickerDateStart, QDate.currentDate().addDays(-10))
        self.pickerDateEnd = QDateEdit()
        self.setupPicker(self.pickerDateEnd, QDate.currentDate())

        self.leftPanel.addWidget(QLabel(api.locals["date"]["start"]))
        self.leftPanel.addWidget(self.pickerDateStart)
        self.leftPanel.addWidget(QLabel(api.locals["date"]["end"]))
        self.leftPanel.addWidget(self.pickerDateEnd)
        
        # self.update_button = QPushButton(api.locals["update"])
        # self.update_button.clicked.connect(self.updatePlot)
        # self.update_button.setFixedSize(120, 35)
        # self.leftPanel.addWidget(self.update_button)

        # self.reset_button = QPushButton(api.locals["reset"])
        # self.reset_button.clicked.connect(self.reset_filters)
        # self.reset_button.setFixedSize(120, 35)
        # self.leftPanel.addWidget(self.reset_button)

        self.leftPanel.addStretch()  # For top alignment
        self.mainLayout.addLayout(self.leftPanel)

        # Right panel for plot
        self.plotWidget = pg.PlotWidget()
        # self.plotWidget.setBackground("black")
        self.plotWidget.showGrid(x=True, y=True)
        self.updatePlot()
        self.mainLayout.addWidget(self.plotWidget)
        
        # Theme toggle button
        self.buttonTheme = QPushButton(api.locals["theme"]["light"])
        self.buttonTheme.clicked.connect(self.toggleTheme)
        self.leftPanel.addWidget(self.buttonTheme)

    def setupPicker(self, picker: QDateEdit, date: QDate):
        picker.setCalendarPopup(True)
        picker.setDate(date)
        picker.dateChanged.connect(self.updatePlot)

    def toggleTheme(self):
        theme = "dark" if self.darkTheme else "light"
        self.buttonTheme.setText(api.locals["theme"][theme])
        # self.setStyleSheet(open(f"config\\themes\\{theme}.qss").read())
        self.darkTheme = not self.darkTheme
        self.updatePlot()  # Re-draw the chart with the new theme

    def addPlot(self, widget: pg.PlotWidget, y: list, color: str, name: str):
        widget.plot(list(range(len(y))), y,
                    pen=pg.mkPen(color=color, width=2),
                    symbol='o', symbolBrush=color, symbolPen=None, name=name)

    def updatePlot(self):
        selectedBank = self.comboBank.currentText()
        selectedCurrency = self.comboCurrency.currentText()
        start = self.pickerDateStart.date().toPyDate()
        end = self.pickerDateEnd.date().toPyDate()

        if start > end:
            self.pickerDateEnd.setDate(self.pickerDateStart.date())
            return

        selection = api.data[
            (api.data["bank"] == selectedBank) &
            (api.data["currency"] == selectedCurrency) &
            (api.data["date"].dt.date.between(start, end))]
        
        # rates = [sum(i) / len(i) for i in zip(selection["rate_buy"], selection["rate_sell"])]
        rates_buy = selection["rate_buy"].tolist()
        rates_sell = selection["rate_sell"].tolist()

        dates = selection["date"].apply(lambda date: date.strftime("%d.%m")).tolist()

        # self.plotWidget.setLabel("left", api.locals["exchange"].format(selectedCurrency), color='r')
        # self.plotWidget.setLabel("bottom", api.locals["plot"]["bottom"], color='r')

        self.plotWidget.clear()
        self.plotWidget.setTitle(api.locals["plot"]["title"].format(selectedBank), color="#808080")
        self.plotWidget.addLegend()

        self.addPlot(self.plotWidget, rates_buy, color="#808080", name=api.locals["plot"]["legend"]["buy"])
        self.addPlot(self.plotWidget, rates_sell, color="#808080", name=api.locals["plot"]["legend"]["sell"])

        if not len(dates):
            self.isAxisBottomUpdated = False
        
        if len(dates) and not self.isAxisBottomUpdated:
            self.isAxisBottomUpdated = True
            self.plotWidget.getPlotItem().setAxisItems({"bottom": pg.AxisItem(orientation="bottom")})

        self.plotWidget.getPlotItem().getAxis("bottom").setTicks([list(enumerate(dates))])
        
        self.plotWidget.plotItem.vb.autoRange()
        

    def updateSelectionCurrency(self):
        self.comboCurrency.clear()
        self.comboCurrency.addItems(api.sorted_unique(api.data[api.data["bank"] == self.comboBank.currentText()]["currency"]))
        self.comboCurrency.setCurrentIndex(0)
        self.updatePlot()

    # def resetFilters(self):
    #     self.pickerDateStart.setDate(QDate.currentDate().addDays(-10))
    #     self.pickerDateEnd.setDate(QDate.currentDate())
    #     self.comboBank.setCurrentIndex(0)
    #     self.comboCurrency.setCurrentIndex(0)
    #     self.updateChart()
