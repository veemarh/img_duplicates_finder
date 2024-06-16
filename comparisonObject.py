import cv2
import hashlib
import imagehash
from PIL import Image
from algorithms.bhash import bhash
from algorithms.mhash import mhash
from PIL import Image
from comparisonMethod import ComparisonMethod

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

def get_data(file_path: str, method: ComparisonMethod):
    match method.name:
        case 'ORB':
            img = cv2.imread(file_path)
            return img, img
        case _:
            img = Image.open(file_path)
            hash = get_hash(img, method)
            return img, hash
        
def get_data_obj(obj, method: ComparisonMethod):
    if isinstance(obj, Image.Image):
        return get_hash(obj, method)      
    else:    
        return obj

class ComparisonObject:
    def __init__(self, file_path: str, comparison_method: ComparisonMethod):
        self.file_path = file_path
        self.object, self.comparison_data = get_data(file_path, comparison_method)