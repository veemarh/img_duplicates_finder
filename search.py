import os
from find_duplicates import find_duplicates
        
def get_images_in_folder_and_subfolders(dir, formats):
    images = []
    for root, subdirs, files in os.walk(dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in formats:
                images.append(os.path.join(root, file))
    return images
            
def get_images_in_folder(dir, formats):
    images = []
    for file in os.listdir(dir):
        if os.path.splitext(file)[1].lower() in formats:
            images.append(os.path.join(dir, file))
    return images
            
# Example of work
dir = 'images'
images = get_images_in_folder_and_subfolders(dir, formats = ['.jpg', '.jpeg', '.png'])
# images = get_images_in_folder(dir, formats = ['.jpg', '.jpeg', '.png'])
# find_duplicates(images, 'result/', perc_similarity=90, method='ORB')
# find_duplicates(images, 'result/', perc_similarity=100, method='aHash')
# find_duplicates(images, 'result/', perc_similarity=100, method='bHash', quick=False, size=256) # 26s - 8 duplicates
find_duplicates(images, 'result/', perc=100, method='mHash', size=16) # 16s - 8 duplicates
# find_duplicates(images, 'result/', method='SHA-2 (512-bit)')
