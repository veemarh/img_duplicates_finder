from PyQt5.QtWidgets import QUndoCommand


class AddFolderCommand(QUndoCommand):
    def __init__(self, file_path, list_widget, search_list):
        super().__init__()
        self.file_path = file_path
        self.list_widget = list_widget
        self.search_list = search_list

    def redo(self):
        self.search_list.append(self.file_path)
        self.list_widget.addItem(self.file_path)

    def undo(self):
        if self.file_path in self.search_list:
            self.search_list.remove(self.file_path)
            self.list_widget.takeItem(self.list_widget.count() - 1)


class ClearSearchListCommand(QUndoCommand):
    def __init__(self, list_widget, search_list):
        super().__init__()
        self.list_widget = list_widget
        self.search_list = search_list
        self.removed_items = list(search_list)

    def redo(self):
        self.search_list.clear()
        self.list_widget.clear()

    def undo(self):
        for item in self.removed_items:
            self.search_list.append(item)
            self.list_widget.addItem(item)


class RemoveSelFolderCommand(QUndoCommand):
    def __init__(self, file_path, list_widget, search_list):
        super().__init__()
        self.list_widget = list_widget
        self.search_list = search_list
        self.file_path = file_path
        self.row_item = self.search_list.index(self.file_path)

    def redo(self):
        self.search_list.pop(self.row_item)
        self.list_widget.takeItem(self.row_item)

    def undo(self):
        if self.file_path not in self.search_list:
            self.search_list.insert(self.row_item, self.file_path)
            self.list_widget.insertItem(self.row_item, self.file_path)


class AddExcludedFolderCommand(QUndoCommand):
    def __init__(self, file_path, list_widget, excluded_list):
        super().__init__()
        self.file_path = file_path
        self.list_widget = list_widget
        self.excluded_list = excluded_list

    def redo(self):
        self.excluded_list.append(self.file_path)
        self.list_widget.addItem(self.file_path)

    def undo(self):
        if self.file_path in self.excluded_list:
            self.excluded_list.remove(self.file_path)
            self.list_widget.takeItem(self.list_widget.count() - 1)


class ClearExcludedSearchListCommand(QUndoCommand):
    def __init__(self, list_widget, excluded_list):
        super().__init__()
        self.list_widget = list_widget
        self.excluded_list = excluded_list
        self.removed_items = list(excluded_list)

    def redo(self):
        self.excluded_list.clear()
        self.list_widget.clear()

    def undo(self):
        for item in self.removed_items:
            self.excluded_list.append(item)
            self.list_widget.addItem(item)


class RemoveExcludedSelFolderCommand(QUndoCommand):
    def __init__(self, file_path, list_widget, excluded_list):
        super().__init__()
        self.list_widget = list_widget
        self.excluded_list = excluded_list
        self.file_path = file_path
        self.row_item = self.excluded_list.index(self.file_path)

    def redo(self):
        self.excluded_list.pop(self.row_item)
        self.list_widget.takeItem(self.row_item)

    def undo(self):
        if self.file_path not in self.excluded_list:
            self.excluded_list.insert(self.row_item, self.file_path)
            self.list_widget.insertItem(self.row_item, self.file_path)
