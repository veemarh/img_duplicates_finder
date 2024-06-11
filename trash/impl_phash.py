import cv2
import os
from pathlib import Path
import time

# https://habr.com/ru/articles/120562/

""" 
Algorithm
- Image compression to the size of NxN pixels
- Converting pixels to black and white
- Calculating the average color value of all pixels
- Creating a new image (hash): if the pixel color value exceeds the average, 
    then make it white, otherwise - black
- Comparing hashes of all images using the Hamming distance
- Images are considered similar and are moved from the specified folder 
    if the difference between the number of identical pixels does not exceed the sensitivity 
    threshold set by the user
"""

def calculate_mean(pixels_list):
    mean = 0
    total_pixels = len(pixels_list)
    for i in range(total_pixels):
        mean += pixels_list[i] / total_pixels
    return mean

def grab_pixels(squeezed_frame):
    pixels_list = []
    for x in range(0, squeezed_frame.shape[1], 1):
        for y in range(0, squeezed_frame.shape[0], 1):
            pixel_color = squeezed_frame[x, y]
            pixels_list.append(pixel_color)
    return pixels_list

def make_bits_list(mean, pixels_list):
    bits_list = []
    for i in range(len(pixels_list)):
        if pixels_list[i] >= mean:
            bits_list.append(255)
        else:
            bits_list.append(0)
    return bits_list

def hashify(squeezed_frame, bits_list):
    bit_index = 0
    hashed_frame = squeezed_frame
    for x in range(0, squeezed_frame.shape[1], 1):
        for y in range(0, squeezed_frame.shape[0], 1):
            hashed_frame[x, y] = bits_list[bit_index]
            bit_index += 1
    return hashed_frame

def generate_hash(frame, hash_size):
    frame_squeezed = cv2.resize(frame, (hash_size, hash_size))
    frame_squeezed = cv2.cvtColor(frame_squeezed, cv2.COLOR_BGR2GRAY)
    pixels_list = grab_pixels(frame_squeezed)
    mean_color = calculate_mean(pixels_list)
    bits_list = make_bits_list(mean_color, pixels_list)
    return bits_list


def find_duplicates(input_folder, duplicates_folder, hash_size = 16, threshold = 0):
    start = time.monotonic()
    files = os.listdir(input_folder)
    i = 0
    k = 1
    frame = None
    duplicate_count = 0
    bits_list = []

    while i < len(files):
        sum_diff = 0

        if files[i] is not None:
            frame = cv2.imread(f"{input_folder}/{files[i]}")
            bits_list = generate_hash(frame, hash_size)

        while k < len(files):
            if (i != k) and (files[k] is not None):
                new_frame = cv2.imread(f"{input_folder}/{files[k]}")
                new_bits_list = generate_hash(new_frame, hash_size)

                for j in range(len(bits_list)):
                    if bits_list[j] != new_bits_list[j]:
                        sum_diff += 1

                if sum_diff <= hash_size * hash_size * threshold / 100:
                    Path(f"{input_folder}/{files[k]}").rename(f"{duplicates_folder}/{files[k]}")
                    del files[k]
                    duplicate_count += 1
                else:
                    k += 1

                sum_diff = 0
        i += 1
        k = i + 1
        
    print(duplicate_count, 'duplicates found')
    print(f'Script running time: {time.monotonic() - start}')

find_duplicates('images/', 'result/', threshold=20)
