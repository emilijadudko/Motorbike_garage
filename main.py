import json
import os
import sys
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MotoSelectApp(QMainWindow):

  def __init__(self):
        super().__init__()
        self.setWindowTitle("Motorcycle Garage")
        self.resize(950, 650)

        self.settings = QSettings("MotoSelectOrg", "MotoSelectApp")
        self.bikes_data = self.load_bike_data()
        self.selected_bike = None

        # Track garage selections
        self.garage = {"A1": None, "A2": None, "Full A": None}

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        top_layout = QVBoxLayout(main_widget)

        # Upper Split (Left: Catalog & Filters, Right: Inspector)
        content_layout = QHBoxLayout()

        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("<b>License Category:</b>"))

        self.tier_combo = QComboBox()
        self.tier_combo.addItems(["A1", "A2", "Full A"])
        self.tier_combo.currentTextChanged.connect(self.filter_bikes)
        left_panel.addWidget(self.tier_combo)

        left_panel.addWidget(QLabel("<b>Available Models:</b>"))
        self.bike_list = QListWidget()
        self.bike_list.itemSelectionChanged.connect(self.display_bike_details)
        left_panel.addWidget(self.bike_list)

        content_layout.addLayout(left_panel, stretch=1)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        content_layout.addWidget(line)

        right_panel = QVBoxLayout()

        self.title_label = QLabel("Select a Bike")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # Center the title text
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_panel.addWidget(self.title_label)

        # Image display label
        self.image_label = QLabel()
        self.image_label.setFixedSize(320, 180)
        self.image_label.setStyleSheet(
            "border: 1px solid #ccc; background-color: #f0f0f0;"
        )
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Center the image widget in the panel layout
        right_panel.addWidget(
            self.image_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Spec details
        self.specs_label = QLabel("Choose a bike model from the catalog.")
        self.specs_label.setWordWrap(True)
        right_panel.addWidget(self.specs_label, stretch=1)

        # "Add to Garage" Button
        self.add_garage_btn = QPushButton("Add to My Garage")
        self.add_garage_btn.setEnabled(False)
        self.add_garage_btn.clicked.connect(self.add_to_garage)
        right_panel.addWidget(self.add_garage_btn)

        content_layout.addLayout(right_panel, stretch=2)
        top_layout.addLayout(content_layout, stretch=2)

        # Bottom Garage Section
        garage_group = QGroupBox("My Garage")
        garage_layout = QHBoxLayout(garage_group)

        self.garage_slots = {}
        for tier in ["A1", "A2", "Full A"]:
            slot_box = QVBoxLayout()

            title = QLabel(f"<b>{tier} Slot</b>")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            img_slot = QLabel()
            img_slot.setFixedSize(140, 80)
            img_slot.setAlignment(Qt.AlignmentFlag.AlignCenter)
            img_slot.setStyleSheet(
                "border: 1px dashed #555; background-color: #222;"
            )

            info_label = QLabel("<i>Empty Slot</i>")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_label.setWordWrap(True)

            slot_box.addWidget(title)
            slot_box.addWidget(
                img_slot, alignment=Qt.AlignmentFlag.AlignCenter
            )
            slot_box.addWidget(info_label)

            container = QFrame()
            container.setFrameShape(QFrame.Shape.StyledPanel)
            container.setLayout(slot_box)

            garage_layout.addWidget(container)

            # Map widgets directly to tier key
            self.garage_slots[tier] = {"info": info_label, "image": img_slot}

        top_layout.addWidget(garage_group, stretch=1)

        # Initial Setup
        self.filter_bikes(self.tier_combo.currentText())
        self.load_saved_garage()


  def load_bike_data(self):
        try:
            with open("bikes.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

  def filter_bikes(self, selected_tier):
        self.bike_list.clear()
        for bike in self.bikes_data:
            if bike["tier"] == selected_tier:
                self.bike_list.addItem(f"{bike['brand']} - {bike['name']}")

  def display_bike_details(self):
    selected_items = self.bike_list.selectedItems()
    if not selected_items:
        self.add_garage_btn.setEnabled(False)
        self.selected_bike = None
        return

    selected_text = selected_items[0].text()

    self.selected_bike = next(
        (
            b
            for b in self.bikes_data
            if f"{b['brand']} - {b['name']}" == selected_text
        ),
        None,
    )

    if self.selected_bike:
        self.add_garage_btn.setEnabled(True)
        name = self.selected_bike.get("name", "")
        brand = self.selected_bike.get("brand", "")
        display_title = (
            name if name.startswith(brand) else f"{brand} {name}"
        )
        self.title_label.setText(display_title)

        # Load Main Image
        img_path = self.selected_bike.get("image", "")
        if img_path and os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("No Image Available")

        # Specs output
        power_kw = self.selected_bike.get("powerHp", 0) * 0.7457
        weight = self.selected_bike.get("weightKg", 1)
        ptw_ratio = round(power_kw / weight, 3)

        details = (
            f"<b>Tier:</b> {self.selected_bike.get('tier', '')}<br>"
            f"<b>Power:</b> {self.selected_bike.get('powerHp', '')} HP ({round(power_kw, 1)} kW)<br>"
            f"<b>Weight:</b> {weight} kg<br>"
            f"<b>Power-to-Weight Ratio:</b> {ptw_ratio} kW/kg<br>"
            f"<b>Seat Height:</b> {self.selected_bike.get('seatHeightMm', '')} mm<br>"
            f"<b>Price:</b> {self.selected_bike.get('priceEstimate', '')}"
        )
        self.specs_label.setText(details)

  def add_to_garage(self):
        if not self.selected_bike:
            return

        tier = self.selected_bike.get("tier")
        if not tier:
            return

        # Assign selected bike to garage slot
        self.garage[tier] = self.selected_bike
        self.update_garage_ui()

        bike_id = self.selected_bike.get("id")
        if bike_id:
            self.settings.setValue(f"garage_{tier}", bike_id)
            
  def update_garage_ui(self):
        for tier, bike in self.garage.items():
            info_label = self.garage_slots[tier]["info"]
            img_label = self.garage_slots[tier]["image"]

            if bike:
                brand = bike.get("brand", "")
                name = bike.get("name", "")
                display_name = name if name.startswith(brand) else f"{brand} {name}"

                info_label.setText(
                    f"<b>{display_name}</b><br>"
                    f"⚡ {bike.get('powerHp', '--')} HP | {bike.get('weightKg', '--')} kg"
                )

                img_path = bike.get("image", "")
                if img_path and os.path.exists(img_path):
                    pixmap = QPixmap(img_path).scaled(
                        img_label.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    img_label.setPixmap(pixmap)
                    img_label.setStyleSheet("border: 1px solid #777;")
                else:
                    img_label.clear()
                    img_label.setText("No Image")
                    img_label.setStyleSheet("border: 1px solid #555;")
            else:
                info_label.setText("<i>Empty Slot</i>")
                img_label.clear()
                img_label.setText("")
                img_label.setStyleSheet(
                    "border: 1px dashed #555; background-color: #222;"
                )

  def load_saved_garage(self):
        """Restores garage slots on application startup."""
        for tier in ["A1", "A2", "Full A"]:
            saved_id = self.settings.value(f"garage_{tier}", None)
            if saved_id:
                bike = next(
                    (b for b in self.bikes_data if b["id"] == saved_id), None
                )
                if bike:
                    self.garage[tier] = bike
        self.update_garage_ui()


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MotoSelectApp()
  window.show()
  sys.exit(app.exec())