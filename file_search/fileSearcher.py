import os
from datetime import datetime


# var 'folders_for_search': array of str - folder paths
# var 'excluded_folders': array of str - folder paths that are not included for search
# var 'file_formats': array of str - formats, e.g. '.png'
class FileSearcher:
    def __init__(self):
        self.search_in_subfolders = False
        self.folders_for_search = []
        self.excluded_folders = []
        self.file_formats = []
        self.__limit_file_creating_time = False
        self.__file_creating_time = {'min': None, 'max': None}  # datetime
        self.__limit_file_modifying_time = False
        self.__file_modifying_time = {'min': None, 'max': None}  # datetime
        self.__limit_file_size = False
        self.__file_size = {'min': None, 'max': None}  # bytes

    def search(self):
        if self.search_in_subfolders:
            search_method = self.__get_images_in_folder_and_subfolders
        else:
            search_method = self.__get_images_in_folder

        files = []
        for folder in self.folders_for_search:
            new_files = search_method(folder)
            files = files + new_files
        return files, len(files)

    def set_limit_file_creating_time(self, min: datetime, max: datetime):
        self.__limit_file_creating_time = True
        self.__file_creating_time['min'] = min
        self.__file_creating_time['max'] = max

    def set_limit_file_modifying_time(self, min: datetime, max: datetime):
        self.__limit_file_modifying_time = True
        self.__file_modifying_time['min'] = min
        self.__file_modifying_time['max'] = max

    def set_limit_file_size(self, min: int, max: int):
        self.__limit_file_size = True
        self.__file_size['min'] = min
        self.__file_size['max'] = max

    def __get_images_in_folder_and_subfolders(self, folder):
        images = []
        for root, subdirs, files in os.walk(folder):
            if root in self.excluded_folders: continue
            for file in files:
                if os.path.splitext(file)[1].lower() in self.file_formats:
                    file_path = os.path.join(root, file)
                    if not self.__check_limits(file_path): continue
                    images.append(file_path)
        return images

    def __get_images_in_folder(self, folder):
        images = []
        for file in os.listdir(folder):
            if folder in self.excluded_folders: break
            if os.path.splitext(file)[1].lower() in self.file_formats:
                file_path = os.path.join(folder, file)
                if not self.__check_limits(file_path): continue
                images.append(file_path)
        return images

    def __check_limits(self, file):
        if not self.__check_file_size(file): return False
        if not self.__check_file_creating_time(file): return False
        if not self.__check_file_modifying_time(file): return False
        return True

    def __check_file_size(self, file):
        if self.__limit_file_size:
            size = os.path.getsize(file)
            min_size = self.__file_size['min']
            max_size = self.__file_size['max']
            if (min_size and size < min_size) or (max_size and size > max_size):
                return False
        return True

    def __check_file_creating_time(self, file):
        if self.__limit_file_creating_time:
            time = datetime.fromtimestamp(os.path.getctime(file))
            min_time = self.__file_creating_time['min']
            max_time = self.__file_creating_time['max']
            if (min_time and time < min_time) or (max_time and time > max_time):
                return False
        return True

    def __check_file_modifying_time(self, file):
        if self.__limit_file_modifying_time:
            time = datetime.fromtimestamp(os.path.getmtime(file))
            min_time = self.__file_modifying_time['min']
            max_time = self.__file_modifying_time['max']
            if (min_time and time < min_time) or (max_time and time > max_time):
                return False
        return True
