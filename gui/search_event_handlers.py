import os
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from duplicates_finder.duplicatesFinder import DuplicatesFinder
from gui.constructing_interface.progressWindow import ProgressWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import Qt
from gui.custom_exceptions import FolderNotSpecifiedError
from gui.constructing_interface.duplicateDetailsDialog import DuplicateDetailsDialog


class FindDuplicatesThread(QThread):
    progress = pyqtSignal(int, int, int)
    found_duplicates = pyqtSignal(dict, int)
    finished = pyqtSignal(dict, int)

    def __init__(self, dupl_finder):
        super().__init__()
        self.dupl_finder = dupl_finder
        self.dupl_finder.set_progress_callback(self.progress.emit)
        self.dupl_finder.set_found_duplicates_callback(self.found_duplicates.emit)

    def run(self):
        duplicates, count = self.dupl_finder.find()
        self.finished.emit(duplicates, count)

    def stop(self):
        self.dupl_finder.stop()


def start_search(self):
    if not self.search_list:
        raise FolderNotSpecifiedError("No folders are selected for search.")

    options = self.options_manager.options
    # turn on/off recursive search
    self.file_searcher.search_in_subfolders = options["recursive_search"]
    # exclude folders
    self.file_searcher.excluded_folders = self.excluded_list
    # get array of file formats
    formats = []
    formats_dict = options["file_formats"]
    for f in formats_dict:
        if formats_dict[f]:
            formats.append(f)
    self.file_searcher.file_formats = formats
    # image limits
    if options["limit_size"]:
        min_val = translate_in_bytes(int(options["size_value_from"]), options["size_unit_from"])
        max_val = translate_in_bytes(int(options["size_value_to"]), options["size_unit_to"])
        self.file_searcher.set_limit_file_size(min_val, max_val)
    else:
        self.file_searcher.set_limit_file_size(None, None)

    if options["limit_creation_date"]:
        min_val = options["creation_date_from"]
        max_val = options["creation_date_to"]
        self.file_searcher.set_limit_file_creating_time(min_val, max_val)
    else:
        self.file_searcher.set_limit_file_creating_time(None, None)

    if options["limit_changing_date"]:
        min_val = options["changing_date_from"]
        max_val = options["changing_date_to"]
        self.file_searcher.set_limit_file_modifying_time(min_val, max_val)
    else:
        self.file_searcher.set_limit_file_modifying_time(None, None)

    # search images
    images = self.file_searcher.search()
    # comparison params
    self.method.name = options["algorithm"]
    self.method.similarity = options["similarity_threshold"]

    self.method.bhash_quick = options["quick_search"]
    if options["comparison_size"]:
        self.method.comparison_size = int(options["comparison_size"])
    else:
        self.method.comparison_size = 16

    dupl_finder = DuplicatesFinder(self.method)
    dupl_finder.files = images[0]

    if options["search_specific_file"]:
        if os.path.isabs(options["specific_file_path"]) and os.path.isfile(options["specific_file_path"]):
            dupl_finder.specified_file = options["specific_file_path"]
        else:
            raise FileNotFoundError(f"File not found: {options['specific_file_path']}.")
    else:
        dupl_finder.specified_file = None

    if options["select_uploading_folder"]:
        if os.path.isabs(options["uploading_folder_path"]) and os.path.isdir(options["uploading_folder_path"]):
            dupl_finder.folder_for_move = options["uploading_folder_path"]
        else:
            raise NotADirectoryError(f"Folder not found: {options['uploading_folder_path']}.")
    else:
        dupl_finder.folder_for_move = None

    dupl_finder.max_num_duplicates = options["max_duplicates"]
    # same properties
    same_props = options["search_by"]  # {"Name": bool, "Format": bool, "Size": bool}
    dupl_finder.set_identical_properties(same_props["Name"], same_props["Format"], same_props["Size"])
    # modifications
    mod_props = options["modified"]
    dupl_finder.set_modified_properties(
        mod_props["rotated 90 deg to the right"],
        mod_props["rotated 180 deg"],
        mod_props["rotated 90 deg to the left"],
        mod_props["reflected horizontally"],
        mod_props["reflected vertically"],
        mod_props["reflected horizontally and rotated 90 deg to the right"],
        mod_props["reflected vertically and rotated 90 deg to the right"]
    )

    # Creating and starting the thread
    self.result_table.clearContents()
    self.result_table.setRowCount(1)
    self.progress_window = ProgressWindow(self)
    self.progress_window.setWindowModality(Qt.ApplicationModal)
    disable_sorting(self)
    self.progress_window.show()

    self.thread = FindDuplicatesThread(dupl_finder)
    self.thread.progress.connect(self.progress_window.update_progress)
    self.thread.found_duplicates.connect(
        lambda duplicates, duplicates_count: update_real_time_duplicates(self, duplicates, duplicates_count))
    self.thread.finished.connect(
        lambda duplicates, duplicates_count: on_search_finished(self, duplicates, duplicates_count))
    self.thread.finished.connect(self.thread.deleteLater)
    self.progress_window.thread = self.thread
    self.thread.start()


def update_real_time_duplicates(self, duplicates, duplicates_count):
    display_results(self, duplicates, duplicates_count)


def on_search_finished(self, duplicates, duplicates_count):
    self.progress_window.close()
    QMessageBox.information(self, "Success",
                            "<h3>Search completed</h3>"
                            f"{duplicates_count} duplicates found for {len(duplicates)} images.")
    enable_sorting(self)


def display_results(self, duplicates, num):
    self.result_table.setRowCount(0)
    row = 0
    for one_file in duplicates:
        file_name = os.path.basename(one_file)
        creation_date = datetime.fromtimestamp(os.path.getctime(one_file)).strftime('%d/%m/%y %H:%M:%S')
        duplicate_count = len(duplicates[one_file])

        self.result_table.insertRow(row)
        self.result_table.setItem(row, 0, QTableWidgetItem(file_name))
        self.result_table.setItem(row, 1, QTableWidgetItem(creation_date))
        self.result_table.setItem(row, 2, QTableWidgetItem(str(duplicate_count)))
        self.result_table.setItem(row, 3, QTableWidgetItem(one_file))
        row += 1

    self.duplicates_dict = duplicates


def show_duplicate_details(self, row):
    file_path = self.result_table.item(row, 3).text()
    duplicates = self.duplicates_dict.get(file_path, [])
    dialog = DuplicateDetailsDialog(file_path, duplicates, self)
    dialog.exec_()


def enable_sorting(self):
    self.result_table.setSortingEnabled(True)


def disable_sorting(self):
    self.result_table.setSortingEnabled(False)


def translate_in_bytes(val: int, unit: str):
    match unit:
        case "bytes":
            res = val
        case "kb":
            res = val * 1024
        case "mb":
            res = val * 1048576
        case _:
            raise Exception("Invalid unit value")
    return res
