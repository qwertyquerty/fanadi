from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QWidget, QListWidgetItem, QLayout, QGroupBox, QSizePolicy
)

from PySide6.QtCore import (
    Qt
)

import sys

from fanadi.const import OS_TIME_SPEED

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

class SavefileInfoWidget(QGroupBox):
    def __init__(self, name, qlog, parent=None):
        super().__init__(name, parent)
        self.qlog = qlog

        self.playtime_label = QLabel("")
        self.name_label = QLabel("")
        self.amounts_label = QLabel("")
        self.location_label = QLabel("")

        self.update_info()

        layout = QVBoxLayout()

        top_row = QHBoxLayout()
        top_row.addWidget(self.name_label)
        top_row.addWidget(self.playtime_label)

        bottom_row = QHBoxLayout()
        bottom_row.addWidget(self.amounts_label)
        bottom_row.addWidget(self.location_label)

        self.playtime_label.setAlignment(Qt.AlignRight)
        self.location_label.setAlignment(Qt.AlignRight)

        layout.addLayout(top_row)
        layout.addLayout(bottom_row)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setLayout(layout)
        self.setStyleSheet("QGroupBox { margin: 2px; background-color: 0x00000000; padding-top: 10px; } QLabel { font-size: 14px; padding: 0; margin: 0; }")

    def update_info(self):
        playtime_seconds = self.qlog.Save.Player.PlayerInfo.TotalTime / OS_TIME_SPEED
        player_name = self.qlog.Save.Player.PlayerInfo.PlayerName.decode()
        horse_name = self.qlog.Save.Player.PlayerInfo.HorseName.decode()
        hearts = self.qlog.Save.Player.PlayerStatusA.Life
        max_life = self.qlog.Save.Player.PlayerStatusA.MaxLife
        rupees = self.qlog.Save.Player.PlayerStatusA.Rupee
        deaths = self.qlog.Save.Player.PlayerInfo.DeathCount
        location = self.qlog.Save.Player.PlayerReturnPlace.Name.decode()
        room = self.qlog.Save.Player.PlayerReturnPlace.RoomNo

        self.name_label.setText(f"{player_name} / {horse_name}" if len(player_name) else "Empty File")
        self.playtime_label.setText(f"{int(playtime_seconds // 3600):02}:{int((playtime_seconds % 3600) // 60):02}:{int(playtime_seconds % 60):02}")
        self.amounts_label.setText(f"{hearts}♥ {max_life}♡ {rupees}R {deaths}💀")
        self.location_label.setText(f"{location}:{room}")
