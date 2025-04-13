import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QDateEdit, QPushButton, QComboBox
from PyQt6.QtCore import QDate
import pyqtgraph as pg
import random


class CryptoExchangeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bank Exchange Rate Chart")
        self.setGeometry(100, 100, 800, 600)

        self.dark_theme = True  # By default, use dark theme

        self.setStyleSheet("background-color: black; color: white;")  # Dark theme by default

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)  # <-- головне компонування горизонтальне

        # Left panel for controls
        self.left_panel = QVBoxLayout()

        self.bank_combo = QComboBox()
        self.bank_combo.addItems(["PrivatBank", "Monobank", "Abank", "Average banks"])
        self.bank_combo.setStyleSheet("font-size: 14px; border: 2px solid white; border-radius: 5px; padding: 5px;")
        self.bank_combo.currentIndexChanged.connect(self.update_chart)
        self.left_panel.addWidget(QLabel("Choose bank:"))
        self.left_panel.addWidget(self.bank_combo)

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["USD", "EUR", "PLN"])
        self.currency_combo.setStyleSheet("font-size: 14px; border: 2px solid white; border-radius: 5px; padding: 5px;")
        self.currency_combo.currentIndexChanged.connect(self.update_chart)
        self.left_panel.addWidget(QLabel("Choose currency:"))
        self.left_panel.addWidget(self.currency_combo)

        self.start_date_picker = QDateEdit()
        self.start_date_picker.setCalendarPopup(True)
        self.start_date_picker.setDate(QDate.currentDate().addDays(-10))

        self.end_date_picker = QDateEdit()
        self.end_date_picker.setCalendarPopup(True)
        self.end_date_picker.setDate(QDate.currentDate())

        self.left_panel.addWidget(QLabel("Start Date:"))
        self.left_panel.addWidget(self.start_date_picker)
        self.left_panel.addWidget(QLabel("End Date:"))
        self.left_panel.addWidget(self.end_date_picker)

        self.update_button = QPushButton("Update Chart")
        self.update_button.clicked.connect(self.update_chart)
        self.update_button.setStyleSheet("""
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
        self.update_button.setFixedSize(120, 35)
        self.left_panel.addWidget(self.update_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_filters)
        self.reset_button.setStyleSheet("""
            QPushButton {
                border: 2px solid white; 
                border-radius: 5px; 
                padding: 5px;
                background-color: #900; 
                color: white;
            }
            QPushButton:hover {
                background-color: #c00;
            }
        """)
        self.reset_button.setFixedSize(120, 35)
        self.left_panel.addWidget(self.reset_button)

        self.left_panel.addStretch()  # Для вирівнювання елементів вгору
        self.main_layout.addLayout(self.left_panel)

        # Right panel for plot
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('black')
        self.plot_widget.setStyleSheet("border: 2px solid white;")
        self.plot_widget.showGrid(x=True, y=True)
        self.main_layout.addWidget(self.plot_widget)

        # Theme toggle button
        self.theme_button = QPushButton("Switch to Light Theme")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setStyleSheet("""
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
        self.left_panel.addWidget(self.theme_button)

        # Variable to hold the text item (used to show value on hover)
        self.text_item = None

        self.plot_graph()

    def toggle_theme(self):
        if self.dark_theme:
            self.setStyleSheet("""
                background-color: #f0f0f0; 
                color: black;
            """)
            self.plot_widget.setBackground('#ffffff')
            self.theme_button.setText("Switch to Dark Theme")
            self.update_button.setStyleSheet("""
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
            self.reset_button.setStyleSheet("""
                QPushButton {
                    border: 2px solid black;
                    border-radius: 5px;
                    padding: 5px;
                    background-color: #e94e77;
                    color: black;
                }
                QPushButton:hover {
                    background-color: #d42f60;
                }
            """)
            self.theme_button.setStyleSheet("""
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
            self.plot_widget.setBackground('black')
            self.theme_button.setText("Switch to Light Theme")
            self.update_button.setStyleSheet("""
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
            self.reset_button.setStyleSheet("""
                QPushButton {
                    border: 2px solid white;
                    border-radius: 5px;
                    padding: 5px;
                    background-color: #900;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #c00;
                }
            """)
            self.theme_button.setStyleSheet("""
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

        self.dark_theme = not self.dark_theme
        self.plot_graph()  # Re-draw the chart with the new theme

    def plot_graph(self):
        self.plot_widget.clear()

        start = self.start_date_picker.date()
        end = self.end_date_picker.date()

        if start > end:
            return

        days_count = (end.toPyDate() - start.toPyDate()).days + 1
        days = list(range(days_count))
        labels = [start.addDays(i).toString("dd.MM") for i in days]

        selected_bank = self.bank_combo.currentText()

        if selected_bank == "PrivatBank":
            rates = [random.uniform(27.0, 30.0) for _ in days]
            color = 'g'
        elif selected_bank == "Monobank":
            rates = [random.uniform(26.5, 29.5) for _ in days]
            color = 'g'
        elif selected_bank == "Abank":
            rates = [random.uniform(28.0, 31.0) for _ in days]
            color = 'g'
        elif selected_bank == "Average banks":
            privat = [random.uniform(27.0, 30.0) for _ in days]
            mono = [random.uniform(26.5, 29.5) for _ in days]
            abank = [random.uniform(28.0, 31.0) for _ in days]
            rates = [(privat[i] + mono[i] + abank[i]) / 3 for i in range(len(days))]
            color = 'g'
        else:
            return

        self.plot_widget.plot(list(range(len(labels))), rates,
                              pen=pg.mkPen(color=color, width=2),
                              symbol='o', name=selected_bank)
        
        selected_currency = self.currency_combo.currentText()
        if selected_currency == "USD":
            self.plot_widget.setLabel("left", "Exchange Rate (USD)", color='r')
        elif selected_currency == "EUR":
            self.plot_widget.setLabel("left", "Exchange Rate (EUR)", color='r')
        elif selected_currency == "PLN":
            self.plot_widget.setLabel("left", "Exchange Rate (PLN)", color='r')
        else:
            self.plot_widget.setLabel("left", "Exchange Rate (Not found)", color='r')
            return
        self.plot_widget.setTitle("Exchange Rate Over Time", color='r')
        self.plot_widget.setLabel("bottom", "Days", color='r')
        self.plot_widget.getPlotItem().getAxis('bottom').setTicks([list(enumerate(labels))])
        self.plot_widget.addLegend()

    def update_chart(self):
        self.plot_graph()

    def reset_filters(self):
        self.start_date_picker.setDate(QDate.currentDate().addDays(-10))
        self.end_date_picker.setDate(QDate.currentDate())
        self.bank_combo.setCurrentIndex(0)
        self.plot_graph()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoExchangeGUI()
    window.show()
    sys.exit(app.exec())
