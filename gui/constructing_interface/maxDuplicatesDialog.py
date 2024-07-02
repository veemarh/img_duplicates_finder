from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSpinBox, QPushButton, QFormLayout
from PyQt5.QtGui import QFont


class MaxDuplicatesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set max duplicates")
        self.setFixedSize(300, 100)
        self.setFont(QFont("OpenSans", 10))
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.form_layout.setHorizontalSpacing(32)
        self.max_duplicates_spinbox = QSpinBox()
        self.max_duplicates_spinbox.setMaximumWidth(200)
        self.max_duplicates_spinbox.setRange(1, 100000)
        self.max_duplicates_spinbox.setValue(self.parent().options_manager.options.get("max_duplicates", 1000))
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

    def accept(self):
        self.parent().options_manager.options["max_duplicates"] = self.max_duplicates_spinbox.value()
        super().accept()
