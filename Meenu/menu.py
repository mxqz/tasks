import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QDateEdit, QPushButton, QHBoxLayout, QComboBox, QSizePolicy, QSpacerItem
from PyQt6.QtCore import QDate
import pyqtgraph as pg
import random

class CryptoExchangeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bank Exchange Rate Chart")
        self.setGeometry(100, 100, 800, 600)

        # Задаємо чорний фон для основного вікна
        self.setStyleSheet("background-color: black; color: white;")

        # Головний віджет і макет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)  # Вертикальний макет

        # Верхня панель (вибір банку)
        self.top_panel = QHBoxLayout()
        self.bank_combo = QComboBox()
        self.bank_combo.addItems(["PrivatBank", "Monobank", "Abank"])
        self.bank_combo.setStyleSheet("font-size: 14px; border: 2px solid white; border-radius: 5px; padding: 5px;")
        self.bank_combo.currentIndexChanged.connect(self.update_chart)
        self.top_panel.addWidget(QLabel("Select Bank:"))
        self.top_panel.addWidget(self.bank_combo)

        self.main_layout.addLayout(self.top_panel)  # Додаємо у головний макет

        # Ліва панель (графік та вибір дат)
        self.left_panel = QVBoxLayout()

        # Права панель (графік)
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('black')
        self.plot_widget.setStyleSheet("border: 2px solid white;")
        self.plot_widget.showGrid(x=True, y=True)

        self.left_panel.addWidget(self.plot_widget)

        # Нижня панель для вибору дат
        self.date_panel = QHBoxLayout()

        # Вибір дати початку
        self.start_date_picker = QDateEdit()
        self.start_date_picker.setCalendarPopup(True)
        self.start_date_picker.setDate(QDate.currentDate().addDays(-10))
        self.date_panel.addWidget(QLabel("Start Date:"))
        self.date_panel.addWidget(self.start_date_picker)

        # Вибір дати закінчення
        self.end_date_picker = QDateEdit()
        self.end_date_picker.setCalendarPopup(True)
        self.end_date_picker.setDate(QDate.currentDate())
        self.date_panel.addWidget(QLabel("End Date:"))
        self.date_panel.addWidget(self.end_date_picker)

        self.left_panel.addLayout(self.date_panel)

        # Панель кнопок
        self.button_panel = QHBoxLayout()

        # Кнопка для оновлення графіка
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
        self.button_panel.addWidget(self.update_button)

        # Кнопка для скидання вибору
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
        self.button_panel.addWidget(self.reset_button)

        self.left_panel.addLayout(self.button_panel)  # Додаємо панель кнопок

        # Додаємо ліву панель у головний макет
        self.main_layout.addLayout(self.left_panel)

        # Малюємо графік при завантаженні
        self.plot_graph()

    def plot_graph(self):
        self.plot_widget.clear()

        start_day = self.start_date_picker.date().day()
        end_day = self.end_date_picker.date().day()
        days = list(range(start_day, end_day + 1))

        if not days:
            return

        # Вибір банку згідно з вибором у випадаючому списку
        selected_bank = self.bank_combo.currentText()

        if selected_bank == "PrivatBank":
            bank1 = [random.uniform(27.0, 30.0) for _ in days]
            bank2 = [random.uniform(26.5, 29.5) for _ in days]
            bank3 = [random.uniform(27.2, 30.2) for _ in days]
        elif selected_bank == "Monobank":
            bank1 = [random.uniform(26.5, 29.5) for _ in days]
            bank2 = [random.uniform(27.0, 30.0) for _ in days]
            bank3 = [random.uniform(27.5, 30.5) for _ in days]
        elif selected_bank == "Abank":
            bank1 = [random.uniform(28.0, 31.0) for _ in days]
            bank2 = [random.uniform(26.0, 29.0) for _ in days]
            bank3 = [random.uniform(27.0, 30.0) for _ in days]
        else:
            return

        # Біле для ліній на чорному фоні
        self.plot_widget.plot(days, bank1, pen=pg.mkPen(color='w', width=2), symbol='o', name='Bank 1')
        self.plot_widget.plot(days, bank2, pen=pg.mkPen(color='g', width=2), symbol='x', name='Bank 2')
        self.plot_widget.plot(days, bank3, pen=pg.mkPen(color='b', width=2), symbol='s', name='Bank 3')

        self.plot_widget.setTitle("Exchange Rate Over Time", color='w')
        self.plot_widget.setLabel("left", "Exchange Rate (UAH)", color='w')
        self.plot_widget.setLabel("bottom", "Days", color='w')
        self.plot_widget.addLegend()

    def update_chart(self):
        self.plot_graph()  # Оновлення графіка після натискання кнопки

    def reset_filters(self):
        self.start_date_picker.setDate(QDate.currentDate().addDays(-10))  # Скидання дати початку
        self.end_date_picker.setDate(QDate.currentDate())  # Скидання дати закінчення
        self.bank_combo.setCurrentIndex(0)  # Скидання вибору банку
        self.plot_graph()  # Перемалюємо графік з новими налаштуваннями

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoExchangeGUI()
    window.show()
    sys.exit(app.exec())
