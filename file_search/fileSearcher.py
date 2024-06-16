from file_search.search_funcs import *

class FileSearcher:
    def __init__(self):
        self.search_in_subfolders = False
        self.folders_for_search = []
        self.file_formats= []
    
    def search(self):
        if self.search_in_subfolders:
            search_method = get_images_in_folder_and_subfolders
        else:
            search_method = get_images_in_folder
            
        formats = self.file_formats
        files = []
        for folder in self.folders_for_search:
            new_files = search_method(folder, formats)
            files = files + new_files
        return files, len(files)
