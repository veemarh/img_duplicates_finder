import cv2
import os
from pathlib import Path
import time

""" 
resistant to
- file formats
- image rotations
- scaling
not resistant to 
- reflection on the y axis
- color correction 
"""
def get_orb_similarity(img1, img2):
    # create ORB feature extractor
    orb = cv2.ORB_create()
    # detect features from the images
    kp1, desc1 = orb.detectAndCompute(img1, None)
    kp2, desc2 = orb.detectAndCompute(img2, None)
    # create feature matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # match descriptors of both images
    matches = bf.match(desc1, desc2)
    # find the number of good matches - accept this distance is <50
    good_mathes = [i for i in matches if i.distance < 50]
    # find the percentage of similarity
    if len(matches) == 0:
        sim = 0
    else: 
        sim = len(good_mathes) / len(matches) * 100
    return sim

def is_duplicates(img1, img2, perc):
    sim_img = get_orb_similarity(img1, img2)
    if sim_img < perc and sim_img > 10:
        # the algorithm is unstable to the reflected image, 
        # so we can check that the images are not identical if we flip it over
        reflected_img = cv2.flip(img1, 1)
        sim_reflected_img = get_orb_similarity(reflected_img, img2)
    else:
        sim_reflected_img = 0
        
    if sim_img >= perc or sim_reflected_img >= perc:
        return True
    return False

# search for duplicates in the source folder
def find_duplicates(input_folder, duplicates_folder, perc):
    start = time.monotonic()
    if not os.path.exists(input_folder):
        print('The directory does not exist')
        return

    images = os.listdir(input_folder)
    duplicate_count = 0
    check_i = 0
    hasDuplicate = False
    while check_i < len(images):
        path_check_img = f"{input_folder}/{images[check_i]}"
        # reading the image
        check_img = cv2.imread(path_check_img)
        curr_i = 0
        while curr_i < len(images):
            if curr_i == check_i:
                curr_i += 1
                continue
            
            name_curr_img = images[curr_i]
            path_curr_img = f"{input_folder}/{name_curr_img}"
            # reading the image
            curr_img = cv2.imread(path_curr_img)
            
            if is_duplicates(check_img, curr_img, perc):
                # move the duplicate to the specified folder
                Path(path_curr_img).rename(f"{duplicates_folder}/{name_curr_img}")
                hasDuplicate = True
                # remove it from the list of viewed files
                images.pop(curr_i)
                duplicate_count +=1
                continue
            
            curr_i += 1
            
        if hasDuplicate:
            # remove it from the list of viewed files
            images.pop(check_i)
            hasDuplicate = False
        else:
            check_i += 1
            
    print(duplicate_count, 'duplicates found')
    print(f'Script running time: {time.monotonic() - start}')
   
# Example of work
find_duplicates('images/', 'result/', 90)
