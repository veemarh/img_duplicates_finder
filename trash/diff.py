from PIL import Image, ImageChops
from itertools import product
import time
  
def summarise(img):
    """Summarise an image into a 16 x 16 image."""
    resized = img.resize((16, 16))
    return resized

def difference(img1, img2):
    # start = time.monotonic()
    """Find the difference between two images."""
    diff = ImageChops.difference(img1, img2)
    print(diff.getbbox())
    diff.show()
    acc = 0
    width, height = diff.size
    for w, h in product(range(width), range(height)):
        r, g, b = diff.getpixel((w, h))
        acc += (r + g + b) / 3

    average_diff = acc / (width * height)
    normalised_diff = average_diff / 255
    # print(f'\nВремя работы diff: {time.monotonic() - start}')
    return normalised_diff
  
# Пример использования функции
img1 = "images/table5.jpg"
img2 = "images/table9.jpg"

images = {img1: Image.open(img1), img2: Image.open(img2)}

print(difference(images[img1], images[img2]))

# pip install Pillow
# pip install colorama

import os
import time


# уменьшаем изображения и сравниваем друг с другом
def check_pictures(img1, img2):
    pic_1 = Image.open(img1)
    pic_2 = Image.open(img2)

    # pic_1.thumbnail((400, 300))
    # pic_2.thumbnail((400, 300))

    # diff = ImageChops.difference(pic_1, pic_2)
    # res = diff.getbbox()
    diff = difference(pic_1, pic_2)
    print('- ', diff, img1, img2)
    # if res is None:
    if diff < 0.07:
        return True
    return False


# запускаем цикл и отправляем изображения для сравнения в функцию
def check(path_img):

    start = time.monotonic()
    if not os.path.exists(path_img):
        print('[-] Директории не существует')
        return

    images = os.listdir(path_img)
    duplicates = {}

    check_img = 0
    hasDuplicate = False
    while check_img < len(images):
        img1 = os.path.join(path_img, images[check_img])
        curr_img = 0
        while curr_img < len(images):
            if curr_img == check_img:
                curr_img += 1
                continue
            
            img2 = os.path.join(path_img, images[curr_img])
            
            if check_pictures(img1, img2):
                if not (img1 in duplicates):
                    duplicates[img1] = [img2]
                else:
                    duplicates[img1].append(img2)
                images.pop(curr_img)
                hasDuplicate = True
                continue
            
            curr_img += 1
            
        if hasDuplicate:
            images.pop(check_img)
            hasDuplicate = False
        else:
            check_img += 1
        
    print(f'\nВремя работы скрипта: {time.monotonic() - start}')
    return duplicates

    
# print(check('images/'))
