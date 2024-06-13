import os
from algorithms.find_duplicates_hash import find_duplicates_use_hash
from algorithms.find_duplicates_orb import find_duplicates_use_orb

# arg 'quick' only for bhash - parameter 'Fast' = True, 'Precise' = False
# arg 'size' for bhash and mhash - parameter 'Comparison area' (bhash:128x128, 256x256, 512x512; mhash: 8x8, 16x16 )
def find_duplicates(paths_images, duplicates_folder, hash_size=16, perc_similarity=100, method='aHash', quick=False, size=16):
    match method:
        case 'ORB':
            find_duplicates_use_orb(paths_images, duplicates_folder, perc_similarity)
        case 'aHash' | 'bHash' | 'dHash' | 'mHash' | 'pHash' | 'MD5' | 'SHA-1 (160-bit)' | 'SHA-2 (256-bit)' | 'SHA-2 (384-bit)' | 'SHA-2 (512-bit)':
            find_duplicates_use_hash(paths_images, duplicates_folder, hash_size, perc_similarity, method, quick, size)
        case _:
            return "Error: method not found"
        
def get_images_in_folder_and_subfolders(dir, formats):
    images = []
    for root, subdirs, files in os.walk(dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in formats:
                images.append(os.path.join(root, file))
    return images
            
def get_images_in_folder(dir, formats):
    images = []
    for file in os.listdir(dir):
        if os.path.splitext(file)[1].lower() in formats:
            images.append(os.path.join(dir, file))
    return images
            
# Example of work
dir = 'images'
images = get_images_in_folder_and_subfolders(dir, formats = ['.jpg', '.jpeg', '.png'])
# find_duplicates('images/', 'result/', perc_similarity=70, method='ORB')
find_duplicates(images, 'result/', perc_similarity=100, method='aHash')
# find_duplicates('images/', 'result/', perc_similarity=100, method='bHash', quick=False, size=256) # 26s - 8 duplicates
# find_duplicates('images/', 'result/', perc_similarity=100, method='mHash', size=16) # 16s - 8 duplicates
# find_duplicates('images/', 'result/', method='SHA-2 (512-bit)')
