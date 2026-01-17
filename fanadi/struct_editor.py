import ctypes
from enum import Enum

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QHBoxLayout,
    QSizePolicy,
    QComboBox,
    QSpinBox
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QIntValidator, QRegularExpressionValidator

from fanadi.util import ctype_limits

class StructTreeEditor(QWidget):
    def __init__(self, struct_instance):
        super().__init__()
        self.struct_instance = struct_instance

        layout = QVBoxLayout(self)
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setColumnCount(1)
        layout.addWidget(self.tree)

        self.build_tree(self.struct_instance)

    def build_tree(self, struct_instance, parent=None):
        if parent is None:
            parent = self.tree.invisibleRootItem()

        for field_name, field_type in struct_instance._fields_:
            if field_name.startswith("_"):
                continue

            value = getattr(struct_instance, field_name)
            item = QTreeWidgetItem(parent)

            if isinstance(value, ctypes.Array):
                elem_type = field_type._type_
                item.setText(0, field_name)
                if issubclass(elem_type, ctypes.Structure):
                    for idx, elem in enumerate(value):
                        child_item = QTreeWidgetItem(item)
                        child_item.setText(0, f"[{idx}]")
                        self.build_tree(elem, child_item)

                else:
                    for i in range(len(value)):
                        sub_item = QTreeWidgetItem()
                        item.addChild(sub_item)
                        label = f"[{i}]"
                        editor = self._create_editor(value[i], field_name, field_type._type_, struct_instance)
                        self._set_inline_widget(sub_item, label, editor)

            elif isinstance(value, ctypes.Structure):
                item.setText(0, field_name)
                self.build_tree(value, item)

            else:
                editor = self._create_editor(value, field_name, field_type, struct_instance)
                self._set_inline_widget(item, field_name, editor)

        self.collapse_all_items()

    def collapse_all_items(self):
        def collapse(item):
            item.setExpanded(False)
            for i in range(item.childCount()):
                collapse(item.child(i))

        for i in range(self.tree.topLevelItemCount()):
            collapse(self.tree.topLevelItem(i))

    def _set_inline_widget(self, item, label, editor):
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(4, 2, 4, 2)
        label = QLabel(label)
        label.setMinimumWidth(150)
        editor.setMinimumWidth(150)
        layout.addWidget(label)
        layout.addWidget(editor)
        layout.setAlignment(Qt.AlignLeft)
        container.setLayout(layout)
        self.tree.setItemWidget(item, 0, container)

    def _create_editor(self, value, field_name, field_type, parent_struct):
        if hasattr(parent_struct, "_field_ui_types_") and field_name in parent_struct._field_ui_types_:
            ui_type = parent_struct._field_ui_types_[field_name]

            if issubclass(ui_type, Enum):
                editor = QComboBox()
                for item in ui_type:
                    editor.addItem(item.name, item.value)
                    if value == item.value:
                        editor.setCurrentText(item.name)

        elif isinstance(value, int):
            limits = ctype_limits(field_type)
            if (ctype_limits(field_type)[1] < (2**31)):
                editor = QSpinBox()
                editor.setValue(value)
                editor.setMinimum(limits[0])
                editor.setMaximum(limits[1])
            else:
                editor = QLineEdit()
                editor.setText(str(value))

        elif isinstance(value, float):
            editor = QLineEdit(str(value))

        elif isinstance(value, bytes):
            editor = QLineEdit(value.decode("ascii", errors="ignore"))
            editor.setMaxLength(ctypes.sizeof(field_type))
            editor.setValidator(QRegularExpressionValidator(QRegularExpression(r"[\x00-\xFF]+")))

        else:
            editor = QLineEdit(str(value))

        editor.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        return editor
