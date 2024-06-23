""" 
The comparison method mHash (Median Hash) resizes the image to 8x8 or 16x16 pixel. 
The image is then converted to grayscale and the mean color value of all image pixels is determined. 
Then all image pixels are compared with the mean color value and the checksum is calculated.
"""
from PIL import Image
import imagehash

def bin_str_to_hex(str):
    return '{0:0={width}x}'.format(int(str, 2), width = len(str) // 4)

def mhash(img: Image, size: int = 16):
    # 'size': int
    #     help='Resize image to specified size before hashing, e.g. 16x16')
    if size <= 0: 
        raise Exception('Invalid size value')
    
    grey_img = img.convert('L')
    grey_img = grey_img.resize((size, size), Image.BILINEAR)
    pixels = list(grey_img.getdata())
    median_pixel = sorted(pixels)[len(pixels) // 2]
    bin_hash_str = ''.join(['1' if p > median_pixel else '0' for p in pixels])
    hex_hash_str = bin_str_to_hex(bin_hash_str)
    return imagehash.hex_to_hash(hex_hash_str)
