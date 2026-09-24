# homepage.py
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QLinearGradient, QPainter, QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class HomePageWidget(QWidget):

    def __init__(self, on_enter_garage_callback):
        super().__init__()
        self.on_enter_garage_callback = on_enter_garage_callback
        self.bg_image_path = "assets/gray.png"

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        # Main Title (border: none explicitly removes global QSS borders)
        title = QLabel("Garage")
        title.setStyleSheet("""
            QLabel {
                font-size: 52px;
                font-weight: bold;
                color: #ffffff;
                background: transparent;
                border: none;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtitle
        subtitle = QLabel("Welcome Home")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #e0e0e0;
                background: transparent;
                border: none;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Click prompt hint
        prompt = QLabel("Click anywhere to enter the garage")
        prompt.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #cccccc;
                background: transparent;
                border: none;
                margin-top: 20px;
            }
        """)
        prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(prompt)

    def mousePressEvent(self, event):
        """Allows clicking anywhere on the screen to enter the garage."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_enter_garage_callback()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        """Draws the background directly to bypass main window QSS overrides."""
        painter = QPainter(self)

        if os.path.exists(self.bg_image_path):
            pixmap = QPixmap(self.bg_image_path)
            scaled_pixmap = pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = (scaled_pixmap.width() - self.width()) // 2
            y = (scaled_pixmap.height() - self.height()) // 2
            painter.drawPixmap(0, 0, scaled_pixmap, x, y, self.width(), self.height())
        else:
            # Fallback dark gradient if file is missing
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, Qt.GlobalColor.darkGray)
            gradient.setColorAt(1, Qt.GlobalColor.black)
            painter.fillRect(self.rect(), gradient)

        super().paintEvent(event)