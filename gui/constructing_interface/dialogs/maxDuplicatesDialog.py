from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSpinBox, QPushButton, QFormLayout
from PyQt5.QtGui import QFont


class MaxDuplicatesDialog(QDialog):
    def __init__(self, max_value):
        super().__init__()
        self.setWindowTitle("Set max duplicates")
        self.setFixedSize(300, 100)
        self.setFont(QFont("OpenSans", 10))
        self.max_value = max_value
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.form_layout.setHorizontalSpacing(32)
        self.max_duplicates_spinbox = QSpinBox()
        self.max_duplicates_spinbox.setMaximumWidth(200)
        self.max_duplicates_spinbox.setRange(1, 100000)
        self.max_duplicates_spinbox.setValue(self.max_value)
        self.form_layout.addRow("Max duplicates:", self.max_duplicates_spinbox)
        layout.addLayout(self.form_layout)

        button_box = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)

        layout.addLayout(button_box)


def open_max_duplicates_dialog(main_window):
    dialog = MaxDuplicatesDialog(main_window.options_manager.get_option("max_duplicates"))
    if dialog.exec_():
        max_duplicates = dialog.max_duplicates_spinbox.value()
        main_window.options_manager.set_option("max_duplicates", max_duplicates)
