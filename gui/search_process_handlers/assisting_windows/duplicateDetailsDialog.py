from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, QWidget, \
    QListWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from datetime import datetime
import os
from send2trash import send2trash
import shutil


def get_file_info(file_path):
    file_name = os.path.basename(file_path)
    creation_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%d/%m/%y %H:%M:%S')
    return f"<b>Name:</b> {file_name}<br/><b>Path:</b> {file_path}<br/><b>Creation Date:</b> {creation_date}"


class DuplicateDetailsDialog(QDialog):
    def __init__(self, file_path, duplicates, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.creation_date = datetime.fromtimestamp(os.path.getctime(self.file_path)).strftime('%d/%m/%y %H:%M:%S')
        self.duplicates = duplicates
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"{os.path.basename(self.file_path)}")
        self.resize(800, 560)
        self.setFont(QFont("OpenSans", 10))
        layout = QVBoxLayout(self)

        # текущий файл
        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        main_image_label = QLabel(self)
        main_image_label.setFixedSize(200, 200)
        pixmap = QPixmap(self.file_path)
        main_image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        left_layout.addWidget(main_image_label)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignVCenter)
        file_name = os.path.basename(self.file_path)
        name_label = QLabel(f"<b>Name:</b> {file_name}")
        name_label.setWordWrap(True)
        path_label = QLabel(f"<b>Path:</b> {self.file_path}")
        path_label.setWordWrap(True)
        creation_date_label = QLabel(f"<b>Creation Date:</b> {self.creation_date}")
        creation_date_label.setWordWrap(True)
        right_layout.addWidget(name_label)
        right_layout.addWidget(path_label)
        right_layout.addWidget(creation_date_label)

        # кнопки
        # main_button_box = QVBoxLayout()
        # main_button_box.setAlignment(Qt.AlignVCenter)
        # main_move_button = QPushButton("Move")
        # main_move_button.clicked.connect(lambda _, p=self.file_path: self.move_file(p))
        # main_delete_button = QPushButton("Delete")
        # main_delete_button.clicked.connect(lambda _, p=self.file_path, b=main_delete_button: self.delete_file(p, b))
        # main_button_box.addWidget(main_move_button)
        # main_button_box.addWidget(main_delete_button)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout, 1)
        # main_layout.addLayout(main_button_box)
        layout.addLayout(main_layout)

        # список дубликатов
        duplicates_label = QLabel("Duplicates:")
        layout.addWidget(duplicates_label)

        self.duplicates_list = QListWidget()
        for duplicate_path in self.duplicates:
            if not os.path.isfile(duplicate_path):
                continue
            item = QListWidgetItem()
            item.setToolTip(get_file_info(duplicate_path))
            widget = QWidget()
            widget_layout = QHBoxLayout(widget)

            # изображения дубликатов
            duplicate_image_label = QLabel()
            duplicate_image_label.setFixedSize(80, 80)
            pixmap = QPixmap(duplicate_path)
            duplicate_image_label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio))
            widget_layout.addWidget(duplicate_image_label)

            # дубликаты
            duplicate_name = os.path.basename(duplicate_path)
            duplicate_name_label = QLabel(duplicate_name)
            duplicate_name_label.setWordWrap(True)
            widget_layout.addWidget(duplicate_name_label, 1)

            # кнопки перемещения и удаления
            move_button = QPushButton("Move")
            delete_button = QPushButton("Delete")
            move_button.clicked.connect(
                lambda _, p=duplicate_path, m=move_button, d=delete_button: self.move_file(p, m, d))
            delete_button.clicked.connect(
                lambda _, p=duplicate_path, m=move_button, d=delete_button: self.delete_file(p, m, d))
            widget_layout.addWidget(move_button)
            widget_layout.addWidget(delete_button)

            item.setSizeHint(widget.sizeHint())
            self.duplicates_list.addItem(item)
            self.duplicates_list.setItemWidget(item, widget)

        layout.addWidget(self.duplicates_list)

    def move_file(self, file_path, move_button, delete_button):
        if os.path.isfile(file_path):
            options = QFileDialog.Options()
            options |= QFileDialog.ShowDirsOnly
            directory = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
            if directory:
                reply = QMessageBox.question(self, "Confirm Move",
                                             f"<h3>Are you sure?</h3>"
                                             f"You want to move the file:<br/>{os.path.basename(file_path)}<br/><br/>"
                                             f"from:<br/>{os.path.dirname(file_path)}<br/><br/>"
                                             f"to:<br/>{directory}",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    try:
                        new_path = os.path.join(directory, os.path.basename(file_path))
                        shutil.move(file_path, new_path)
                        QMessageBox.information(self, "Success", "<h3>File Moved</h3>"
                                                                 f"File has been moved:<br/>{new_path}")
                        move_button.setEnabled(False)
                        delete_button.setEnabled(False)
                    except Exception as e:
                        QMessageBox.warning(self, "Error Occurred",
                                            "<h3>Something went wrong</h3>"
                                            f"An error occurred while moving the file:<br/>{str(e)}")
        else:
            QMessageBox.warning(self, "Error Occurred",
                                "<h3>File doesn't exist</h3>"
                                "The file may have been already deleted or removed.<br/><br/>")

    def delete_file(self, file_path, move_button, delete_button):
        if os.path.isfile(file_path):
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"<h3>Are you sure?</h3>You want to delete the file:<br/>{file_path}",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                path_to_delete = file_path.replace("/", "\\")
                send2trash(path_to_delete)
                move_button.setEnabled(False)
                delete_button.setEnabled(False)
        else:
            QMessageBox.warning(self, "Error Occurred",
                                "<h3>File doesn't exist</h3>"
                                "The file may have been already deleted or removed.<br/><br/>")
