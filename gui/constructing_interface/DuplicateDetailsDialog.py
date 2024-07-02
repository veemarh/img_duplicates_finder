from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, QWidget, \
    QListWidgetItem, QToolTip
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QEvent
from datetime import datetime
import os


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
        main_button_box = QVBoxLayout()
        main_button_box.setAlignment(Qt.AlignVCenter)
        main_move_button = QPushButton("Move")
        main_move_button.clicked.connect(lambda _, p=self.file_path: self.move_file(p))
        main_delete_button = QPushButton("Delete")
        main_delete_button.clicked.connect(lambda _, p=self.file_path: self.delete_file(p))
        main_button_box.addWidget(main_move_button)
        main_button_box.addWidget(main_delete_button)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout, 1)
        main_layout.addLayout(main_button_box)
        layout.addLayout(main_layout)

        # список дубликатов
        duplicates_label = QLabel("Duplicates:")
        layout.addWidget(duplicates_label)

        self.duplicates_list = QListWidget()
        for duplicate_path in self.duplicates:
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

            # кнопка перемещения
            move_button = QPushButton("Move")
            move_button.clicked.connect(lambda _, p=duplicate_path: self.move_file(p))
            widget_layout.addWidget(move_button)

            # кнопка удаления
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, p=duplicate_path: self.delete_file(p))
            widget_layout.addWidget(delete_button)

            item.setSizeHint(widget.sizeHint())
            self.duplicates_list.addItem(item)
            self.duplicates_list.setItemWidget(item, widget)

        layout.addWidget(self.duplicates_list)

    def move_file(self, file_path):
        pass

    def delete_file(self, file_path):
        pass
