from PyQt5.QtWidgets import QMenuBar


def create_menubar(main_window):
    menubar = QMenuBar(main_window)
    # File
    file_menu = menubar.addMenu("&File")
    open_recent_menu = file_menu.addMenu("&Open Recent")
    file_menu.addAction(main_window.exitAction)
    # Edit
    edit_menu = menubar.addMenu("&Edit")
    edit_menu.addAction(main_window.undoAction)
    edit_menu.addAction(main_window.redoAction)
    edit_menu.addSeparator()
    edit_menu.addAction(main_window.addFolderAction)
    edit_menu.addAction(main_window.removeSelAction)
    edit_menu.addAction(main_window.clearFoldersAction)
    edit_menu.addSeparator()
    edit_menu.addAction(main_window.addExcludedFolderAction)
    edit_menu.addAction(main_window.removeSelExcludedAction)
    edit_menu.addAction(main_window.clearExcludedAction)
    # *** Options
    options_menu = menubar.addMenu("&Options")
    # Folders
    folders_menu = options_menu.addMenu("&Folders")
    folders_menu.addAction(main_window.recursiveSearchAction)
    folders_menu.addAction(main_window.currentSearchAction)
    # Search by
    search_by_menu = options_menu.addMenu("&Search by")
    search_by_menu.addActions([main_window.byNameAction, main_window.byFormatAction, main_window.bySizeAction])
    # Algorithms
    algorithms_menu = options_menu.addMenu("&Algorithm")
    for action in main_window.algorithm_actions.values():
        algorithms_menu.addAction(action)
    # More
    more_menu = options_menu.addAction(main_window.openSettingsAction)
    # Help
    help_menu = menubar.addMenu("&Help")
    help_menu.addAction(main_window.helpContentAction)
    help_menu.addAction(main_window.aboutAction)

    return menubar
