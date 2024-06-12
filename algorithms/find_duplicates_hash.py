import os
from pathlib import Path
import time
import imagehash
from PIL import Image
from algorithms.bhash import bhash

def get_hash(img, method='aHash', hash_size=16, quick=False, size='256x256'):
    match method:
        case 'aHash':
            return imagehash.average_hash(img, hash_size=hash_size)
        case 'bHash':
            return bhash(img, quick=quick, hash_size=hash_size, size=size)
        case 'dHash':
            return imagehash.dhash(img, hash_size=hash_size)
        case 'mHash':
            return 
        case 'pHash':
            return imagehash.phash(img, hash_size=hash_size)
        case 'MD5':
            return
        case 'SHA-1':
            return 
        case 'SHA-2':
            return

    return "Error: the method was not found"

# find the percentage difference
def get_difference(hash1, hash2, hash_size):
    hamming_distance = hash1 - hash2
    return hamming_distance / (hash_size**2) * 100
    
# search for duplicates in the source folder
def find_duplicates_use_hash(input_folder, duplicates_folder, hash_size = 16, perc = 100, method = 'aHash', quick=False, size='256x256'):
    start = time.monotonic()
    images = os.listdir(input_folder)
    check_i = 0
    curr_i = 1
    duplicate_count = 0

    while check_i < len(images):
        if images[check_i] is not None:
            checked_img = Image.open(f"{input_folder}/{images[check_i]}")
            checked_hash = get_hash(checked_img, method=method, hash_size=hash_size, quick=quick, size=size)

        while curr_i < len(images):
            if (check_i != curr_i) and (images[curr_i] is not None):
                name_curr_img = images[curr_i]
                curr_img = Image.open(f"{input_folder}/{name_curr_img}")
                curr_hash = get_hash(curr_img, method=method, hash_size=hash_size, quick=quick, size=size)
                
                # find the hash percentage difference
                diff = get_difference(checked_hash, curr_hash, hash_size)

                if diff <= (100 - perc):
                    print(name_curr_img)
                    Path(f"{input_folder}/{name_curr_img}").rename(f"{duplicates_folder}/{name_curr_img}")
                    del images[curr_i]
                    duplicate_count += 1
                else:
                    curr_i += 1
                    
        check_i += 1
        curr_i = check_i + 1
        
    print(duplicate_count, 'duplicates found')
    print(f'Script running time: {time.monotonic() - start}')