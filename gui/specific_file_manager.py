from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt


def toggle_specific_file_search(self, state):
    enabled = state == Qt.Checked
    self.specific_file_path_edit.setEnabled(enabled)
    self.file_browse_button.setEnabled(enabled)
    self.options_manager.set_option("search_specific_file", enabled)


def set_specific_file(self, text):
    self.options_manager.set_option("specific_file_path", text)


def browse_file(self):
    file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
    if file_path:
        self.specific_file_path_edit.setText(file_path)
