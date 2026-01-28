import ctypes
import array

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QGridLayout, QSizePolicy, QWidget, QFileDialog, QMessageBox, QProgressDialog, QListWidget, QListView
from PySide6.QtGui  import QFont, QIcon, QAction

from fanadi.qlog import c_save, c_dat, c_qlog
from fanadi.struct_editor import StructTreeEditor
from fanadi.gci import read_gci
from fanadi.widgets import *
from fanadi.const import *

from pathlib import Path
import copy

class QLogEditor(StructTreeEditor):
    def __init__(self, qlog: c_qlog, name: str):
        self.qlog = qlog
        self.name = name

        super().__init__(self.qlog.Save)

class FanadiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = QWidget()
        self.setCentralWidget(self.window)

        self.editor_tabs = QTabWidget()
        self.editor_tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.editors = []

        layout = QGridLayout(self.window)
        layout.addWidget(self.editor_tabs, 0, 0, 1, 1)

        self.save_previews = QListWidget()
        layout.addWidget(self.save_previews, 0, 1, 1, 1)
        self.save_previews.itemClicked.connect(self.preview_clicked_callback)
        self.save_previews.setUniformItemSizes(True)
        self.save_previews.setResizeMode(QListView.Adjust)

        layout.setColumnStretch(0, 5)
        layout.setColumnStretch(1, 2)

        self.file_menu = self.menuBar().addMenu("&File")
        self.edit_menu = self.menuBar().addMenu("&Edit")
        self.help_menu = self.menuBar().addMenu("&Help")

        self.open_gci_action = QAction("Open GCI", self)
        self.open_gci_action.triggered.connect(lambda: self.open_single_file_dialog("gci"))
        self.file_menu.addAction(self.open_gci_action)

        self.open_qlogs_action = QAction("Open QLog(s)", self)
        self.open_qlogs_action.triggered.connect(lambda: self.open_multi_file_dialog("qlog"))
        self.file_menu.addAction(self.open_qlogs_action)

        self.open_bin_action = QAction("Open Wii Save", self)
        self.open_bin_action.triggered.connect(lambda: self.open_single_file_dialog("bin"))
        self.file_menu.addAction(self.open_bin_action)

        self.file_menu.addSeparator()

        self.export_gci_action = QAction("Export GCI", self)
        self.export_gci_action.triggered.connect(self.export_gci)
        self.file_menu.addAction(self.export_gci_action)

        self.file_menu.addAction("Export QLog(s)")
        self.file_menu.addAction("Export Wii Save")

        self.resize(1000, 600)
        self.setWindowTitle("Fanadi")

    def preview_clicked_callback(self, item):
        self.editor_tabs.setCurrentIndex(self.save_previews.row(item))

    def create_editors(self, qlogs, names):
        bar = QProgressDialog("Loading...", None, 0, len(qlogs))
        bar.setWindowTitle("Loading...")
        bar.show()
        QApplication.processEvents()

        i = 0
        for qlog,name in zip(qlogs,names):
            self.add_editor(qlog, name)
            i += 1
            bar.setValue(i)
            QApplication.processEvents()

    def add_editor(self, qlog, name):
        editor = QLogEditor(qlog, name)
        self.editors.append(editor)
        self.editor_tabs.addTab(editor, editor.name)

        item = QListWidgetItem()
        preview = SavefileInfoWidget(editor.name, qlog, self.save_previews)
        self.save_previews.addItem(item)
        self.save_previews.setItemWidget(item, preview)
        item.setSizeHint(preview.sizeHint())  

    def clear_editors(self):
        self.editor_tabs.clear()

        for editor in self.editors:
            editor.deleteLater()
        
        self.save_previews.clear()

        self.editors = []

        QApplication.processEvents()

    def load_gci(self, filename):
        self.clear_editors()

        self.gci = read_gci(filename)
        ba = array.array("b")
        ba.frombytes(self.gci["m_save_data"][2])
        gci_save_data_struct = c_dat.from_buffer_copy(ba)

        qlogs = [gci_save_data_struct.Log1, gci_save_data_struct.Log2, gci_save_data_struct.Log3]

        self.create_editors(qlogs, [f"Log {i+1}" for i in range(3)])

    def load_qlogs(self, filenames):
        self.clear_editors()

        qlogs = []
        names = []

        for filename in filenames:
            with open(filename, "rb") as qlog:
                ba = array.array("b")
                ba.fromfile(qlog, ctypes.sizeof(c_save))
                c_save_struct = c_save.from_buffer_copy(ba)

            qlog_struct = c_qlog()
            qlog_struct.Save = c_save_struct
            qlogs.append(qlog_struct)
            names.append(Path(filename).stem)
        
        self.create_editors(qlogs, names)

    def load_bin(self, filename):
        QMessageBox.warning(self, "Error", "Not implemented yet!")

    def get_qlog_from_editor_index(self, index):
        return self.editors[index].qlog if index is not None else 0

    def export_gci(self):
        dialog = ExportSaveConfigureDialog([editor.name for editor in self.editors], REGIONS)

        if dialog.exec() == QDialog.Accepted:
            logs = dialog.get_logs()
            region = dialog.get_region()
            
            filename = self.save_single_file_dialog("gci")
            
            if filename:
                gci = copy.deepcopy(TEMPLATE_GCI)
                dat = c_dat()
                dat.Log1 = self.get_qlog_from_editor_index(logs[0]) or c_qlog()
                dat.Log2 = self.get_qlog_from_editor_index(logs[1]) or c_qlog()
                dat.Log3 = self.get_qlog_from_editor_index(logs[2]) or c_qlog()
                dat.DataVersion = DATA_VERSION
                dat.recalculate_checksums()

                gci["m_save_data"].append(bytes(dat))
                gci["m_save_data"].append(bytes(dat)) # backup
                gci["m_gci_header"]["Gamecode"] = region
                gci["m_gci_header"]["ModTime"] = datetime.now()

                with open(filename, "wb") as f:
                    f.write(write_gci(gci))

    def open_single_file_dialog(self, file_type):
        filename, filter = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file to open',
            dir='.',
            filter=f'{"GCI" if file_type == "gci" else "Wii Save"} Files (*.{file_type});;All Files (*.*)'
        )

        if filename:
            if file_type == "gci":
                self.load_gci(filename)
            elif file_type == "bin":
                self.load_bin(filename)

    def open_multi_file_dialog(self, file_type):
        filenames, filter = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Select files to open',
            dir='.',
            filter=f'QLog Files (*.bin);;All Files (*.*)'
        )

        if filenames:
            if file_type == "qlog":
                self.load_qlogs(filenames)

    def save_single_file_dialog(self, file_type):
        filename, filter = QFileDialog.getSaveFileName(
            parent=self,
            caption='Select a file to open',
            dir='.',
            filter=f'{"GCI" if file_type == "gci" else "Wii Save"} Files (*.{file_type});;All Files (*.*)'
        )

        return filename


    def change_tab(self, item):
        index = self.listWidget.row(item)
        self.tabWidget.setCurrentIndex(index)
