from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QFileInfo
from gui.undo_commands import AddFolderCommand, AddExcludedFolderCommand


def dragEnterEvent(event):
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

    excluded_dnd_rect = self.excluded_dnd_space.rect()
    excluded_mouse_pos = self.excluded_dnd_space.mapFromGlobal(QCursor.pos())
    if excluded_dnd_rect.contains(excluded_mouse_pos):
        paths = set([u.toLocalFile() for u in event.mimeData().urls()])
        for path in paths:
            if QFileInfo(path).isDir() and path not in self.excluded_list:
                command = AddExcludedFolderCommand(path, self.excluded_dnd_space, self.excluded_list)
                self.undo_stack.push(command)
