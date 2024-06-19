from PyQt5.QtWidgets import QFileDialog, QMessageBox
from gui.undo_commands import AddFolderCommand, ClearSearchListCommand, RemoveSelFolderCommand, \
    AddExcludedFolderCommand, ClearExcludedSearchListCommand, RemoveExcludedSelFolderCommand
from duplicates_finder.duplicatesFinder import DuplicatesFinder


def browse_folder(self):
    folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
    if folder_path and folder_path not in self.search_list:
        command = AddFolderCommand(folder_path, self.dnd_space, self.search_list)
        self.undo_stack.push(command)


def browse_excluded_folder(self):
    folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
    if folder_path and folder_path not in self.excluded_list:
        command = AddExcludedFolderCommand(folder_path, self.excluded_dnd_space, self.excluded_list)
        self.undo_stack.push(command)


def start_search(self):
    if not self.search_list:
        QMessageBox.warning(self, "Empty Folder Path", "Please select a folder for search.")
        return

    self.file_searcher.file_formats = [".png", ".jpg", ".jpeg"]
    # img params
    images = self.file_searcher.search()
    # method params
    dupl_finder = DuplicatesFinder(self.method)
    dupl_finder.files = images[0]
    # finder params
    dupl_finder.find()
    # self.display_results(dups)


def display_results(self, duplicates):
    self.result_listbox.clear()
    if duplicates:
        for duplicate in duplicates:
            self.result_listbox.addItem(f"{duplicate[0]} and {duplicate[1]}")
    else:
        self.result_listbox.addItem("No duplicate images found.")


def remove_sel_folder(self):
    sel_item = self.dnd_space.currentItem()
    if sel_item:
        command = RemoveSelFolderCommand(sel_item.text(), self.dnd_space, self.search_list)
        self.undo_stack.push(command)


def remove_sel_excluded_folder(self):
    sel_item = self.excluded_dnd_space.currentItem()
    if sel_item:
        command = RemoveExcludedSelFolderCommand(sel_item.text(), self.excluded_dnd_space, self.excluded_list)
        self.undo_stack.push(command)


def clear_search_list(self):
    if self.search_list:
        command = ClearSearchListCommand(self.dnd_space, self.search_list)
        self.undo_stack.push(command)


def clear_excluded_list(self):
    if self.excluded_list:
        command = ClearExcludedSearchListCommand(self.excluded_dnd_space, self.excluded_list)
        self.undo_stack.push(command)
