# Perceptual image hash calculation tool based on algorithm descibed in
# Block Mean Value Based Image Perceptual Hashing by Bian Yang, Fan Gu and Xiamu Niu

import math
import imagehash
import PIL.Image as Image

def median(data):
    data = sorted(data)
    length = len(data)
    if length % 2 == 0:
        return (data[length // 2 - 1] + data[length // 2]) / 2.0
    return data[length // 2]

def total_value_rgba(im, data, x, y):
    r, g, b, a = data[y * im.size[0] + x]
    if a == 0:
        return 765
    else:
        return r + g + b

def total_value_rgb(img, data, x, y):
    r, g, b = data[y * img.size[0] + x]
    return r + g + b

def translate_blocks_to_bits(blocks, pixels_per_block):
    half_block_value = pixels_per_block * 256 * 3 / 2

    # Compare medians across four horizontal bands
    bandsize = len(blocks) // 4
    for i in range(4):
        m = median(blocks[i * bandsize : (i + 1) * bandsize])
        for j in range(i * bandsize, (i + 1) * bandsize):
            v = blocks[j]

            # Output a 1 if the block is brighter than the median.
            # With images dominated by black or white, the median may
            # end up being 0 or the max value, and thus having a lot
            # of blocks of value equal to the median.  To avoid
            # generating hashes of all zeros or ones, in that case output
            # 0 if the median is in the lower value space, 1 otherwise
            blocks[j] = int(v > m or (abs(v - m) < 1 and m > half_block_value))


def bits_to_hexhash(bits):
    return '{0:0={width}x}'.format(int(''.join([str(x) for x in bits]), 2), width = len(bits) // 4)


def blockhash_even(img, hash_size):
    if img.mode == 'RGBA':
        total_value = total_value_rgba
    elif img.mode == 'RGB':
        total_value = total_value_rgb
    else:
        raise RuntimeError('Unsupported image mode: {}'.format(img.mode))

    data = img.getdata()
    width, height = img.size
    blocksize_x = width // hash_size
    blocksize_y = height // hash_size

    result = []

    for y in range(hash_size):
        for x in range(hash_size):
            value = 0

            for iy in range(blocksize_y):
                for ix in range(blocksize_x):
                    cx = x * blocksize_x + ix
                    cy = y * blocksize_y + iy
                    value += total_value(img, data, cx, cy)

            result.append(value)

    translate_blocks_to_bits(result, blocksize_x * blocksize_y)
    return bits_to_hexhash(result)

def blockhash(img, hash_size):
    if img.mode == 'RGBA':
        total_value = total_value_rgba
    elif img.mode == 'RGB':
        total_value = total_value_rgb
    else:
        raise RuntimeError('Unsupported image mode: {}'.format(img.mode))

    data = img.getdata()
    width, height = img.size

    even_x = width % hash_size == 0
    even_y = height % hash_size == 0

    if even_x and even_y:
        return blockhash_even(img, hash_size)

    blocks = [[0 for col in range(hash_size)] for row in range(hash_size)]

    block_width = float(width) / hash_size
    block_height = float(height) / hash_size

    for y in range(height):
        if even_y:
            # don't bother dividing y, if the size evenly divides by bits
            block_top = block_bottom = int(y // block_height)
            weight_top, weight_bottom = 1, 0
        else:
            y_frac, y_int = math.modf((y + 1) % block_height)

            weight_top = (1 - y_frac)
            weight_bottom = (y_frac)

            # y_int will be 0 on bottom/right borders and on block boundaries
            if y_int > 0 or (y + 1) == height:
                block_top = block_bottom = int(y // block_height)
            else:
                block_top = int(y // block_height)
                block_bottom = int(-(-y // block_height)) # int(math.ceil(float(y) / block_height))

        for x in range(width):
            value = total_value(img, data, x, y)

            if even_x:
                # don't bother dividing x, if the size evenly divides by bits
                block_left = block_right = int(x // block_width)
                weight_left, weight_right = 1, 0
            else:
                x_frac, x_int = math.modf((x + 1) % block_width)

                weight_left = (1 - x_frac)
                weight_right = (x_frac)

                # x_int will be 0 on bottom/right borders and on block boundaries
                if x_int > 0 or (x + 1) == width:
                    block_left = block_right = int(x // block_width)
                else:
                    block_left = int(x // block_width)
                    block_right = int(-(-x // block_width)) # int(math.ceil(float(x) / block_width))

            # add weighted pixel value to relevant blocks
            blocks[block_top][block_left] += value * weight_top * weight_left
            blocks[block_top][block_right] += value * weight_top * weight_right
            blocks[block_bottom][block_left] += value * weight_bottom * weight_left
            blocks[block_bottom][block_right] += value * weight_bottom * weight_right

    result = [blocks[row][col] for row in range(hash_size) for col in range(hash_size)]

    translate_blocks_to_bits(result, block_width * block_height)
    return bits_to_hexhash(result)

def bhash(img: Image, quick = False, hash_size = 16, size = '256x256'):
    # 'quick': type=bool, default=False,
    #     help='Use quick hashing method. Default: False'
    # 'hash_size': type=int, default=16,
    #     help='Create hash of size N^2 bits. Default: 16')
    # 'size':
    #     help='Resize image to specified size before hashing, e.g. 256x256')
  
    if quick:
        method = blockhash_even
    else:
        method = blockhash

    # convert indexed/grayscale images to RGB
    if img.mode == '1' or img.mode == 'L' or img.mode == 'P':
        img = img.convert('RGB')
    elif img.mode == 'LA':
        img = img.convert('RGBA')
    # resize the image
    if size:
        size = size.split('x')
        size = (int(size[0]), int(size[1]))
        img = img.resize(size, Image.BILINEAR)

    hash = method(img, hash_size)
    return imagehash.hex_to_hash(hash)
