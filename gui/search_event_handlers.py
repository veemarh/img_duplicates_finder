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
    # get array of file formats
    formats = []
    formats_dict = self.options_manager.options["file_formats"]
    for f in formats_dict:
        if formats_dict[f]:
            formats.append(f)
    self.file_searcher.file_formats = formats
    # img params
    images = self.file_searcher.search()
    # method params
    dupl_finder = DuplicatesFinder(self.method)
    dupl_finder.files = images[0]
    # finder params
    dups, dups_num = dupl_finder.find()
    display_results(self, dups, dups_num)


def display_results(self, duplicates, num):
    self.result_listbox.clear()
    self.result_listbox.addItem(f"{num} duplicates found")
    for i in duplicates:
        self.result_listbox.addItem(f"{i}:")
        for duplicate in duplicates[i]:
            self.result_listbox.addItem(f"- {duplicate}")
        self.result_listbox.addItem("")
        


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
