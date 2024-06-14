from PyQt5.QtWidgets import QUndoCommand


class AddFileCommand(QUndoCommand):
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
