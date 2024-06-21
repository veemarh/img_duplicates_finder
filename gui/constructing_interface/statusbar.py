from PyQt5.QtWidgets import QStatusBar, QLabel


def create_status_bar(main_window):
    statusbar = QStatusBar(main_window)
    constant_message = "Constant"
    constant_message_label = QLabel(f"{constant_message}")
    statusbar.addPermanentWidget(constant_message_label)

    return statusbar
