import os
from pathlib import Path
import time
import imagehash
from PIL import Image

""" 
Positive
- The hash has a small size
- It is calculated quickly
- It is being searched for quickly
- Resistant to recycling

Minuses
- It is not resistant to crop
- Not resistant to turns

catches duplicates in different formats at threshold=20
"""

# search for duplicates in the source folder
def find_duplicates(input_folder, duplicates_folder, hash_size = 16, threshold = 0):
    start = time.monotonic()
    
    images = os.listdir(input_folder)
    check_i = 0
    curr_i = 1
    duplicate_count = 0
    bits_list = []

    while check_i < len(images):
        sum_diff = 0

        if images[check_i] is not None:
            check_img = Image.open(f"{input_folder}/{images[check_i]}")
            bits_list = imagehash.phash(check_img, hash_size).hash

        while curr_i < len(images):
            if (check_i != curr_i) and (images[curr_i] is not None):
                name_curr_img = images[curr_i]
                curr_img = Image.open(f"{input_folder}/{name_curr_img}")
                new_bits_list = imagehash.phash(curr_img, hash_size).hash
                
                # we compare the images by bits
                # sum up the number of different bits
                for j in range(len(bits_list)):
                    for t in range(hash_size):
                        if bits_list[j][t] != new_bits_list[j][t]:
                            sum_diff += 1
                
                # we find the difference in percentages          
                diff_prec = sum_diff / (hash_size * hash_size) * 100
                if diff_prec <= threshold:
                    # move the duplicate to the specified folder
                    Path(f"{input_folder}/{name_curr_img}").rename(f"{duplicates_folder}/{name_curr_img}")
                    del images[curr_i]
                    duplicate_count += 1
                else:   
                    curr_i += 1

                sum_diff = 0
        check_i += 1
        curr_i = check_i + 1
        
    print(duplicate_count, 'duplicates found')
    print(f'Script running time: {time.monotonic() - start}')
    
# Example of work
find_duplicates('images/', 'result/', threshold = 30)   