from PyQt5.QtCore import QDate


class OptionsManager:
    def __init__(self):
        self.options = {
            "recursive_search": True,
            "search_by": "Content",
            "algorithm": "aHash",
            "limit_size": False,
            "limit_creation_date": False,
            "creation_date_from": QDate.addDays(QDate.currentDate(), -7),
            "creation_date_to": QDate.currentDate(),
            "limit_changing_date": False,
            "changing_date_from": QDate.addDays(QDate.currentDate(), -7),
            "changing_date_to": QDate.currentDate(),
            "file_formats": {
                'png': True, 'jpg': True, 'jpeg': True, 'bmp': False, 'dds': False, 'dib': False,
                'eps': False, 'gif': False, 'icns': False, 'ico': False, 'pcx': False, 'ppm': False,
                'psd': False, 'tga': False, 'tif': False, 'tiff': False, 'webp': False, 'wmf': False
            },
            "similarity_threshold": 90,
            "quick_search": False,
            "comparison_size": 16
        }

    def set_option(self, option_name, value):
        if option_name in self.options:
            self.options[option_name] = value
            print(self.options)
        else:
            print(f"Option '{option_name}' does not exist")

    def get_option(self, option_name):
        return self.options.get(option_name, None)
