from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QPushButton, \
    QHBoxLayout, QScrollArea, QWidget
from PyQt5.QtGui import QFont
from gui.algorithmsManager import get_algorithm_names, get_algorithm_description_by_name


class AlgorithmInfoDialog(QDialog):
    def __init__(self, algorithm):
        super().__init__()
        self.setWindowTitle("Algorithms Info")
        self.resize(800, 560)
        self.setFont(QFont("OpenSans", 10))
        self.selected_algorithm = algorithm
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.addWidget(QLabel("<h3>Algorithms Info</h3>"))

        self.radio_group = QButtonGroup(self)
        self.radio_group.setExclusive(True)

        for algo_name in get_algorithm_names():
            radio_button = QRadioButton(algo_name)
            radio_button.setFixedWidth(160)
            if algo_name == self.selected_algorithm:
                radio_button.setChecked(True)
            self.radio_group.addButton(radio_button)
            description = get_algorithm_description_by_name(algo_name)
            label = QLabel(description)
            label.setWordWrap(True)

            item_layout = QHBoxLayout()
            item_layout.addWidget(radio_button)
            item_layout.addSpacing(16)
            item_layout.addWidget(label, 1)

            item_widget = QWidget()
            item_widget.setLayout(item_layout)

            scroll_layout.addWidget(item_widget)

        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        select_button = QPushButton("Select")
        select_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(select_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def accept(self):
        selected_button = self.radio_group.checkedButton()
        if selected_button:
            self.selected_algorithm = selected_button.text()
        super().accept()


def open_algorithm_info_dialog(main_window):
    dialog = AlgorithmInfoDialog(main_window.options_manager.get_option("algorithm"))
    if dialog.exec_():
        algorithm = dialog.selected_algorithm
        main_window.options_manager.set_option("algorithm", algorithm)
        main_window.algorithm_actions[algorithm].setChecked(True)
