from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtGui import QFont


class ProgressWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Searching for duplicates")
        self.setFixedSize(350, 160)
        self.setFont(QFont("OpenSans", 10))

        layout = QVBoxLayout(self)

        label = QLabel("Please wait...", self)
        layout.addWidget(label)
        layout.addStretch()

        self.total_images_label = QLabel("Total images: 0", self)
        layout.addWidget(self.total_images_label)

        self.checked_images_label = QLabel("Checked images: 0", self)
        layout.addWidget(self.checked_images_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        # self.button_box = QDialogButtonBox(QDialogButtonBox.Cancel)
        # self.button_box.rejected.connect(self.reject)
        # layout.addWidget(self.button_box)

    def update_progress(self, total, checked, progress):
        self.total_images_label.setText(f"Total images: {total}")
        self.checked_images_label.setText(f"Checked images: {checked}")
        self.progress_bar.setValue(progress)
