import ctypes

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt

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
            item.setText(0, field_name)

            if isinstance(value, ctypes.Array):
                elem_type = field_type._type_

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
                        editor = self._create_editor(value[i])
                        self._set_inline_widget(sub_item, label, editor)

            elif isinstance(value, ctypes.Structure):
                self.build_tree(value, item)

            else:
                editor = self._create_editor(value)
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
        layout.addWidget(QLabel(label))
        layout.addWidget(editor)
        layout.setAlignment(Qt.AlignLeft)
        container.setLayout(layout)
        self.tree.setItemWidget(item, 0, container)

    def _create_editor(self, value):
        if isinstance(value, int):
            editor = QLineEdit(str(value))
        elif isinstance(value, float):
            editor = QLineEdit(str(value))
        elif isinstance(value, bytes):
            editor = QLineEdit(value.decode("ascii"))
        else:
            editor = QLineEdit(str(value))
        
        editor.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        return editor
