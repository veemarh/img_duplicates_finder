import cv2
import numpy as np
import os
import time

def get_orb_sim(img1, img2):
    orb = cv2.ORB_create()

    kp1, desc1 = orb.detectAndCompute(img1, None)
    kp2, desc2 = orb.detectAndCompute(img2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc1, desc2)
   
    good_mathes = [i for i in matches if i.distance < 50]
    if len(matches) == 0:
        sim = 0
    sim = len(good_mathes) / len(matches) * 100
    
    return sim

def get_orb_similarity(img1, img2):
    # start = time.monotonic()
    sim_img = get_orb_sim(img1, img2)
    
    reflected_img = reflect_img_for_y(img1)
    sim_reflected_img = get_orb_sim(reflected_img, img2)
    
    if (sim_img > sim_reflected_img): 
        res = sim_img 
    else: 
        res = sim_reflected_img
    # print(f'\nВремя работы orb: {time.monotonic() - start}')
    return res

def reflect_img_for_y(img):
    reflected_img = cv2.flip(img, 1)
    return reflected_img

def is_duplicate(img1, img2, proc):
    
    img1 = cv2.imread(img1)
    img2 = cv2.imread(img2)

    similarity = get_orb_similarity(img1, img2)
    if similarity >= proc:
        return True
    return False

def find_duplicates_img(path_img, proc = 100):

    start = time.monotonic()
    if not os.path.exists(path_img):
        print('Директории не существует')
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
            
            if is_duplicate(img1, img2, proc):
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

# Пример использования функции
# img1 = "images/image-1.jpeg"
# img2 = "images/image-7.jpeg"

# images = {img1: cv2.imread(img1), img2: cv2.imread(img2)}

# sim = get_orb_similarity(images[img1], images[img2])
# print(sim)

print(find_duplicates_img('C:/Users/icecr/.vscode/img_duplicates_finder/images', 70))
