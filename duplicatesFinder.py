import os
import time
from pathlib import Path
from find_funcs import *

# arg 'bhash_quick' only for bhash - parameter 'Fast' = True, 'Precise' = False
# arg 'compare_size' for bhash and mhash - parameter 'Comparison area' (bhash:128x128, 256x256, 512x512; mhash: 8x8, 16x16 )  
class DuplicatesFinder:
    def __init__(self):
        self.files = []
        self.file_is_specified = False #
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
        start = time.monotonic()
        paths_images = self.files
        method = self.method
        similarity = self.similarity
        duplicates_folder = self.folder_for_move
        hash_size = self.hash_size
        size = self.compare_size
        
        match method:
            case 'ORB':
                get_data = get_data_orb
            case _:
                get_data = get_data_hash
    
        check_i = 0
        curr_i = 1
        duplicate_count = 0

        while check_i < len(paths_images):
            if paths_images[check_i] is not None:
                path_checked_img = paths_images[check_i]
                checked_data = get_data(path_checked_img, method, hash_size, self.bhash_quick, size)
                    
            while curr_i < len(paths_images):
                if (check_i != curr_i) and (paths_images[curr_i] is not None):
                    path_curr_img = paths_images[curr_i]
                    
                    if self.require_identical_properties:
                        if not check_identical_properties(path_checked_img, path_curr_img, self.identical_properties):
                            curr_i += 1
                            continue
                    
                    curr_data = get_data(path_curr_img, method, hash_size, self.bhash_quick, size)
                    
                    # find the percentage difference
                    match method:
                        case 'ORB':
                            diff = similarity - get_orb_similarity(checked_data, curr_data)
                        case 'MD5' | 'SHA-1 (160-bit)' | 'SHA-2 (256-bit)' | 'SHA-2 (384-bit)' | 'SHA-2 (512-bit)':
                            diff = 0 if checked_data == curr_data else 100
                        case _:
                            diff = get_difference(checked_data, curr_data, self.hash_size)

                    if diff <= (100 - similarity):
                        print(f"{path_checked_img} - {path_curr_img}")
                        name_curr_img = os.path.basename(path_curr_img)
                        if duplicates_folder:
                            Path(path_curr_img).rename(f"{duplicates_folder}/{name_curr_img}")
                        del paths_images[curr_i]
                        duplicate_count += 1
                    else:
                        curr_i += 1
                        
            check_i += 1
            curr_i = check_i + 1
            
        print(duplicate_count, 'duplicates found')
        print(f'Script running time: {time.monotonic() - start}')
    