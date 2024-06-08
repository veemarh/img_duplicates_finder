from PIL import Image, ImageChops
from itertools import product
  
def summarise(img):
    """Summarise an image into a 16 x 16 image."""
    resized = img.resize((16, 16))
    return resized

def difference(img1, img2):
    """Find the difference between two images."""
    diff = ImageChops.difference(img1, img2)

    acc = 0
    width, height = diff.size
    for w, h in product(range(width), range(height)):
        r, g, b = diff.getpixel((w, h))
        acc += (r + g + b) / 3

    average_diff = acc / (width * height)
    normalised_diff = average_diff / 255
    return normalised_diff
  
# Пример использования функции
img1 = "images/img1.jpg"
img2 = "images/img4.jpg"

images = {img1: Image.open(img1), img2: Image.open(img2)}

print(difference(images[img1], images[img2]))
