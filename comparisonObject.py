import cv2
from PIL import Image
from algorithms.hash import get_hash
from comparisonMethod import ComparisonMethod

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

class ComparisonObject:
    def __init__(self, file_path: str, comparison_method: ComparisonMethod):
        self.file_path = file_path
        self.object, self.comparison_data = get_data(file_path, comparison_method)
