import unittest
import os

from fanadi.qlog import *
from fanadi.struct_editor import StructTreeEditor

from PySide6.QtWidgets import QApplication

class TestStructTreeEditor(unittest.TestCase):
    def test_export_diff(self):
        QApplication()

        for filename in os.listdir(os.path.join(".", "test_data", "qlogs")):
            save_original = c_save.from_qlog_file(os.path.join(".", "test_data", "qlogs", filename))
            save_tree = c_save.from_qlog_file(os.path.join(".", "test_data", "qlogs", filename))

            tree_editor = StructTreeEditor(save_tree)
            tree_editor.apply_dict_to_struct(tree_editor.get_values_as_dict(), save_tree)
            
            self.assertEqual(bytes(save_original), bytes(save_tree))


if __name__ == '__main__':
    unittest.main()
