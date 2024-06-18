from PyQt5.QtWidgets import QMenu, QToolBar, QToolButton
from PyQt5.QtGui import QIcon


def create_toolbar(main_window):
    toolbar = QToolBar("Tools", main_window)
    toolbar.setFloatable(False)
    # Edit
    toolbar.addAction(main_window.addFolderAction)
    toolbar.addAction(main_window.removeSelAction)
    toolbar.addSeparator()
    # Folders
    toolbar.addAction(main_window.recursiveSearchAction)
    toolbar.addAction(main_window.currentSearchAction)
    toolbar.addSeparator()
    # Search by
    search_by_menu = QMenu(main_window)
    search_by_menu.addActions([main_window.byContentAction, main_window.byNameAction, main_window.bySizeAction])
    search_by_tool = QToolButton(main_window)
    search_by_tool.setToolTip("Search by")
    search_by_tool.setIcon(QIcon("static/search_by.png"))
    search_by_tool.setPopupMode(QToolButton.InstantPopup)
    search_by_tool.setMenu(search_by_menu)
    toolbar.addWidget(search_by_tool)
    toolbar.addSeparator()
    # Algorithms
    algorithms_menu = QMenu(main_window)
    algorithms_menu.addActions([main_window.aHashAction, main_window.pHashAction, main_window.orbAction])
    algorithms_tool = QToolButton(main_window)
    algorithms_tool.setToolTip("Algorithm")
    algorithms_tool.setIcon(QIcon("static/algorithm.png"))
    algorithms_tool.setPopupMode(QToolButton.InstantPopup)
    algorithms_tool.setMenu(algorithms_menu)
    toolbar.addWidget(algorithms_tool)

    return toolbar
