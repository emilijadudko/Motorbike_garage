# main.py
import sys
from garage_view import GarageViewWidget
from homepage import HomePageWidget
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motorcycle Garage App")
        self.resize(950, 650)

        # Light Mode Global Theme
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #ffffff;
                color: #111111;
            }
            QGroupBox {
                border: 1px solid #cccccc;
                border-radius: 6px;
                margin-top: 12px;
                font-weight: bold;
                color: #111111;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }
            QFrame {
                background-color: #f9f9f9;
                border: 1px solid #dddddd;
                border-radius: 4px;
            }
            QListWidget, QComboBox {
                background-color: #ffffff;
                color: #111111;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 4px;
            }
            QListWidget::item:selected {
                background-color: #007acc;
                color: #ffffff;
            }
            QPushButton {
                background-color: #f0f0f0;
                color: #111111;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #e4e4e4;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                color: #888888;
                border: 1px solid #e0e0e0;
            }
        """)

        # Container manager for multiple screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Instantiate view pages
        self.home_page = HomePageWidget(self.show_garage)
        self.garage_page = GarageViewWidget(self.show_home)

        # Add screens to stacked layout index
        self.stacked_widget.addWidget(self.home_page)  # Index 0
        self.stacked_widget.addWidget(self.garage_page)  # Index 1

        # Start on homepage
        self.show_home()

    def show_home(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_garage(self):
        self.stacked_widget.setCurrentWidget(self.garage_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())