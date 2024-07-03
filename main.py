import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QListWidget, QMessageBox, QDesktopWidget, QMainWindow, QCheckBox, QUndoStack, QTableWidget, QHeaderView, \
    QAbstractItemView
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from gui.optionsManager import OptionsManager
from file_search.fileSearcher import FileSearcher
from duplicates_finder.comparisonMethod import ComparisonMethod
from gui.constructing_interface.toolbar import create_toolbar
from gui.constructing_interface.menubar import create_menubar
from gui.constructing_interface.context_menu import create_context_menu
from gui.constructing_interface.statusbar import create_status_bar
from gui.constructing_interface.actions import create_actions
from gui.drag_drop import dragEnterEvent, dropEvent
from gui.search_event_handlers import browse_folder, start_search, display_results, remove_sel_folder, \
    clear_search_list, browse_excluded_folder, remove_sel_excluded_folder, clear_excluded_list, show_duplicate_details
from gui.specificFileManager import toggle_specific_file_search, set_specific_file, browse_file
from gui.uploadingFolderManager import toggle_uploading_folder_search, set_uploading_folder, browse_uploading_folder


class ImgDuplicatesFinder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.undo_stack = QUndoStack(self)
        self.options_manager = OptionsManager()
        self._createActions()
        self._createToolbar()
        self._createMenuBar()
        self._createStatusBar()

        self.file_searcher = FileSearcher()
        self.method = ComparisonMethod()
        self.search_list = self.file_searcher.folders_for_search
        self.excluded_list = self.file_searcher.excluded_folders

        self.initUI()

    def _createActions(self):
        create_actions(self)

    def _createToolbar(self):
        self.addToolBar(create_toolbar(self))

    def _createMenuBar(self):
        self.setMenuBar(create_menubar(self))

    def _createStatusBar(self):
        self.setStatusBar(create_status_bar(self))

    def contextMenuEvent(self, event):
        create_context_menu(self, event)

    def initUI(self):
        self.resize(1200, 600)
        self.center()
        self.setWindowTitle("Image Duplicates Finder")
        self.setWindowIcon(QIcon("static/icon.ico"))
        self.setFont(QFont("OpenSans", 10))
        self.setAcceptDrops(True)

        # рабочая область
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # выбор папки
        folder_label = QLabel("Drag folders here to add them to your search list")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_folder)
        self.dnd_space = QListWidget()
        self.dnd_space.setWordWrap(True)
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.remove_sel_folder)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_search_list)

        # макет блока для секции выбора папки
        folder_layout = QVBoxLayout()
        folder_layout.addWidget(folder_label, alignment=Qt.AlignCenter)
        folder_layout.addWidget(self.dnd_space)
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(browse_button)
        buttons_layout.addWidget(remove_button)
        buttons_layout.addWidget(clear_button)
        folder_layout.addLayout(buttons_layout)

        # папки, в которых не нужно искать
        excluded_folder_label = QLabel("Specify the folders in which you do not need to search")
        excluded_browse_button = QPushButton("Browse")
        excluded_browse_button.clicked.connect(self.browse_excluded_folder)
        self.excluded_dnd_space = QListWidget()
        self.excluded_dnd_space.setWordWrap(True)
        excluded_remove_button = QPushButton("Remove")
        excluded_remove_button.clicked.connect(self.remove_sel_excluded_folder)
        excluded_clear_button = QPushButton("Clear")
        excluded_clear_button.clicked.connect(self.clear_excluded_list)

        # блок выбора папкок, в которых не нужно искать
        excluded_folder_layout = QVBoxLayout()
        excluded_folder_layout.addWidget(excluded_folder_label, alignment=Qt.AlignCenter)
        excluded_folder_layout.addWidget(self.excluded_dnd_space)
        excluded_buttons_layout = QHBoxLayout()
        excluded_buttons_layout.addStretch(1)
        excluded_buttons_layout.addWidget(excluded_browse_button)
        excluded_buttons_layout.addWidget(excluded_remove_button)
        excluded_buttons_layout.addWidget(excluded_clear_button)
        excluded_folder_layout.addLayout(excluded_buttons_layout)

        # опция поиска конкретного файла
        self.search_specific_file_checkbox = QCheckBox("Search for duplicates of a specific file")
        self.search_specific_file_checkbox.stateChanged.connect(self.toggle_specific_file_search)
        self.specific_file_path_edit = QLineEdit()
        self.specific_file_path_edit.setPlaceholderText("Enter file path")
        self.specific_file_path_edit.setEnabled(False)
        self.specific_file_path_edit.textChanged.connect(self.set_specific_file)

        self.file_browse_button = QPushButton("Browse")
        self.file_browse_button.clicked.connect(self.browse_file)
        self.file_browse_button.setEnabled(False)

        # макет для поиска конкретного файла
        specific_file_layout = QHBoxLayout()
        specific_file_layout.addWidget(self.search_specific_file_checkbox)
        specific_file_layout.addWidget(self.specific_file_path_edit)
        specific_file_layout.addWidget(self.file_browse_button)

        # опция выбора папки для загрузки
        self.select_uploading_folder_checkbox = QCheckBox("Upload found duplicates to a folder")
        self.select_uploading_folder_checkbox.stateChanged.connect(self.toggle_uploading_folder_search)
        self.uploading_folder_path_edit = QLineEdit()
        self.uploading_folder_path_edit.setPlaceholderText("Enter folder path")
        self.uploading_folder_path_edit.setEnabled(False)
        self.uploading_folder_path_edit.textChanged.connect(self.set_uploading_folder)

        self.uploading_folder_browse_button = QPushButton("Browse")
        self.uploading_folder_browse_button.clicked.connect(self.browse_uploading_folder)
        self.uploading_folder_browse_button.setEnabled(False)

        # макет для выбора папки для загрузки
        uploading_folder_layout = QHBoxLayout()
        uploading_folder_layout.addWidget(self.select_uploading_folder_checkbox)
        uploading_folder_layout.addWidget(self.uploading_folder_path_edit)
        uploading_folder_layout.addWidget(self.uploading_folder_browse_button)

        # кнопка начала поиска
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.start_search)

        # дисплей результатов поиска
        result_label = QLabel("Results:")
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Name", "Creation Date", "Duplicates", "Path"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setRowCount(1)
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.result_table.cellDoubleClicked.connect(self.show_duplicate_details)

        # установка макетов
        main_layout = QHBoxLayout(self.central_widget)
        settings_layout = QVBoxLayout()
        result_layout = QVBoxLayout()
        settings_layout.addLayout(folder_layout)
        settings_layout.addLayout(excluded_folder_layout)
        settings_layout.addLayout(specific_file_layout)
        settings_layout.addLayout(uploading_folder_layout)
        settings_layout.addWidget(search_button)
        result_layout.addWidget(result_label)
        result_layout.addWidget(self.result_table)
        main_layout.addLayout(settings_layout)
        main_layout.addLayout(result_layout)

        self.show()

    # подтверждение выхода
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Quit", "<h3>Confirm quit</h3>Are you sure you want to quit?",
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

    # о приложении
    def about(self):
        QMessageBox.about(self, "About Img Duplicates Finder",
                          "<h3>About Img Duplicates Finder</h3>"
                          "Built on June 4, 2024<br/><br/>"
                          "For non-commercial use only.<br/><br/>"
                          "Contributors: <a href='https://github.com/soneXgo'>soneXgo</a> "
                          "and <a href='https://github.com/veemarh'>veemarh</a>.<br/>"
                          "To view source code visit "
                          "<a href='https://github.com/veemarh/img_duplicates_finder'>repository on GitHub</a>.<br/>"
                          "Copyright ©2024")

    def browse_folder(self):
        browse_folder(self)

    def browse_excluded_folder(self):
        browse_excluded_folder(self)

    def start_search(self):
        try:
            start_search(self)
        except Exception as e:
            QMessageBox.warning(self, "Oops!",
                                "<h3>Error occurred</h3>"
                                "Something went wrong. Please check the entered data.<br/><br/>"
                                f"<b>Error:</b><br/>{type(e).__name__}<br/>"
                                f"<b>Details:</b><br/>{str(e)}")

    def display_results(self, duplicates, num):
        display_results(self, duplicates, num)

    def remove_sel_folder(self):
        remove_sel_folder(self)

    def remove_sel_excluded_folder(self):
        remove_sel_excluded_folder(self)

    def clear_search_list(self):
        clear_search_list(self)

    def clear_excluded_list(self):
        clear_excluded_list(self)

    def dragEnterEvent(self, event):
        dragEnterEvent(event)

    def dropEvent(self, event):
        dropEvent(self, event)

    def undo_action(self):
        self.undo_stack.undo()

    def redo_action(self):
        self.undo_stack.redo()

    def toggle_specific_file_search(self, state):
        toggle_specific_file_search(self, state)

    def set_specific_file(self, text):
        set_specific_file(self, text)

    def browse_file(self):
        browse_file(self)

    def toggle_uploading_folder_search(self, state):
        toggle_uploading_folder_search(self, state)

    def set_uploading_folder(self, text):
        set_uploading_folder(self, text)

    def browse_uploading_folder(self):
        browse_uploading_folder(self)

    def show_duplicate_details(self, row):
        try:
            show_duplicate_details(self, row)
        except Exception:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImgDuplicatesFinder()
    sys.exit(app.exec_())
