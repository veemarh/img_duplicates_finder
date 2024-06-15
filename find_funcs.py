import os
import cv2
import imagehash
import hashlib
from PIL import Image
from algorithms.bhash import bhash
from algorithms.mhash import mhash
from comparisonMethod import ComparisonMethod

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

def get_hash(img: Image, method: ComparisonMethod):
    name = method.name
    hash_size = method.hash_size
    quick = method.bhash_quick
    size = method.comparison_size
    match name:
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
def get_difference(hash1: imagehash.ImageHash, hash2: imagehash.ImageHash, hash_size: int):
    hamming_distance = hash1 - hash2
    return hamming_distance / (hash_size**2) * 100

def get_data(file_path: str, method: ComparisonMethod):
    match method.name:
        case 'ORB':
            img = cv2.imread(file_path)
            return img, img
        case _:
            img = Image.open(file_path)
            hash = get_hash(img, method)
            return img, hash

def find_percentage_difference(data1, data2, method: ComparisonMethod):
    match method.name:
        case 'ORB':
            diff = method.similarity - get_orb_similarity(data1, data2)
        case 'MD5' | 'SHA-1 (160-bit)' | 'SHA-2 (256-bit)' | 'SHA-2 (384-bit)' | 'SHA-2 (512-bit)':
            diff = 0 if data1 == data2 else 100
        case _:
            diff = get_difference(data1, data2, method.hash_size)
    return diff

def is_duplicates(data1, data2, method: ComparisonMethod):                    
    # find the percentage difference
    diff = find_percentage_difference(data1, data2, method)
    return diff <= (100 - method.similarity)

def check_identical_properties(file1: str, file2: str, properties={'name': False, 'format': False, 'size': False}):
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

def check_modified():
    return

def modify_image(img, properties):
    if isinstance(img, Image.Image):
        return modify_image_with_Image(img, properties)
    return modify_image_with_cv2(img, properties)

# arg 'modified_images_properties' has keys:
# 1 - rotated 90 deg to the right,
# 2 - rotated 180 deg,
# 3 - rotated 90 deg to the left, 
# 4 - reflected horizontally,
# 5 - reflected vertically
def modify_image_with_Image(check_img, img_to_modif: Image, properties):
    if properties[1]:
        modified_img = img_to_modif.rotate(-90, expand=True)
        check_modified(check_img, modified_img)
        return 

def modify_image_with_cv2(img, properties):
    return


# modify_image(Image.open('images/image-1.jpeg'), {1: True, 2: True, 3: True, 4: True, 5: True})