import hashlib
import imagehash
from PIL import Image
from algorithms.bhash import bhash
from algorithms.mhash import mhash

def get_hash(img: Image, method_name: str = 'aHash', hash_size: int = 16, bhash_quick: bool = False, comparison_size: int = 16):
    match method_name:
        case 'aHash':
            return imagehash.average_hash(img, hash_size)
        case 'bHash':
            return bhash(img, quick=bhash_quick, size=comparison_size)
        case 'dHash':
            return imagehash.dhash(img, hash_size)
        case 'mHash':
            return mhash(img, size=comparison_size)
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
