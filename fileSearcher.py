from search import get_images_in_folder
from search import get_images_in_folder_and_subfolders

class FileSearcher:
    def __init__(self):
        self.searchInSubfolders = False
        self.foldersForSearch = []
        self.fileFormats= []
    
    def search(self):
        if self.searchInSubfolders:
            search_method = get_images_in_folder_and_subfolders
        else:
            search_method = get_images_in_folder
            
        formats = self.fileFormats
        files = []
        for folder in self.foldersForSearch:
            new_files = search_method(folder, formats)
            files = files + new_files
        return files, len(files)

# Example of work    
file_searcher = FileSearcher()
file_searcher.searchInSubfolders = True
file_searcher.foldersForSearch = ['images', 'result']
file_searcher.fileFormats = ['.png', '.jpg', '.jpeg']

images, count = file_searcher.search()
print(images, count)

