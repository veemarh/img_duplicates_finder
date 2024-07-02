from PyQt5.QtWidgets import QMenu


def create_context_menu(main_window, event):
    context_menu = QMenu(main_window.central_widget)
    context_menu.addAction(main_window.openSettingsAction)
    context_menu.exec(event.globalPos())
