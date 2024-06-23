import os
import time
from copy import copy
from pathlib import Path
from duplicates_finder.find_funcs import *
from algorithms.orb import get_orb_similarity
from duplicates_finder.comparisonMethod import ComparisonMethod
from duplicates_finder.comparisonObject import ComparisonObject

# var 'files': array of strings - file paths
# var 'specified_file': str
# var 'folder_for_move': str
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
        self.folder_for_move = None
        self.max_num_duplicates = 1000
        self.__require_identical_properties = False
        self.__identical_properties = {'name': False, 'format': False, 'size': False}
        self.__search_modified_images = False
        self.__modified_properties = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False}
        self.__comparison_method = comparison_method

    def find(self):
        start = time.monotonic()

        duplicates = {}
        file_is_specified = False
        check_i = 0

        if self.specified_file:
            file_is_specified = True
            path_check_img = self.specified_file
            curr_i = 0
        else:
            curr_i = 1

        paths_images = self.files
        comparison_method = self.__comparison_method

        duplicate_count = 0

        while check_i < len(paths_images):
            if not file_is_specified:
                path_check_img = paths_images[check_i]

            if path_check_img is not None:
                checked_obj = ComparisonObject(path_check_img, comparison_method)
            else:
                check_i += 1
                continue

            while curr_i < len(paths_images):
                path_curr_img = paths_images[curr_i]

                if (path_check_img == path_curr_img) or (path_curr_img is None):
                    curr_i += 1
                    continue

                if self.__require_identical_properties:
                    if not check_identical_properties(checked_obj.file_path, path_curr_img,
                                                      self.__identical_properties):
                        curr_i += 1
                        continue

                curr_obj = ComparisonObject(path_curr_img, comparison_method)

                if self.__is_duplicates(checked_obj.comparison_data, curr_obj.comparison_data) or \
                        (self.__search_modified_images and self.__check_modified(checked_obj, curr_obj)):
                    # add duplicates
                    if path_check_img in duplicates:
                        duplicates[path_check_img].append(path_curr_img)
                    else:
                        duplicates[path_check_img] = [path_curr_img]
                        
                    self.__action_with_duplicates(checked_obj, curr_obj)
                    if file_is_specified:
                        curr_i += 1
                    else:
                        del paths_images[curr_i]
                    duplicate_count += 1
                    if duplicate_count >= self.max_num_duplicates: break
                else:
                    curr_i += 1

            if file_is_specified or duplicate_count >= self.max_num_duplicates: break
            check_i += 1
            curr_i = check_i + 1

        print(f'Script running time: {time.monotonic() - start}')
        return duplicates, duplicate_count

    def set_identical_properties(self, name: bool = False, format: bool = False, size: bool = False):
        self.__require_identical_properties = True
        self.__identical_properties['name'] = name
        self.__identical_properties['format'] = format
        self.__identical_properties['size'] = size

    def set_modified_properties(self, _1: bool = False, _2: bool = False, \
                                _3: bool = False, _4: bool = False, _5: bool = False, \
                                _6: bool = False, _7: bool = False):
        # 1 - rotated 90 deg to the right,
        # 2 - rotated 180 deg,
        # 3 - rotated 90 deg to the left, 
        # 4 - reflected horizontally,
        # 5 - reflected vertically,
        # 6 - reflected horizontally and rotated 90 degrees to the right,
        # 7 - reflected vertically and rotated 90 degrees to the right
        self.__search_modified_images = True
        self.__modified_properties[1] = _1
        self.__modified_properties[2] = _2
        self.__modified_properties[3] = _3
        self.__modified_properties[4] = _4
        self.__modified_properties[5] = _5
        self.__modified_properties[6] = _6
        self.__modified_properties[7] = _7

    def __find_percentage_difference(self, data1, data2):
        method = self.__comparison_method
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
        return diff <= (100 - self.__comparison_method.similarity)

    def __check_modified(self, obj: ComparisonObject, obj_to_mod: ComparisonObject):
        properties = self.__modified_properties
        img_to_mod = copy(obj_to_mod.object)
        for key in properties:
            if properties[key]:
                if self.__check_property(obj, img_to_mod, key):
                    return True
        return False

    def __check_property(self, obj: ComparisonObject, img_to_mod, property: int):
        method = self.__comparison_method
        modified_img = modify_img(img_to_mod, property)
        modified_comparison_data = get_data_obj(modified_img, method)
        if self.__is_duplicates(obj.comparison_data, modified_comparison_data):
            return True
        return False

    def __action_with_duplicates(self, checked_obj: ComparisonObject, curr_obj: ComparisonObject):
        path_curr_img = curr_obj.file_path
        # print(f"{checked_obj.file_path} - {path_curr_img}")
        name_curr_img = os.path.basename(path_curr_img)
        if self.folder_for_move:
            Path(path_curr_img).rename(f"{self.folder_for_move}/{name_curr_img}")
