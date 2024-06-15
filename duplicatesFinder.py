import os
import time
from accessify import protected
from pathlib import Path
from find_funcs import *

# arg 'bhash_quick' only for bhash - parameter 'Fast' = True, 'Precise' = False
# arg 'compare_size' for bhash and mhash - parameter 'Comparison area' (bhash:128x128, 256x256, 512x512; mhash: 8x8, 16x16 )  
class DuplicatesFinder:
    def __init__(self):
        self.files = []
        self.specified_file = None
        self.require_identical_properties =  False
        self.identical_properties = {'name': False, 'format': False, 'size': False}
        self.search_modified_images = False # rotated 90 deg to the right, rotated 180 deg, rotated 90 deg to the left, reflected horizontally, reflected vertically
        self.method = 'aHash'
        self.hash_size = 16
        self.bhash_quick = False
        self.compare_size = 16
        self.similarity = 100
        self.folder_for_move = None
        
    def find(self):
        if self.specified_file:
            return self.__find(self.specified_file)
        start = time.monotonic()
        paths_images = self.files
        
        get_data = func_get_data(self.method)
        check_i = 0
        curr_i = 1
        duplicate_count = 0

        while check_i < len(paths_images):
            if paths_images[check_i] is not None:
                path_checked_img = paths_images[check_i]
                checked_data = get_data(path_checked_img, self.method, self.hash_size, self.bhash_quick, self.compare_size)
                    
            while curr_i < len(paths_images):
                path_curr_img = paths_images[curr_i]
                if (check_i != curr_i) and (path_curr_img is not None):
                    if self.require_identical_properties:
                        if not check_identical_properties(path_checked_img, path_curr_img, self.identical_properties):
                            curr_i += 1
                            continue
                    
                    curr_data = get_data(path_curr_img, self.method, self.hash_size, self.bhash_quick, self.compare_size)
                    
                    # find the percentage difference
                    diff = find_percentage_difference(checked_data, curr_data, self.method, self.similarity, self.hash_size)

                    if diff <= (100 - self.similarity):
                        print(f"{path_checked_img} - {path_curr_img}")
                        name_curr_img = os.path.basename(path_curr_img)
                        if self.folder_for_move:
                            Path(path_curr_img).rename(f"{self.folder_for_move}/{name_curr_img}")
                        del paths_images[curr_i]
                        duplicate_count += 1
                    else:
                        curr_i += 1
                        
            check_i += 1
            curr_i = check_i + 1
            
        print(duplicate_count, 'duplicates found')
        print(f'Script running time: {time.monotonic() - start}')
    
    @protected     
    def __find(self, specified_file):
        start = time.monotonic()
        paths_images = self.files
        
        get_data = func_get_data(self.method)
        duplicate_count = 0

        if specified_file is not None:
            checked_data = get_data(specified_file, self.method, self.hash_size, self.bhash_quick, self.compare_size)
                
        for curr_img in paths_images:
            if (specified_file != curr_img) and (curr_img is not None):
                if self.require_identical_properties:
                    if not check_identical_properties(specified_file, curr_img, self.identical_properties):
                        continue
                
                curr_data = get_data(curr_img, self.method, self.hash_size, self.bhash_quick, self.compare_size)
                
                # find the percentage difference
                diff = find_percentage_difference(checked_data, curr_data, self.method, self.similarity, self.hash_size)
                
                if diff <= (100 - self.similarity):
                    print(f"{specified_file} - {curr_img}")
                    name_curr_img = os.path.basename(curr_img)
                    if self.folder_for_move:
                        Path(curr_img).rename(f"{self.folder_for_move}/{name_curr_img}")
                    del curr_img
                    duplicate_count += 1
                                
        print(duplicate_count, 'duplicates found')
        print(f'Script running time: {time.monotonic() - start}')
        