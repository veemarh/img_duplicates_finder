import cv2
import os
from pathlib import Path
import time
import imagehash
from PIL import Image

def find_duplicates(input_folder, duplicates_folder, hash_size = 16, threshold = 0):
    start = time.monotonic()
    images = os.listdir(input_folder)
    i = 0
    k = 1
    duplicate_count = 0

    while i < len(images):
        if images[i] is not None:
            check_img = Image.open(f"{input_folder}/{images[i]}")
            check_hash = imagehash.phash(check_img, hash_size)

        while k < len(images):
            if (i != k) and (images[k] is not None):
                name_curr_img = images[k]
                curr_img = Image.open(f"{input_folder}/{name_curr_img}")
                curr_hash = imagehash.phash(curr_img, hash_size)

                hamming_distance = check_hash - curr_hash

                if hamming_distance <= threshold:
                    Path(f"{input_folder}/{name_curr_img}").rename(f"{duplicates_folder}/{name_curr_img}")
                    del images[k]
                    duplicate_count += 1
                else:
                    k += 1

        i += 1
        k = i + 1
        
    print(duplicate_count, 'duplicates found')
    print(f'Script running time: {time.monotonic() - start}')

find_duplicates('result/', 'result/', threshold=50)
    
# как вычисляется расстояние Хэмминга для этого хэша? 
# не работает на одном и том же формате файла