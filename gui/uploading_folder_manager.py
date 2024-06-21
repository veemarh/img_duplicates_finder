from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt


def toggle_uploading_folder_search(self, state):
    enabled = state == Qt.Checked
    self.uploading_folder_path_edit.setEnabled(enabled)
    self.uploading_folder_browse_button.setEnabled(enabled)
    self.options_manager.set_option("select_uploading_folder", enabled)


def set_uploading_folder(self, text):
    self.options_manager.set_option("uploading_folder_path", text)


def browse_uploading_folder(self):
    uploading_folder_path = QFileDialog.getExistingDirectory(self, "Select Uploading Folder")
    if uploading_folder_path:
        self.uploading_folder_path_edit.setText(uploading_folder_path)
