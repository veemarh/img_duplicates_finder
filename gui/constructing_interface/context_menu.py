from PyQt5.QtWidgets import QMenu, QAction


def create_context_menu(main_window, event):
    context_menu = QMenu(main_window.central_widget)
    separator = QAction(main_window)
    separator.setSeparator(True)
    context_menu.addAction(main_window.recursiveSearchAction)
    context_menu.addAction(main_window.currentSearchAction)
    context_menu.addAction(separator)
    # context_menu.addAction(main_window.aHashAction)
    # context_menu.addAction(main_window.pHashAction)
    # context_menu.addAction(main_window.orbAction)
    context_menu.exec(event.globalPos())
