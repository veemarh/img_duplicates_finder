import os
import cv2
import imagehash
import hashlib
from PIL import Image
from algorithms.bhash import bhash
from algorithms.mhash import mhash

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

def func_get_data(method):
    match method:
        case 'ORB':
            return get_data_orb
        case _:
            return get_data_hash

def find_percentage_difference(data1, data2, method, similarity, hash_size):
    match method:
        case 'ORB':
            diff = similarity - get_orb_similarity(data1, data2)
        case 'MD5' | 'SHA-1 (160-bit)' | 'SHA-2 (256-bit)' | 'SHA-2 (384-bit)' | 'SHA-2 (512-bit)':
            diff = 0 if data1 == data2 else 100
        case _:
            diff = get_difference(data1, data2, hash_size)
    return diff

def check_identical_properties(file1, file2, properties={'name': False, 'format': False, 'size': False}):
    if properties['name']:
        name1 = os.path.splitext(os.path.basename(file1))[0]
        name2 = os.path.splitext(os.path.basename(file2))[0]
        if not name1 == name2:
            return False
    if properties['format']:
        format1 = os.path.splitext(os.path.basename(file1))[1].lower()
        format2 = os.path.splitext(os.path.basename(file2))[1].lower()
        if not format1 == format2:
            return False
    if properties['size']:
        size1 = os.path.getsize(file1)
        size2 = os.path.getsize(file2)
        if not size1 == size2:
            return False
    return True
