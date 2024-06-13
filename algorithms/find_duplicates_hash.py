import os
from pathlib import Path
import time
import imagehash
import hashlib
from PIL import Image
from algorithms.bhash import bhash
from algorithms.mhash import mhash

def get_hash(img, method='aHash', hash_size=16, quick=False, size=16):
    match method:
        case 'aHash':
            return imagehash.average_hash(img, hash_size)
        case 'bHash':
            return bhash(img, quick=quick, size=size)
        case 'dHash':
            return imagehash.dhash(img, hash_size)
        case 'mHash':
            return mhash(img, size=size)
        case 'pHash':
            return imagehash.phash(img, hash_size)
        case 'MD5':
            return hashlib.md5(img.tobytes()).hexdigest()
        case 'SHA-1 (160-bit)':
            return hashlib.sha1(img.tobytes()).hexdigest()
        case 'SHA-2 (256-bit)':
            return hashlib.sha256(img.tobytes()).hexdigest()
        case 'SHA-2 (384-bit)':
            return hashlib.sha384(img.tobytes()).hexdigest()
        case 'SHA-2 (512-bit)':
            return hashlib.sha512(img.tobytes()).hexdigest()
        case _:
            return "Error: the method was not found"

# find the percentage difference
def get_difference(hash1, hash2, hash_size):
    hamming_distance = hash1 - hash2
    return hamming_distance / (hash_size**2) * 100
    
# search for duplicates in the source folder
def find_duplicates_use_hash(paths_images, duplicates_folder, hash_size=16, perc=100, method='aHash', quick=False, size=16):
    start = time.monotonic()
   
    check_i = 0
    curr_i = 1
    duplicate_count = 0

    while check_i < len(paths_images):
        if paths_images[check_i] is not None:
            path_checked_img = paths_images[check_i]
            checked_img = Image.open(path_checked_img)
            checked_hash = get_hash(checked_img, method=method, hash_size=hash_size, quick=quick, size=size)

        while curr_i < len(paths_images):
            if (check_i != curr_i) and (paths_images[curr_i] is not None):
                path_curr_img = paths_images[curr_i]
                curr_img = Image.open(path_curr_img)
                curr_hash = get_hash(curr_img, method=method, hash_size=hash_size, quick=quick, size=size)
                
                # find the hash percentage difference
                match method:
                    case 'MD5' | 'SHA-1 (160-bit)' | 'SHA-2 (256-bit)' | 'SHA-2 (384-bit)' | 'SHA-2 (512-bit)':
                        diff = 0 if checked_hash == curr_hash else 100
                    case _:
                        diff = get_difference(checked_hash, curr_hash, hash_size)

                if diff <= (100 - perc):
                    print(f"{path_checked_img} - {path_curr_img}")
                    name_curr_img = os.path.basename(path_curr_img)
                    Path(path_curr_img).rename(f"{duplicates_folder}/{name_curr_img}")
                    del paths_images[curr_i]
                    duplicate_count += 1
                else:
                    curr_i += 1
                    
        check_i += 1
        curr_i = check_i + 1
        
    print(duplicate_count, 'duplicates found')
    print(f'Script running time: {time.monotonic() - start}')