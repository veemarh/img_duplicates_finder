import os
import time
from accessify import protected
from pathlib import Path
from find_funcs import *
from comparisonMethod import ComparisonMethod
from comparisonObject import ComparisonObject

# var 'bhash_quick' only for bhash - parameter 'Fast' = True, 'Precise' = False
# var 'compare_size' for bhash and mhash - parameter 'Comparison area' (bhash:128x128, 256x256, 512x512; mhash: 8x8, 16x16 )  
# var 'modified_images_properties' has keys:
# 1 - rotated 90 deg to the right,
# 2 - rotated 180 deg,
# 3 - rotated 90 deg to the left, 
# 4 - reflected horizontally,
# 5 - reflected vertically
class DuplicatesFinder:
    def __init__(self, comparison_method: ComparisonMethod):
        self.files = []
        self.specified_file = None
        self.require_identical_properties =  False
        self.identical_properties = {'name': False, 'format': False, 'size': False}
        self.search_modified_images = False 
        self.modified_images_properties = {1: True, 2: True, 3: True, 4: True, 5: True}
        self.comparison_method = comparison_method
        self.folder_for_move = None
        
    def find(self):
        if self.specified_file:
            return #self.__find(self.specified_file)
        start = time.monotonic()
        paths_images = self.files
        comparison_method = self.comparison_method
        
        check_i = 0
        curr_i = 1
        duplicate_count = 0

        while check_i < len(paths_images):
            if paths_images[check_i] is not None:
                checked_obj = ComparisonObject(paths_images[check_i], comparison_method)
                    
            while curr_i < len(paths_images):
                path_curr_img = paths_images[curr_i]
                if (check_i != curr_i) and (path_curr_img is not None):
                    if self.require_identical_properties:
                        if not check_identical_properties(checked_obj.file_path, path_curr_img, self.identical_properties):
                            curr_i += 1
                            continue
                    
                    curr_obj = ComparisonObject(path_curr_img, comparison_method)

                    if is_duplicates(checked_obj.comparison_data, curr_obj.comparison_data, comparison_method):
                        print(f"{checked_obj.file_path} - {path_curr_img}")
                        name_curr_img = os.path.basename(path_curr_img)
                        if self.folder_for_move:
                            Path(path_curr_img).rename(f"{self.folder_for_move}/{name_curr_img}")
                        del paths_images[curr_i]
                        duplicate_count += 1
                    else:
                        if self.search_modified_images:
                            if check_modified(checked_obj, curr_obj, comparison_method, self.modified_images_properties):
                                print(f"{checked_obj.file_path} - {path_curr_img}")
                                name_curr_img = os.path.basename(path_curr_img)
                                if self.folder_for_move:
                                    Path(path_curr_img).rename(f"{self.folder_for_move}/{name_curr_img}")
                                del paths_images[curr_i]
                                duplicate_count += 1
                                continue
                        curr_i += 1
                        
            check_i += 1
            curr_i = check_i + 1
            
        print(duplicate_count, 'duplicates found')
        print(f'Script running time: {time.monotonic() - start}')
    
    # @protected     
    # def __find(self, specified_file):
    #     start = time.monotonic()
    #     paths_images = self.files
        
    #     get_data = func_get_data(self.method)
    #     duplicate_count = 0

    #     if specified_file is not None:
    #         checked_data = get_data(specified_file, self.method, self.hash_size, self.bhash_quick, self.compare_size)
                
    #     for curr_img in paths_images:
    #         if (specified_file != curr_img) and (curr_img is not None):
    #             if self.require_identical_properties:
    #                 if not check_identical_properties(specified_file, curr_img, self.identical_properties):
    #                     continue
                
    #             curr_data = get_data(curr_img, self.method, self.hash_size, self.bhash_quick, self.compare_size)
    #             # find the percentage difference
    #             diff = find_percentage_difference(checked_data, curr_data, self.method, self.similarity, self.hash_size)
                
    #             if diff <= (100 - self.similarity):
    #                 print(f"{specified_file} - {curr_img}")
    #                 name_curr_img = os.path.basename(curr_img)
    #                 if self.folder_for_move:
    #                     Path(curr_img).rename(f"{self.folder_for_move}/{name_curr_img}")
    #                 del curr_img
    #                 duplicate_count += 1
                                
    #     print(duplicate_count, 'duplicates found')
    #     print(f'Script running time: {time.monotonic() - start}')
        