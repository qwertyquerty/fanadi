import sys
import ctypes
import array

import qtvscodestyle as qtvsc
from PySide6.QtWidgets import QApplication

from fanadi.qlog import c_save
from fanadi.struct_editor import StructTreeEditor

app = QApplication(sys.argv)

with open("morpheel.bin", "rb") as qlog:
    ba = array.array('b')
    ba.fromfile(qlog, ctypes.sizeof(c_save))
    qlog_struct = c_save.from_buffer_copy(ba)


editor = StructTreeEditor(qlog_struct)
editor.setWindowTitle("Fanadi")
editor.resize(1600, 900)
editor.show()

stylesheet = qtvsc.load_stylesheet(qtvsc.Theme.DARK_VS)
app.setStyleSheet(stylesheet)

sys.exit(app.exec())
