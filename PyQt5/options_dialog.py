from PyQt5.QtWidgets import QDialog, QFormLayout, QCheckBox, QDialogButtonBox


class OptionsDialog(QDialog):
    def __init__(self, options, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Options")

        self.layout = QFormLayout(self)

        self.checkboxes = {}
        for option, value in options.items():
            checkbox = QCheckBox(option)
            checkbox.setChecked(value)
            self.layout.addRow(checkbox)
            self.checkboxes[option] = checkbox

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def get_options(self):
        return {option: checkbox.isChecked() for option, checkbox in self.checkboxes.items()}
