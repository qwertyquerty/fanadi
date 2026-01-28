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

from fanadi.util import ctype_limits, is_ctypes_char_array

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
                editor.setMinimum(limits[0])
                editor.setMaximum(limits[1])
                editor.setValue(value)
            else:
                editor = QLineEdit()
                editor.setText(str(value))

        elif isinstance(value, float):
            editor = QLineEdit(str(value))

        elif isinstance(value, bytes):
            editor = QLineEdit(value.decode("latin-1", errors="ignore"))
            editor.setMaxLength(ctypes.sizeof(field_type))
            editor.setValidator(QRegularExpressionValidator(QRegularExpression(r"[\x00-\xFF]+")))

        else:
            editor = QLineEdit(str(value))

        editor.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        return editor

    def get_values_as_dict(self):
        def extract_value(editor):
            if isinstance(editor, QSpinBox):
                return editor.value()
            elif isinstance(editor, QComboBox):
                return editor.currentData()
            elif isinstance(editor, QLineEdit):
                text = editor.text()
                try:
                    if "." in text:
                        return float(text)
                    return int(text)
                except ValueError:
                    return text
            return None

        def walk_item(item):
            widget = self.tree.itemWidget(item, 0)
            if widget:
                label = widget.layout().itemAt(0).widget().text()
                editor = widget.layout().itemAt(1).widget()
                return label, extract_value(editor)

            result = {}
            array_items = []

            for i in range(item.childCount()):
                child = item.child(i)
                key, value = walk_item(child)

                if key.startswith("[") and key.endswith("]"):
                    array_items.append(value)
                else:
                    result[key] = value

            if array_items:
                return item.text(0), array_items

            return item.text(0), result

        data = {}
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            key, value = walk_item(item)
            data[key] = value

        return data

    def apply_dict_to_struct(self, data: dict, struct_instance=None):
        if struct_instance is None:
            struct_instance = self.struct_instance

        for field_name, field_type in struct_instance._fields_:
            if field_name.startswith("_"):
                continue

            if field_name not in data:
                continue

            value = data[field_name]
            current = getattr(struct_instance, field_name)

            if isinstance(current, ctypes.Structure):
                self.apply_dict_to_struct(value, current)
            elif isinstance(current, ctypes.Array):
                elem_type = field_type._type_

                if issubclass(elem_type, ctypes.Structure):
                    for i, elem_data in enumerate(value):
                        if i < len(current):
                            self.apply_dict_to_struct(elem_data, current[i])

                else:
                    for i, v in enumerate(value):
                        if i < len(current):
                            current[i] = elem_type(v)
            else:
                if is_ctypes_char_array(field_type):
                    setattr(struct_instance, field_name, value.encode("latin-1"))
                else:
                    setattr(struct_instance, field_name, field_type(value))
