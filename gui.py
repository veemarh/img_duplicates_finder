import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QVBoxLayout, \
    QHBoxLayout, QFileDialog, QListWidget, QMessageBox, QDesktopWidget, QMainWindow, QAction, QMenu
from PyQt5.QtGui import QIcon, QFont


class ImgDuplicatesFinder(QMainWindow):
    def __init__(self):
        super().__init__()

        self._createActions()
        self._createMenuBar()
        self._createStatusBar()

        self.initUI()

    def _createActions(self):
        self.exitAction = QAction(QIcon("static/quit.png"), "&Quit", self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Quit application')
        self.exitAction.triggered.connect(self.close)

    def _createMenuBar(self):
        menubar = self.menuBar()
        file_menu = QMenu("&File", self)
        file_menu.addAction(self.exitAction)
        menubar.addMenu(file_menu)

    def _createStatusBar(self):
        statusbar = self.statusBar()
        # постоянное сообщение
        constant_message = "Constant"
        constant_message_label = QLabel(f"{constant_message}")
        statusbar.addPermanentWidget(constant_message_label)

    def initUI(self):
        self.resize(600, 450)
        self.center()
        self.setWindowTitle("Image Duplicates Finder")
        self.setWindowIcon(QIcon("static/icon.ico"))
        self.setFont(QFont("OpenSans", 10))

        # рабочая область
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # выбор папки
        folder_label = QLabel("Select Folder:")
        self.folder_entry = QLineEdit()
        self.folder_entry.setPlaceholderText("Enter an absolute folder path...")
        browse_button = QPushButton("Browse")
        # browse_button.setToolTip('Some notes')
        browse_button.clicked.connect(self.browse_folder)

        # макет горизонтального блока для секции выбора папки
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_entry)
        folder_layout.addWidget(browse_button)

        # выбор опций
        option_label = QLabel("Search Options:")
        self.exact_radio = QRadioButton("Exact Match")
        self.exact_radio.setChecked(True)
        self.resize_radio = QRadioButton("Match with Resize")
        self.filter_radio = QRadioButton("Match with Filter")

        # макет вертикального блока для секции выбора опций
        options_layout = QVBoxLayout()
        options_layout.addWidget(option_label)
        options_layout.addWidget(self.exact_radio)
        options_layout.addWidget(self.resize_radio)
        options_layout.addWidget(self.filter_radio)

        # кнопка начала поиска
        search_button = QPushButton("Start Search")
        search_button.clicked.connect(self.start_search)

        # дисплей результатов поиска
        result_label = QLabel("Results:")
        self.result_listbox = QListWidget()

        # установка макетов
        main_layout = QVBoxLayout(central_widget)
        main_layout.addLayout(folder_layout)
        main_layout.addLayout(options_layout)
        main_layout.addWidget(search_button)
        main_layout.addWidget(result_label)
        main_layout.addWidget(self.result_listbox)

        self.setLayout(main_layout)

        self.show()

    # выбор папки для поиска
    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_entry.setText(folder_path)

    # обработчик кнопки поиска
    def start_search(self):
        folder_path = self.folder_entry.text()
        if not folder_path:
            QMessageBox.warning(self, "Empty Folder Path", "Please select a folder to search for.")
            return

        option = 'exact' if self.exact_radio.isChecked() \
            else 'resize' if self.resize_radio.isChecked() \
            else 'filter'
        # Call your search function here and update the result_listbox with the results
        # For example: duplicates = find_duplicate_images(folder_path, option)
        # Then update the listbox with results
        self.display_results([])  # Replace with actual results

    # вывод результатов
    def display_results(self, duplicates):
        self.result_listbox.clear()
        if duplicates:
            for dup in duplicates:
                self.result_listbox.addItem(f"{dup[0]} and {dup[1]}")
        else:
            self.result_listbox.addItem("No duplicate images found.")

    # подтверждение выхода
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirm Quit', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # центрирование окна
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImgDuplicatesFinder()
    sys.exit(app.exec_())
