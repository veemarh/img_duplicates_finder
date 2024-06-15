import os
        
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
            