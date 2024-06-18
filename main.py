import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QVBoxLayout, \
    QHBoxLayout, QFileDialog, QListWidget, QMessageBox, QDesktopWidget, QMainWindow, QAction, QMenu, QActionGroup, \
    QUndoStack, QToolButton, QDialog
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtCore import Qt, QFileInfo, QRect
from gui.undo_commands import AddFolderCommand, ClearSearchListCommand, RemoveSelFolderCommand
from gui.options_dialog import OptionsDialog
from gui.options_manager import *
from file_search.fileSearcher import FileSearcher
from duplicates_finder.duplicatesFinder import DuplicatesFinder
from duplicates_finder.comparisonMethod import ComparisonMethod
from gui.constructing_interface.toolbar import create_toolbar
from gui.constructing_interface.menubar import create_menubar
from gui.constructing_interface.context_menu import create_context_menu
from gui.constructing_interface.statusbar import create_status_bar
from gui.constructing_interface.actions import create_actions


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

        # кнопка начала поиска
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.start_search)

        # дисплей результатов поиска
        result_label = QLabel("Results:")
        self.result_listbox = QListWidget()

        # установка макетов
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addLayout(folder_layout)
        main_layout.addWidget(search_button)
        main_layout.addWidget(result_label)
        main_layout.addWidget(self.result_listbox)

        self.show()

    # выбор папки для поиска
    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path and folder_path not in self.search_list:
            command = AddFolderCommand(folder_path, self.dnd_space, self.search_list)
            self.undo_stack.push(command)

    # обработчик кнопки поиска
    def start_search(self):
        if not self.search_list:
            QMessageBox.warning(self, "Empty Folder Path", "Please select a folder for search.")
            return

        self.file_searcher.file_formats = ['.png', '.jpg', '.jpeg']
        # img params
        images = self.file_searcher.search()
        # method params
        dupl_finder = DuplicatesFinder(self.method)
        dupl_finder.files = images[0]
        # finder params
        dupl_finder.find()

        # self.display_results(dups)

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
            paths = set([u.toLocalFile() for u in event.mimeData().urls()])
            for path in paths:
                if QFileInfo(path).isDir() and path not in self.search_list:
                    command = AddFolderCommand(path, self.dnd_space, self.search_list)
                    self.undo_stack.push(command)

    def clear_search_list(self):
        if self.search_list:
            command = ClearSearchListCommand(self.dnd_space, self.search_list)
            self.undo_stack.push(command)

    def undo_action(self):
        self.undo_stack.undo()

    def redo_action(self):
        self.undo_stack.redo()

    def remove_sel_folder(self):
        sel_item = self.dnd_space.currentItem()
        if sel_item:
            command = RemoveSelFolderCommand(sel_item.text(), self.dnd_space, self.search_list)
            self.undo_stack.push(command)

    def open_options_dialog(self):
        dialog = OptionsDialog(self.options_manager.options, self)
        if dialog.exec_() == QDialog.Accepted:
            self.options_manager.options = dialog.get_options()
            self.update_options()
            print(self.options_manager.options)

    def update_options(self):
        self.recursiveSearchAction.setChecked(self.options_manager.options["recursive_search"])
        self.currentSearchAction.setChecked(not self.options_manager.options["recursive_search"])

        search_by = self.options_manager.options.get("search_by")
        if search_by == "Content":
            self.byContentAction.setChecked(True)
        elif search_by == "Name":
            self.byNameAction.setChecked(True)
        elif search_by == "Size":
            self.bySizeAction.setChecked(True)

        algorithm = self.options_manager.options.get("algorithm")
        if algorithm == "aHash":
            self.aHashAction.setChecked(True)
        elif algorithm == "pHash":
            self.pHashAction.setChecked(True)
        elif algorithm == "ORB":
            self.orbAction.setChecked(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImgDuplicatesFinder()
    sys.exit(app.exec_())
