import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QVBoxLayout, \
    QHBoxLayout, QFileDialog, QListWidget, QMessageBox, QDesktopWidget, QMainWindow, QAction, QMenu, QActionGroup, \
    QUndoStack, QToolButton, QDialog
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtCore import Qt, QFileInfo, QRect
from gui.options_manager import OptionsManager
from file_search.fileSearcher import FileSearcher
from duplicates_finder.comparisonMethod import ComparisonMethod
from gui.constructing_interface.toolbar import create_toolbar
from gui.constructing_interface.menubar import create_menubar
from gui.constructing_interface.context_menu import create_context_menu
from gui.constructing_interface.statusbar import create_status_bar
from gui.constructing_interface.actions import create_actions
from gui.drag_drop import dragEnterEvent, dropEvent
from gui.search_event_handlers import browse_folder, start_search, display_results, remove_sel_folder, \
    clear_search_list, browse_excluded_folder, remove_sel_excluded_folder, clear_excluded_list


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
        self.resize(800, 600)
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

        # кнопка начала поиска
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.start_search)

        # дисплей результатов поиска
        result_label = QLabel("Results:")
        self.result_listbox = QListWidget()

        # установка макетов
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addLayout(folder_layout)
        main_layout.addLayout(excluded_folder_layout)
        main_layout.addWidget(search_button)
        main_layout.addWidget(result_label)
        main_layout.addWidget(self.result_listbox)

        self.show()

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

    def browse_folder(self):
        browse_folder(self)

    def browse_excluded_folder(self):
        browse_excluded_folder(self)

    def start_search(self):
        start_search(self)

    def display_results(self, duplicates):
        display_results(self, duplicates)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImgDuplicatesFinder()
    sys.exit(app.exec_())
