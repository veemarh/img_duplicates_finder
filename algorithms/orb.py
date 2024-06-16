import cv2

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
