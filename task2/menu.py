from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QDateEdit, QPushButton, QComboBox
from PyQt6.QtCore import QDate
import pyqtgraph as pg
from numpy import polyfit, polyval
import api_requests_and_dump as api
import layout


class CryptoExchangeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.isAxisBottomUpdated = False
        self.showTrend = True
        self.setWindowTitle(layout.locals["window"])
        self.setGeometry(100, 100, 800, 600)

        self.darkTheme = False

        self.createWidgets()
        self.addWidgets()

        self.pickerDateStart.setDate(QDate.currentDate().addDays(-7))
        self.pickerDateEnd.setDate(QDate.currentDate())
        self.pickerDateStart.setCalendarPopup(True)
        self.pickerDateEnd.setCalendarPopup(True)

        self.plotWidget.showGrid(x=True, y=True)

        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QHBoxLayout(self.centralWidget)
        self.mainLayout.addLayout(self.leftPanel)
        self.mainLayout.addWidget(self.plotWidget)

        self.updateLocals()
        self.connectWidgets()
        self.toggleTheme()
        self.toggleTrend()
        self.updatePlot()
    

    def createWidgets(self):
        self.centralWidget = QWidget()
        self.labelBank = QLabel()
        self.comboBank = QComboBox()
        self.labelCurrency = QLabel()
        self.comboCurrency = QComboBox()
        self.labelDateStart = QLabel()
        self.pickerDateStart = QDateEdit()
        self.labelDateEnd = QLabel()
        self.pickerDateEnd = QDateEdit()
        self.requestButton = QPushButton()
        self.clearButton = QPushButton()
        self.buttonTrend = QPushButton()
        self.buttonTheme = QPushButton()
        self.comboLang = QComboBox()
        self.plotWidget = pg.PlotWidget()
        self.leftPanel = QVBoxLayout()


    def addWidgets(self):
        self.leftPanel.addWidget(self.labelBank)
        self.leftPanel.addWidget(self.comboBank)
        self.leftPanel.addWidget(self.labelCurrency)
        self.leftPanel.addWidget(self.comboCurrency)
        self.leftPanel.addWidget(self.labelDateStart)
        self.leftPanel.addWidget(self.pickerDateStart)
        self.leftPanel.addWidget(self.labelDateEnd)
        self.leftPanel.addWidget(self.pickerDateEnd)
        self.leftPanel.addWidget(QLabel(""))
        self.leftPanel.addWidget(self.requestButton)
        self.leftPanel.addWidget(self.clearButton)
        self.leftPanel.addStretch()
        self.leftPanel.addWidget(self.buttonTrend)
        self.leftPanel.addWidget(self.buttonTheme)
        self.leftPanel.addWidget(self.comboLang)


    def connectWidgets(self):
        self.comboBank.currentIndexChanged.connect(self.updateSelectionCurrency)
        self.comboCurrency.currentIndexChanged.connect(self.updatePlot)
        self.pickerDateStart.dateChanged.connect(self.updatePlot)
        self.pickerDateEnd.dateChanged.connect(self.updatePlot)
        self.requestButton.clicked.connect(self.requestData)
        self.clearButton.clicked.connect(self.clearData)
        self.buttonTrend.clicked.connect(self.toggleTrend)
        self.buttonTheme.clicked.connect(self.toggleTheme)
        self.comboLang.currentIndexChanged.connect(self.updateLocals)


    def getThemeString(self):
        return "dark" if self.darkTheme else "light"


    def getTrendString(self):
        return "shown" if self.showTrend else "hidden"


    def toggleTheme(self):
        self.darkTheme = not self.darkTheme
        theme = self.getThemeString()
        styleSheet = open(layout.stylesheet.format(theme)).read()
        self.setStyleSheet(styleSheet)
        self.plotWidget.setBackground(layout.config["plot"][theme]["background-color"])
        self.buttonTheme.setText(layout.locals["theme"][theme])


    def toggleTrend(self):
        self.showTrend = not self.showTrend
        mode = self.getTrendString()
        self.buttonTrend.setText(layout.locals["trend"][mode])
        self.updatePlot()


    def addPlot(self, plot: pg.PlotItem, x: list, y: list, color: str, symbol: str | None, name: str):
        plot.plot(x, y, 
                  pen=pg.mkPen(color=color, width=2),
                  symbol=symbol,
                  symbolBrush=color, 
                  symbolPen=layout.config["plot"]["symbol"]["pen"],
                  name=name)


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
            (api.data["date"].dt.date.between(start, end))
        ]

        rates_buy = selection["rate_buy"].tolist()
        rates_sell = selection["rate_sell"].tolist()

        dates = selection["date"].apply(lambda date: date.strftime("%d.%m")).tolist()
        axis_x = range(len(dates))

        self.plotWidget.clear()
        self.plotWidget.setTitle(layout.locals["plot"]["title"].format(selectedBank))
        self.plotWidget.addLegend()

        plot = self.plotWidget.getPlotItem()
        
        self.addPlot(plot, axis_x, rates_buy, 
                     color=layout.config["plot"]["color"]["buy"], 
                     symbol=layout.config["plot"]["symbol"][""],
                     name=layout.locals["plot"]["legend"]["buy"]
                     )
        self.addPlot(plot, axis_x, rates_sell, 
                     color=layout.config["plot"]["color"]["sell"],
                     symbol=layout.config["plot"]["symbol"][""],
                     name=layout.locals["plot"]["legend"]["sell"]
                     )
        
        if self.showTrend and len(axis_x) > 1:
            rates = list(zip(rates_buy, rates_sell))
            rates = [sum(item) / len(item) for item in rates]
            trend = polyval(polyfit(axis_x, rates, deg=1), axis_x)

            self.addPlot(plot, axis_x, trend,
                     color=layout.config["plot"]["color"]["trend"],
                     symbol=layout.config["plot"]["symbol"]["trend"],
                     name=layout.locals["plot"]["legend"]["trend"]
                     )

        if not len(dates):
            self.isAxisBottomUpdated = False
        
        if len(dates) and not self.isAxisBottomUpdated:
            self.isAxisBottomUpdated = True
            self.plotWidget.getPlotItem().setAxisItems({"bottom": pg.AxisItem(orientation="bottom")})

        ticks = [list(zip(axis_x, dates))]
        self.plotWidget.getPlotItem().getAxis("bottom").setTicks(ticks)

        self.plotWidget.plotItem.vb.autoRange()


    def updateSelectionCurrency(self):
        self.comboCurrency.clear()
        self.comboCurrency.addItems(api.sorted_unique(api.data[api.data["bank"] == self.comboBank.currentText()]["currency"]))
        self.updatePlot()


    def updateChart(self):
        self.comboBank.clear()
        self.comboBank.addItems(api.sorted_unique(api.data["bank"]))
        self.updateSelectionCurrency()


    def updateLocals(self):
        self.setWindowTitle(layout.locals["window"])
        theme = self.getThemeString()
        mode = self.getTrendString()
        selected_index = self.comboLang.currentIndex()
        if selected_index != -1:
            layout.set_localization(self.comboLang.currentData())
        self.comboLang.blockSignals(True)
        self.comboLang.clear()
        for lang in layout.config["available_lang"]:
            self.comboLang.addItem(layout.locals["lang"][lang], lang)
        self.comboLang.setCurrentIndex(self.comboLang.findData(layout.config["selected_lang"]))
        self.comboLang.blockSignals(False)
        self.labelBank.setText(layout.locals["choose"]["bank"])
        self.labelCurrency.setText(layout.locals["choose"]["currency"])
        self.labelDateStart.setText(layout.locals["date"]["start"])
        self.labelDateEnd.setText(layout.locals["date"]["end"])
        self.requestButton.setText(layout.locals["request"])
        self.clearButton.setText(layout.locals["clear"])
        self.buttonTheme.setText(layout.locals["theme"][theme])
        self.buttonTrend.setText(layout.locals["trend"][mode])
        api.data = api.request_csv_reading(layout.raw_data)
        self.updateChart()
        


    def requestData(self):
        start = self.pickerDateStart.date().toPyDate()
        end = self.pickerDateEnd.date().toPyDate()
        api.request_external_csv_update(start, end, layout.raw_data, layout.raw_exchange_rates)
        api.data = api.request_csv_reading(layout.raw_data)
        self.updateChart()
    

    def clearData(self):
        api.request_csv_clear(layout.raw_data)
        api.data = api.request_csv_reading(layout.raw_data)
        self.updateChart()
