from PyQt5.QtWidgets import QFileDialog
from gui.undo_commands import AddFolderCommand, ClearSearchListCommand, RemoveSelFolderCommand, \
    AddExcludedFolderCommand, ClearExcludedSearchListCommand, RemoveExcludedSelFolderCommand


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
