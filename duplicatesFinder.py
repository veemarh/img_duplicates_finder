import os
import time
from copy import copy
from pathlib import Path
from find_funcs import *
from algorithms.orb import get_orb_similarity
from comparisonMethod import ComparisonMethod
from comparisonObject import ComparisonObject

# var 'bhash_quick' only for bhash - parameter 'Fast' = True, 'Precise' = False
# var 'compare_size' for bhash and mhash - parameter 'Comparison area' (bhash:128x128, 256x256, 512x512; mhash: 8x8, 16x16 )  
# var 'modified_images_properties' has keys:
# 1 - rotated 90 deg to the right,
# 2 - rotated 180 deg,
# 3 - rotated 90 deg to the left, 
# 4 - reflected horizontally,
# 5 - reflected vertically,
# 6 - reflected horizontally and rotated 90 degrees to the right,
# 7 - reflected vertically and rotated 90 degrees to the right
class DuplicatesFinder:
    def __init__(self, comparison_method: ComparisonMethod):
        self.files = []
        self.specified_file = None
        self.require_identical_properties =  False
        self.identical_properties = {'name': False, 'format': False, 'size': False}
        self.search_modified_images = False 
        self.modified_images_properties = {1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True}
        self.comparison_method = comparison_method
        self.folder_for_move = None
        
    def find(self):
        if self.specified_file:
            return self.__find(self.specified_file)
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

                    if self.__is_duplicates(checked_obj.comparison_data, curr_obj.comparison_data) or \
                        (self.search_modified_images and self.__check_modified(checked_obj, curr_obj)):
                        self.__action_with_duplicates(checked_obj, curr_obj)
                        del paths_images[curr_i]
                        duplicate_count += 1
                    else:
                        curr_i += 1
                        
            check_i += 1
            curr_i = check_i + 1
            
        print(duplicate_count, 'duplicates found')
        print(f'Script running time: {time.monotonic() - start}')
     
    def __find(self, specified_file: str):
        start = time.monotonic()
        paths_images = self.files
        comparison_method = self.comparison_method
        
        duplicate_count = 0

        if specified_file is not None:
            checked_obj = ComparisonObject(specified_file, comparison_method)
                    
        for curr_img in paths_images:
            if (specified_file != curr_img) and (curr_img is not None):
                if self.require_identical_properties:
                    if not check_identical_properties(checked_obj.file_path, curr_img, self.identical_properties):
                        continue
                    
                curr_obj = ComparisonObject(curr_img, comparison_method)

                if self.__is_duplicates(checked_obj.comparison_data, curr_obj.comparison_data) or \
                    (self.search_modified_images and self.__check_modified(checked_obj, curr_obj)):
                    self.__action_with_duplicates(checked_obj, curr_obj)
                    duplicate_count += 1
            
        print(duplicate_count, 'duplicates found')
        print(f'Script running time: {time.monotonic() - start}')
        
    def __find_percentage_difference(self, data1, data2):
        method = self.comparison_method
        match method.name:
            case 'ORB':
                diff = method.similarity - get_orb_similarity(data1, data2)
            case 'MD5' | 'SHA-1 (160-bit)' | 'SHA-2 (256-bit)' | 'SHA-2 (384-bit)' | 'SHA-2 (512-bit)':
                diff = 0 if data1 == data2 else 100
            case _:
                diff = get_difference(data1, data2, method.hash_size)
        return diff

    def __is_duplicates(self, data1, data2):              
        # find the percentage difference
        diff = self.__find_percentage_difference(data1, data2)
        return diff <= (100 - self.comparison_method.similarity)
        
    def __check_modified(self, obj: ComparisonObject, obj_to_mod: ComparisonObject):
        properties = self.modified_images_properties
        img_to_mod = copy(obj_to_mod.object)
        for key in properties:
            if properties[key]:
                if self.__check_property(obj, img_to_mod, key): 
                    return True        
        return False

    def __check_property(self, obj: ComparisonObject, img_to_mod, property: int):
        method = self.comparison_method
        modified_img = modify_img(img_to_mod, property)
        modified_comparison_data = get_data_obj(modified_img, method)
        if self.__is_duplicates(obj.comparison_data, modified_comparison_data): 
            return True
        return False
    
    def __action_with_duplicates(self, checked_obj: ComparisonObject, curr_obj: ComparisonObject):
        path_curr_img = curr_obj.file_path
        print(f"{checked_obj.file_path} - {path_curr_img}")
        name_curr_img = os.path.basename(path_curr_img)
        if self.folder_for_move:
            Path(path_curr_img).rename(f"{self.folder_for_move}/{name_curr_img}")
        