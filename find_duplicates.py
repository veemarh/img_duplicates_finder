import os
import cv2
from pathlib import Path
import time
import imagehash
import hashlib
from PIL import Image
from algorithms.bhash import bhash
from algorithms.mhash import mhash

""" 
resistant to
- file formats
- image rotations
- scaling
not resistant to 
- reflection on the y axis
- color correction 
"""
def get_orb_similarity(img1, img2):
    # create ORB feature extractor
    orb = cv2.ORB_create()
    # detect features from the images
    kp1, desc1 = orb.detectAndCompute(img1, None)
    kp2, desc2 = orb.detectAndCompute(img2, None)
    # create feature matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # match descriptors of both images
    matches = bf.match(desc1, desc2)
    # find the number of good matches - accept this distance is <50
    good_mathes = [i for i in matches if i.distance < 50]
    # find the percentage of similarity
    if len(matches) == 0:
        sim = 0
    else: 
        sim = len(good_mathes) / len(matches) * 100
    return sim

# def is_duplicates(img1, img2, perc):
#     sim_img = get_orb_similarity(img1, img2)
#     if sim_img < perc and sim_img > 10:
#         # the algorithm is unstable to the reflected image, 
#         # so we can check that the images are not identical if we flip it over
#         reflected_img = cv2.flip(img1, 1)
#         sim_reflected_img = get_orb_similarity(reflected_img, img2)
#     else:
#         sim_reflected_img = 0
        
#     if sim_img >= perc or sim_reflected_img >= perc:
#         return True
#     return False

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

def get_data_orb(file_path, method, hash_size, quick, size):
    return cv2.imread(file_path)

def get_data_hash(file_path, method, hash_size, quick, size):
    img = Image.open(file_path)
    hash = get_hash(img, method, hash_size, quick, size)
    return hash

# arg 'quick' only for bhash - parameter 'Fast' = True, 'Precise' = False
# arg 'size' for bhash and mhash - parameter 'Comparison area' (bhash:128x128, 256x256, 512x512; mhash: 8x8, 16x16 )    

# search for duplicates in the source folder
def find_duplicates(paths_images, duplicates_folder, hash_size=16, perc=100, method='aHash', quick=False, size=16):
    start = time.monotonic()
    
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
            checked_data = get_data(path_checked_img, method, hash_size, quick, size)
                
        while curr_i < len(paths_images):
            if (check_i != curr_i) and (paths_images[curr_i] is not None):
                path_curr_img = paths_images[curr_i]
                curr_data = get_data(path_curr_img, method, hash_size, quick, size)
                
                # find the percentage difference
                match method:
                    case 'ORB':
                        diff = perc - get_orb_similarity(checked_data, curr_data)
                    case 'MD5' | 'SHA-1 (160-bit)' | 'SHA-2 (256-bit)' | 'SHA-2 (384-bit)' | 'SHA-2 (512-bit)':
                        diff = 0 if checked_data == curr_data else 100
                    case _:
                        diff = get_difference(checked_data, curr_data, hash_size)

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