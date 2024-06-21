from PyQt5.QtWidgets import QDialog, QFormLayout, QCheckBox, QDialogButtonBox, QVBoxLayout, \
    QFrame, QLabel, QSpacerItem, QSizePolicy, QComboBox, QScrollArea, QWidget, QDateEdit, QSlider, QSpinBox, QLineEdit, \
    QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class OptionsDialog(QDialog):
    def __init__(self, options):
        super().__init__()

        self.setWindowTitle("General options")
        self.setFont(QFont("OpenSans", 10))
        self.options = options

        dlg_layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumSize(560, 400)
        self.scroll_widget = QWidget()
        self.form_layout = QFormLayout(self.scroll_widget)
        self.form_layout.setHorizontalSpacing(32)
        self.form_layout.addRow(QLabel("<h3>General options</h3>"))

        self.add_separator("<b>Search options</b>")
        self.create_folder_options()
        self.create_specific_file_option()
        self.add_separator("<b>Image properties</b>")
        self.create_image_property_options()
        self.add_separator("<b>Comparison parameters</b>")
        self.create_algorithm_options()
        self.create_similarity_threshold_options()
        self.create_algorithm_specific_options()
        self.add_separator("<b>When searching for duplicates</b>")
        self.create_max_duplicates_option()
        self.create_search_by_options()
        self.add_separator("<b>Modifications</b>")
        self.create_modified_options()
        self.add_separator("<b>File formats</b>")
        self.create_file_format_options()

        self.scroll_area.setWidget(self.scroll_widget)
        dlg_layout.addWidget(self.scroll_area)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        dlg_layout.addWidget(buttons)

    def create_specific_file_option(self):
        self.specific_file_checkbox = QCheckBox("Search for duplicates of a specific file")
        self.specific_file_checkbox.setChecked(self.options.get("search_specific_file", False))
        self.form_layout.addRow(self.specific_file_checkbox)

    def create_folder_options(self):
        self.folder_combo = QComboBox()
        self.folder_combo.setMaximumWidth(200)
        self.folder_combo.addItems(["Recursive Search", "In the Current Folder"])

        if self.options.get("recursive_search"):
            self.folder_combo.setCurrentIndex(0)
        else:
            self.folder_combo.setCurrentIndex(1)

        self.form_layout.addRow("Folders for search:", self.folder_combo)

    def create_search_by_options(self):
        self.search_by_name = QCheckBox("Search by Name")
        self.search_by_format = QCheckBox("Search by Format")
        self.search_by_size = QCheckBox("Search by Size")

        search_by = self.options.get("search_by", {})
        self.search_by_name.setChecked(search_by.get("Name", False))
        self.search_by_format.setChecked(search_by.get("Format", False))
        self.search_by_size.setChecked(search_by.get("Size", False))

        self.form_layout.addRow(self.search_by_name)
        self.form_layout.addRow(self.search_by_format)
        self.form_layout.addRow(self.search_by_size)

    def create_algorithm_options(self):
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.setMaximumWidth(200)
        algorithms = ["aHash", "bHash", "dHash", "mHash", "pHash", "MD5", "SHA-1, 160 bit", "SHA-2, 256 bit",
                      "SHA-2, 384 bit", "SHA-2, 512 bit", "ORB"]
        self.algorithm_combo.addItems(algorithms)

        selected_algorithm = self.options.get("algorithm")
        if selected_algorithm in algorithms:
            self.algorithm_combo.setCurrentIndex(algorithms.index(selected_algorithm))

        self.algorithm_combo.currentTextChanged.connect(self.update_algorithm_specific_options)
        self.form_layout.addRow("Algorithm:", self.algorithm_combo)

    def create_image_property_options(self):
        self.limit_size = QCheckBox("Limit Size")
        self.limit_size.setChecked(self.options.get("limit_size", False))
        self.limit_size.toggled.connect(self.toggle_size_limits)

        self.size_value = QLineEdit()
        self.size_value.setMaximumWidth(128)
        self.size_value.setText(self.options.get("size_value"))
        self.size_value.setEnabled(self.limit_size.isChecked())

        self.size_unit = QComboBox()
        self.size_unit.setMaximumWidth(96)
        size_units = ["bytes", "kb", "mb"]
        self.size_unit.addItems(size_units)
        selected_unit = self.options.get("size_unit")
        self.size_unit.setCurrentIndex(size_units.index(selected_unit))
        self.size_unit.setEnabled(self.limit_size.isChecked())

        limit_size_hbox = QHBoxLayout()
        limit_size_hbox.addWidget(self.size_value)
        limit_size_hbox.addWidget(self.size_unit)
        limit_size_hbox.addStretch()
        self.form_layout.addRow(self.limit_size, limit_size_hbox)

        self.limit_creation_date = QCheckBox("Limit Creation Date")
        self.limit_creation_date.setChecked(self.options.get("limit_creation_date", False))
        self.limit_creation_date.toggled.connect(self.toggle_creation_date_limits)
        self.form_layout.addRow(self.limit_creation_date)

        self.creation_date_from = QDateEdit()
        self.creation_date_from.setMaximumWidth(200)
        self.creation_date_from.setCalendarPopup(True)
        self.creation_date_from.setDate(self.options.get("creation_date_from"))
        self.creation_date_from.setEnabled(self.limit_creation_date.isChecked())
        self.form_layout.addRow("From:", self.creation_date_from)

        self.creation_date_to = QDateEdit()
        self.creation_date_to.setMaximumWidth(200)
        self.creation_date_to.setCalendarPopup(True)
        self.creation_date_to.setDate(self.options.get("creation_date_to"))
        self.creation_date_to.setEnabled(self.limit_creation_date.isChecked())
        self.form_layout.addRow("To:", self.creation_date_to)

        self.limit_changing_date = QCheckBox("Limit Changing Date")
        self.limit_changing_date.setChecked(self.options.get("limit_changing_date", False))
        self.limit_changing_date.toggled.connect(self.toggle_changing_date_limits)
        self.form_layout.addRow(self.limit_changing_date)

        self.changing_date_from = QDateEdit()
        self.changing_date_from.setMaximumWidth(200)
        self.changing_date_from.setCalendarPopup(True)
        self.changing_date_from.setDate(self.options.get("changing_date_from"))
        self.changing_date_from.setEnabled(self.limit_changing_date.isChecked())
        self.form_layout.addRow("From:", self.changing_date_from)

        self.changing_date_to = QDateEdit()
        self.changing_date_to.setMaximumWidth(200)
        self.changing_date_to.setCalendarPopup(True)
        self.changing_date_to.setDate(self.options.get("changing_date_to"))
        self.changing_date_to.setEnabled(self.limit_changing_date.isChecked())
        self.form_layout.addRow("To:", self.changing_date_to)

    def toggle_size_limits(self, checked):
        self.size_value.setEnabled(checked)
        self.size_unit.setEnabled(checked)

    def toggle_creation_date_limits(self, checked):
        self.creation_date_from.setEnabled(checked)
        self.creation_date_to.setEnabled(checked)

    def toggle_changing_date_limits(self, checked):
        self.changing_date_from.setEnabled(checked)
        self.changing_date_to.setEnabled(checked)

    def create_file_format_options(self):
        self.file_format_checkboxes = {}
        file_formats = self.options.get("file_formats", {})
        for format_name, checked in file_formats.items():
            checkbox = QCheckBox(format_name.upper())
            checkbox.setChecked(checked)
            self.file_format_checkboxes[format_name] = checkbox
            self.form_layout.addRow(checkbox)

    def create_similarity_threshold_options(self):
        self.similarity_threshold_slider = QSlider(Qt.Horizontal)
        self.similarity_threshold_slider.setMaximumWidth(200)
        self.similarity_threshold_slider.setRange(0, 100)
        self.similarity_threshold_slider.setValue(self.options.get("similarity_threshold"))
        self.similarity_threshold_slider.setTickPosition(QSlider.TicksBelow)
        self.similarity_threshold_slider.setTickInterval(10)

        self.similarity_threshold_label = QLabel(f"Similarity: {self.similarity_threshold_slider.value()}%")
        self.similarity_threshold_slider.valueChanged.connect(self.update_similarity_threshold_label)
        self.form_layout.addRow(self.similarity_threshold_label, self.similarity_threshold_slider)

    def create_algorithm_specific_options(self):
        self.comparison_size_spinbox = QSpinBox()
        self.comparison_size_spinbox.setMaximumWidth(200)
        self.comparison_size_spinbox.setRange(1, 100)
        self.comparison_size_spinbox.setValue(self.options.get("comparison_size", 16))
        self.form_layout.addRow("Comparison Size:", self.comparison_size_spinbox)

        self.quick_search_checkbox = QCheckBox("Quick Search")
        self.quick_search_checkbox.setChecked(self.options.get("quick_search", False))
        self.form_layout.addRow(self.quick_search_checkbox)

        self.update_algorithm_specific_options(self.algorithm_combo.currentText())

    def create_max_duplicates_option(self):
        self.max_duplicates_spinbox = QSpinBox()
        self.max_duplicates_spinbox.setMaximumWidth(200)
        self.max_duplicates_spinbox.setRange(1, 100000)
        self.max_duplicates_spinbox.setValue(self.options.get("max_duplicates", 1000))
        self.form_layout.addRow("Max duplicates:", self.max_duplicates_spinbox)

    def create_modified_options(self):
        self.modified_checkboxes = {}
        modified = self.options.get("modified", {})
        for mod_name, checked in modified.items():
            checkbox = QCheckBox(mod_name)
            checkbox.setChecked(checked)
            self.modified_checkboxes[mod_name] = checkbox
            self.form_layout.addRow(checkbox)

    def update_algorithm_specific_options(self, algorithm):
        is_b_or_m_hash = algorithm not in ["bHash", "mHash"]
        self.quick_search_checkbox.setDisabled(is_b_or_m_hash)
        self.comparison_size_spinbox.setDisabled(is_b_or_m_hash)

    def update_similarity_threshold_label(self, value):
        self.similarity_threshold_label.setText(f"Similarity: {value}%")

    def get_options(self):
        file_formats = {format_name: checkbox.isChecked() for format_name, checkbox in
                        self.file_format_checkboxes.items()}
        search_by = {
            "Name": self.search_by_name.isChecked(),
            "Format": self.search_by_format.isChecked(),
            "Size": self.search_by_size.isChecked()
        }
        modified = {mod_name: checkbox.isChecked() for mod_name, checkbox in
                    self.modified_checkboxes.items()}
        return {
            "recursive_search": self.folder_combo.currentIndex() == 0,
            "search_by": search_by,
            "algorithm": self.algorithm_combo.currentText(),
            "limit_size": self.limit_size.isChecked(),
            "limit_creation_date": self.limit_creation_date.isChecked(),
            "creation_date_from": self.creation_date_from.date(),
            "creation_date_to": self.creation_date_to.date(),
            "limit_changing_date": self.limit_changing_date.isChecked(),
            "changing_date_from": self.changing_date_from.date(),
            "changing_date_to": self.changing_date_to.date(),
            "file_formats": file_formats,
            "similarity_threshold": self.similarity_threshold_slider.value(),
            "quick_search": self.quick_search_checkbox.isChecked(),
            "comparison_size": self.comparison_size_spinbox.value(),
            "max_duplicates": self.max_duplicates_spinbox.value(),
            "modified": modified,
            "search_specific_file": self.specific_file_checkbox.isChecked(),
            "specific_file_path": self.options.get("specific_file_path"),
            "size_value": self.size_value.text(),
            "size_unit": self.size_unit.currentText()
        }

    def add_separator(self, text):
        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.form_layout.addItem(spacer)
        self.form_layout.addRow(QLabel(text))
        self.form_layout.addRow(separator)


def open_options_dialog(main_window):
    dialog = OptionsDialog(main_window.options_manager.options)
    if dialog.exec_() == QDialog.Accepted:
        main_window.options_manager.options = dialog.get_options()
        update_options(main_window)
        print(main_window.options_manager.options)


def update_options(main_window):
    main_window.recursiveSearchAction.setChecked(main_window.options_manager.options["recursive_search"])
    main_window.currentSearchAction.setChecked(not main_window.options_manager.options["recursive_search"])

    search_by = main_window.options_manager.options.get("search_by", {})
    main_window.byNameAction.setChecked(search_by.get("Name", False))
    main_window.byFormatAction.setChecked(search_by.get("Format", False))
    main_window.bySizeAction.setChecked(search_by.get("Size", False))

    algorithm = main_window.options_manager.options.get("algorithm")
    main_window.algorithm_actions[algorithm].setChecked(True)

    search_specific_file = main_window.options_manager.options.get("search_specific_file")
    main_window.search_specific_file_checkbox.setChecked(search_specific_file)
