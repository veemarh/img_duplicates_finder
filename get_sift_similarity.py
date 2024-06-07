import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_sift_descriptor(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    # sift_img = cv2.drawKeypoints(gray, keypoints, img)
    # cv2.imshow('image', sift_img)
    return keypoints, descriptors

def reflect_img_for_y(img):
    reflected_img = cv2.flip(img, 1)
    return reflected_img

def get_sift_similarity(img1, img2):
    sim_img = get_sift_sim(img1, img2)

    reflected_img = reflect_img_for_y(img1)
    sim_reflected_img = get_sift_sim(reflected_img, img2)

    if (sim_img > sim_reflected_img): 
        res = sim_img 
    else: 
        res = sim_reflected_img
    return res

def get_sift_sim(img1, img2):
    bf = cv2.BFMatcher()
    kp1, desc1 = get_sift_descriptor(img1)
    kp2, desc2 = get_sift_descriptor(img2)
    matches = bf.knnMatch(desc1, desc2, k = 2)
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append([m])
    # img3 = cv2.drawMatchesKnn(img,kp,cimages[key],keypoints[key],good_matches,None,flags=0)
    # plt.imshow(img3),plt.show()
    similarity = len(good_matches) / min(len(kp1), len(kp2)) * 100
    return similarity

# Пример использования функции
img1 = 'image-1.jpeg'
img2 = 'image-7.jpeg'

images = {img1: cv2.imread(img1), 
          img2: cv2.imread(img2)}

sim = get_sift_similarity(images[img1], images[img2])
print(sim)