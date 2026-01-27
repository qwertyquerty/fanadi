from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton
)
import sys

class ExportSaveConfigureDialog(QDialog):
    def __init__(self, qlogs, regions, parent=None, enable_region=True):
        super().__init__(parent)
        self.setWindowTitle("Configure Export")

        self.combos = []

        layout = QVBoxLayout(self)

        for i in range(3):
            row = QHBoxLayout()
            combo = QComboBox()

            combo.addItem("(None)", None)
            for item in qlogs:
                combo.addItem(item, i)

            combo.setCurrentIndex(min(i+1, len(qlogs)))

            self.combos.append(combo)
            row.addWidget(QLabel(f"Slot {i + 1}:"))
            row.addWidget(combo)
            layout.addLayout(row)
        
        row = QHBoxLayout()
        self.region = QComboBox()
        
        for region in regions:
            self.region.addItem(region, region)
        
        if enable_region:
            row.addWidget(QLabel("Region"))
            row.addWidget(self.region)
            layout.addLayout(row)

        button_row = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        button_row.addStretch()
        button_row.addWidget(ok_btn)
        button_row.addWidget(cancel_btn)

        layout.addLayout(button_row)

        self.resize(300, 200)

    def get_logs(self):
        return [combo.currentData() for combo in self.combos]

    def get_region(self):
        return self.region.currentData()
