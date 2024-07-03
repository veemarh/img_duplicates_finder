from PyQt5.QtWidgets import QAction, QActionGroup
from PyQt5.QtGui import QIcon
from gui.optionsDialog import open_options_dialog
from gui.constructing_interface.maxDuplicatesDialog import open_max_duplicates_dialog
from gui.algorithmInfoDialog import open_algorithm_info_dialog
from gui.algorithmsManager import get_algorithm_names


def create_actions(main_window):
    # File
    main_window.exitAction = QAction(QIcon("static/quit.png"), "&Quit", main_window)
    main_window.exitAction.setShortcut("Ctrl+Q")
    main_window.exitAction.setStatusTip("Quit application")
    main_window.exitAction.triggered.connect(main_window.close)
    # Edit
    main_window.undoAction = QAction(QIcon("static/undo.png"), "&Undo", main_window)
    main_window.undoAction.setShortcut("Ctrl+Z")
    main_window.undoAction.setStatusTip("Undo")
    main_window.undoAction.triggered.connect(main_window.undo_action)
    main_window.redoAction = QAction(QIcon("static/redo.png"), "&Redo", main_window)
    main_window.redoAction.setShortcut("Ctrl+Shift+Z")
    main_window.redoAction.setStatusTip("Redo")
    main_window.redoAction.triggered.connect(main_window.redo_action)
    main_window.addFolderAction = QAction(QIcon("static/add.png"), "&Add to Search List", main_window)
    main_window.addFolderAction.setShortcut("Ctrl+M")
    main_window.addFolderAction.setStatusTip("Add a new folder to search list")
    main_window.addFolderAction.triggered.connect(main_window.browse_folder)
    main_window.removeSelAction = QAction(QIcon("static/remove.png"), "&Remove from Search List", main_window)
    main_window.removeSelAction.setShortcut("Delete")
    main_window.removeSelAction.setStatusTip("Remove selected folder from search list")
    main_window.removeSelAction.triggered.connect(main_window.remove_sel_folder)
    main_window.clearFoldersAction = QAction("&Clear Search List", main_window)
    main_window.clearFoldersAction.setStatusTip("Clear search list")
    main_window.clearFoldersAction.triggered.connect(main_window.clear_search_list)
    main_window.addExcludedFolderAction = QAction("&Add Exclusion", main_window)
    main_window.addExcludedFolderAction.setStatusTip("Add a folder to excluded")
    main_window.addExcludedFolderAction.triggered.connect(main_window.browse_excluded_folder)
    main_window.removeSelExcludedAction = QAction("&Remove Exclusion", main_window)
    main_window.removeSelExcludedAction.setStatusTip("Remove selected folder from excluded")
    main_window.removeSelExcludedAction.triggered.connect(main_window.remove_sel_excluded_folder)
    main_window.clearExcludedAction = QAction("&Clear Excluded", main_window)
    main_window.clearExcludedAction.setStatusTip("Clear excluded")
    main_window.clearExcludedAction.triggered.connect(main_window.clear_excluded_list)

    # *** Search options
    # Folders
    main_window.recursiveSearchAction = QAction(QIcon("static/recursive.png"), "&Recursive Search", main_window)
    main_window.recursiveSearchAction.setStatusTip("Search in folders and their subfolders")
    main_window.recursiveSearchAction.triggered.connect(
        lambda: main_window.options_manager.set_option("recursive_search", True))
    main_window.currentSearchAction = QAction(QIcon("static/current.png"), "In the &Current Folder", main_window)
    main_window.currentSearchAction.setStatusTip("Search only in the specified folders")
    main_window.currentSearchAction.triggered.connect(
        lambda: main_window.options_manager.set_option("recursive_search", False))
    main_window.recursiveSearchAction.setCheckable(True)
    main_window.currentSearchAction.setCheckable(True)
    folder_options_group = QActionGroup(main_window)
    folder_options_group.addAction(main_window.recursiveSearchAction)
    folder_options_group.addAction(main_window.currentSearchAction)
    folder_options_group.setExclusive(True)
    main_window.recursiveSearchAction.setChecked(True)
    # Search by
    main_window.byNameAction = QAction("&Name", main_window)
    main_window.byNameAction.setStatusTip("Compare only with the same name")
    main_window.byNameAction.setCheckable(True)
    main_window.byNameAction.toggled.connect(lambda checked: update_search_by_option(main_window, "Name", checked))
    main_window.byFormatAction = QAction("&Format", main_window)
    main_window.byFormatAction.setStatusTip("Compare only with the same format")
    main_window.byFormatAction.setCheckable(True)
    main_window.byFormatAction.toggled.connect(lambda checked: update_search_by_option(main_window, "Format", checked))
    main_window.bySizeAction = QAction("&Size", main_window)
    main_window.bySizeAction.setStatusTip("Compare only with the same size")
    main_window.bySizeAction.setCheckable(True)
    main_window.bySizeAction.toggled.connect(lambda checked: update_search_by_option(main_window, "Size", checked))
    # Algorithms
    algorithms = get_algorithm_names()
    algorithms_group = QActionGroup(main_window)
    algorithms_group.setExclusive(True)
    main_window.algorithm_actions = {}
    for algorithm in algorithms:
        action = QAction(f"&{algorithm}", main_window)
        action.setStatusTip(f"Use {algorithm} comparison algorithm")
        action.triggered.connect(lambda checked, alg=algorithm: set_algorithm(main_window, alg))
        action.setCheckable(True)
        algorithms_group.addAction(action)
        main_window.algorithm_actions[algorithm] = action
    default_algorithm = main_window.options_manager.options.get("algorithm", "pHash")
    main_window.algorithm_actions[default_algorithm].setChecked(True)

    main_window.algorithmInfoAction = QAction(QIcon("static/info.png"), "&Learn more...", main_window)
    main_window.algorithmInfoAction.setStatusTip("Find out algorithms are right for you")
    main_window.algorithmInfoAction.triggered.connect(lambda: open_algorithm_info_dialog(main_window))
    # Max duplicates
    main_window.maxDuplicatesAction = QAction(QIcon("static/max_dups.png"), "&Set max duplicates...", main_window)
    main_window.maxDuplicatesAction.setStatusTip("Set max number of duplicates to show "
                                                 f"({main_window.options_manager.options['max_duplicates']})")
    main_window.maxDuplicatesAction.triggered.connect(lambda: open_max_duplicates_dialog(main_window))
    # More
    main_window.openSettingsAction = QAction(QIcon("static/settings.png"), "&More...", main_window)
    main_window.openSettingsAction.setShortcut("Ctrl+Alt+S")
    main_window.openSettingsAction.setStatusTip("Open detailed settings")
    main_window.openSettingsAction.triggered.connect(lambda: open_options_dialog(main_window))

    # Help
    main_window.aboutAction = QAction(QIcon("static/about.png"), "&About", main_window)
    main_window.aboutAction.setStatusTip("Show the Img Duplicates Finder's About box")
    main_window.aboutAction.triggered.connect(main_window.about)


def set_algorithm(main_window, algorithm):
    if main_window.options_manager.get_option("algorithm") != algorithm:
        main_window.options_manager.set_option("algorithm", algorithm)
        if algorithm == "bHash":
            main_window.options_manager.set_option("comparison_size", "256")
        elif algorithm == "mHash":
            main_window.options_manager.set_option("comparison_size", "16")
        else:
            main_window.options_manager.set_option("comparison_size", "")

        if hasattr(main_window, 'options_dialog'):
            main_window.options_dialog.update_algorithm_specific_options(algorithm)


def update_search_by_option(main_window, key, checked):
    search_by = main_window.options_manager.get_option("search_by")
    search_by[key] = checked
    main_window.options_manager.set_option("search_by", search_by)
