import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QVBoxLayout, \
    QHBoxLayout, QFileDialog, QListWidget, QMessageBox, QDesktopWidget, QMainWindow, QAction, QMenu
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtCore import Qt, QFileInfo, QRect


class ImgDuplicatesFinder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.search_list = set()
        self._createActions()
        self._createToolbar()
        self._createMenuBar()
        self._createStatusBar()

        self.initUI()

    def _createActions(self):
        self.exitAction = QAction(QIcon("static/quit.png"), "&Quit", self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Quit application')
        self.exitAction.triggered.connect(self.close)
        self.helpContentAction = QAction(QIcon("static/readme.png"), "&About", self)
        self.helpContentAction.setStatusTip("Show the Img Duplicates Finder's About box")
        self.helpContentAction.triggered.connect(self.about)

    def _createToolbar(self):
        toolbar = self.addToolBar('Tools')
        # toolbar.addAction(self.exitAction)

    def _createMenuBar(self):
        menubar = self.menuBar()
        file_menu = QMenu("&File", self)
        file_menu.addAction(self.exitAction)
        menubar.addMenu(file_menu)
        about_menu = QMenu("&Help", self)
        about_menu.addAction(self.helpContentAction)
        menubar.addMenu(about_menu)

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
        self.setAcceptDrops(True)

        # рабочая область
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # выбор папки
        folder_label = QLabel("Drag folders here to add them to your search list")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_folder)
        self.dnd_space = QListWidget()
        self.dnd_space.setWordWrap(True)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clearSearchList)

        # макет блока для секции выбора папки
        folder_layout = QVBoxLayout()
        folder_layout.addWidget(folder_label, alignment=Qt.AlignCenter)
        folder_layout.addWidget(self.dnd_space)
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(browse_button)
        buttons_layout.addWidget(clear_button)
        folder_layout.addLayout(buttons_layout)

        # выбор опций
        # option_label = QLabel("Search Options:")
        # self.exact_radio = QRadioButton("Exact Match")
        # self.exact_radio.setChecked(True)
        # self.resize_radio = QRadioButton("Match with Resize")
        # self.filter_radio = QRadioButton("Match with Filter")

        # макет вертикального блока для секции выбора опций
        # options_layout = QVBoxLayout()
        # options_layout.addWidget(option_label)
        # options_layout.addWidget(self.exact_radio)
        # options_layout.addWidget(self.resize_radio)
        # options_layout.addWidget(self.filter_radio)

        # кнопка начала поиска
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.start_search)

        # дисплей результатов поиска
        result_label = QLabel("Results:")
        self.result_listbox = QListWidget()

        # установка макетов
        main_layout = QVBoxLayout(central_widget)
        main_layout.addLayout(folder_layout)
        # main_layout.addLayout(options_layout)
        main_layout.addWidget(search_button)
        main_layout.addWidget(result_label)
        main_layout.addWidget(self.result_listbox)

        self.show()

    # выбор папки для поиска
    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path and self.addToSearchList(folder_path):
            self.dnd_space.addItem(f"{folder_path}")

    # обработчик кнопки поиска
    def start_search(self):
        if not self.search_list:
            QMessageBox.warning(self, "Empty Folder Path", "Please select a folder to search for.")
            return

        # option = 'exact' if self.exact_radio.isChecked() \
        #     else 'resize' if self.resize_radio.isChecked() \
        #     else 'filter'
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
    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Confirm Quit', "Are you sure to quit?",
    #                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    # центрирование окна
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # о приложении
    def about(self):
        QMessageBox.about(self, "About Img Duplicates Finder", "<h3>About Img Duplicates Finder</h3>"
                                                               "<a href='https://github.com/soneXgo/img_duplicates_finder'>GitHub</a>")

    # drag'n'drop
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        dnd_rect = self.dnd_space.rect()
        mouse_pos = self.dnd_space.mapFromGlobal(QCursor.pos())
        if dnd_rect.contains(mouse_pos):
            paths = [u.toLocalFile() for u in event.mimeData().urls()]
            for path in paths:
                if QFileInfo(path).isDir() and self.addToSearchList(path):
                    self.dnd_space.addItem(f"{path}")

    def clearSearchList(self):
        self.search_list.clear()
        self.dnd_space.clear()

    # синхронизация серверного и клиентского списков
    def addToSearchList(self, item):
        if item not in self.search_list:
            self.search_list.add(f"{item}")
            return True
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImgDuplicatesFinder()
    sys.exit(app.exec_())
