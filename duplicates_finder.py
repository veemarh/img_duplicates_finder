import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_orb_sim(img1, img2):
    orb = cv2.ORB_create()

    kp1, desc1 = orb.detectAndCompute(img1, None)
    kp2, desc2 = orb.detectAndCompute(img2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc1, desc2)
   
    similar_regions = [i for i in matches if i.distance < 50]
    if len(matches) == 0:
        sim = 0
    sim = len(similar_regions) / len(matches) * 100
    
    return sim

def get_orb_similarity(img1, img2):
    sim_img = get_orb_sim(img1, img2)
    
    reflected_img = reflect_img_for_y(img1)
    sim_reflected_img = get_orb_sim(reflected_img, img2)
    
    if (sim_img > sim_reflected_img): 
        res = sim_img 
    else: 
        res = sim_reflected_img
    return res

def reflect_img_for_y(img):
    reflected_img = cv2.flip(img, 1)
    return reflected_img

# Пример использования функции
img1 = "images/image-1.jpeg"
img2 = "images/image-9.jpeg"

images = {img1: cv2.imread(img1), img2: cv2.imread(img2)}

sim = get_orb_similarity(images[img1], images[img2])
print(sim)
