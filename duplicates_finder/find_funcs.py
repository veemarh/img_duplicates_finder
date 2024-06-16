import os
import cv2
import imagehash
from PIL import Image
from algorithms.hash import get_hash
from duplicates_finder.comparisonMethod import ComparisonMethod

def get_data(file_path: str, method: ComparisonMethod):
    name = method.name
    match name:
        case 'ORB':
            img = cv2.imread(file_path)
            return img, img
        case _:
            hash_size = method.hash_size
            quick = method.bhash_quick
            size = method.comparison_size
            img = Image.open(file_path)
            hash = get_hash(img, name, hash_size, quick, size)
            return img, hash
        
def get_data_obj(obj, method: ComparisonMethod):
    name = method.name
    if isinstance(obj, Image.Image):
        hash_size = method.hash_size
        quick = method.bhash_quick
        size = method.comparison_size
        return get_hash(obj, name, hash_size, quick, size)      
    else:    
        return obj

# find the percentage difference
def get_difference(hash1: imagehash.ImageHash, hash2: imagehash.ImageHash, hash_size: int):
    hamming_distance = hash1 - hash2
    return hamming_distance / (hash_size**2) * 100

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
