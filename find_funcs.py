import os
import cv2
from copy import copy
import imagehash
from PIL import Image
from comparisonMethod import ComparisonMethod
from comparisonObject import *

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

# find the percentage difference
def get_difference(hash1: imagehash.ImageHash, hash2: imagehash.ImageHash, hash_size: int):
    hamming_distance = hash1 - hash2
    return hamming_distance / (hash_size**2) * 100

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

# arg 'properties' has keys:
# 1 - rotated 90 deg to the right,
# 2 - rotated 180 deg,
# 3 - rotated 90 deg to the left, 
# 4 - reflected horizontally,
# 5 - reflected vertically,
# 6 - reflected horizontally and rotated 90 degrees to the right,
# 7 - reflected vertically and rotated 90 degrees to the left
def check_modified(obj: ComparisonObject, obj_to_mod: ComparisonObject, method: ComparisonMethod, properties={1: True, 2: True, 3: True, 4: True, 5: True}):
    img_to_mod = copy(obj_to_mod.object)
    if properties[1]:
        modified_img = modify_img(img_to_mod, 1)
        modified_comparison_data = get_data_obj(modified_img, method)
        if is_duplicates(obj.comparison_data, modified_comparison_data, method): return True
        
    if properties[2]:
        modified_img = modify_img(img_to_mod, 2)
        modified_comparison_data = get_data_obj(modified_img, method)
        if is_duplicates(obj.comparison_data, modified_comparison_data, method): return True
        
    if properties[3]:
        modified_img = modify_img(img_to_mod, 3)
        modified_comparison_data = get_data_obj(modified_img, method)
        if is_duplicates(obj.comparison_data, modified_comparison_data, method): return True
        
    if properties[4]:
        modified_img = modify_img(img_to_mod, 4)
        modified_comparison_data = get_data_obj(modified_img, method)
        if is_duplicates(obj.comparison_data, modified_comparison_data, method): return True
        
    if properties[5]:
        modified_img = modify_img(img_to_mod, 5)
        modified_comparison_data = get_data_obj(modified_img, method)
        if is_duplicates(obj.comparison_data, modified_comparison_data, method): return True
        
    if properties[6]:
        modified_img = modify_img(img_to_mod, 6)
        modified_comparison_data = get_data_obj(modified_img, method)
        if is_duplicates(obj.comparison_data, modified_comparison_data, method): return True
    
    if properties[7]:
        modified_img = modify_img(img_to_mod, 7)
        modified_comparison_data = get_data_obj(modified_img, method)
        if is_duplicates(obj.comparison_data, modified_comparison_data, method): return True
        
    return False

def modify_img(img, option: int):
    if isinstance(img, Image.Image):
        img = modify_img_with_Image(img, option)
    else:
        img = modify_img_with_cv2(img, option)
    return img
    
def modify_img_with_Image(img: Image, option: int):
    match option:
        case 1:
            return img.rotate(90, expand=True)
        case 2:
            return img.rotate(180, expand=True)
        case 3:
            return img.rotate(-90, expand=True)
        case 4:
            return img.transpose(Image.FLIP_LEFT_RIGHT)
        case 5:
            return img.transpose(Image.FLIP_TOP_BOTTOM)
        case 6:
            modified_img = img.transpose(Image.FLIP_LEFT_RIGHT)
            return modified_img.rotate(-90, expand=True)
        case 7:
            modified_img = img.transpose(Image.FLIP_TOP_BOTTOM)
            return modified_img.rotate(-90, expand=True)

def modify_img_with_cv2(img, option: int):
    match option:
        case 1:
            return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        case 2:
            return cv2.rotate(img, cv2.ROTATE_180)
        case 3:
            return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        case 4:
            return cv2.flip(img, 1) # reflected horizontally
        case 5:
            return cv2.flip(img, 0) # reflected vertically
        case 6:
            modified_img = cv2.flip(img, 1)
            return cv2.rotate(modified_img, cv2.ROTATE_90_CLOCKWISE)
        case 7:
            modified_img = cv2.flip(img, 0)
            return cv2.rotate(modified_img, cv2.ROTATE_90_CLOCKWISE)
