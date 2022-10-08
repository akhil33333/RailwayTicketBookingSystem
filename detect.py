import cv2
import numpy as np
import glob


def check_covid():
    original = cv2.imread("static/uploads/uploaded_image.jpg")
    positive_images = []
    negative_images = []
    p_titles = []
    n_titles = []
    for f in glob.iglob("positive/*"):
        image = cv2.imread(f)
        p_titles.append(f)
        positive_images.append(image)

    for f in glob.iglob("negative/*"):
        image = cv2.imread(f)
        n_titles.append(f)
        negative_images.append(image)

    for image_to_compare, p_titles in zip(positive_images, p_titles):
        # 1) Check if 2 images are equals
        if original.shape == image_to_compare.shape:
            print("The images have same size and channels Positive")
            difference = cv2.subtract(original, image_to_compare)
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                print("Similarity: 100% (equal size and channels)")
                return 2

    for image_to_compare, n_titles in zip(negative_images, n_titles):
        # 1) Check if 2 images are equals
        if original.shape == image_to_compare.shape:
            print("The images have same size and channels - Negative")
            difference = cv2.subtract(original, image_to_compare)
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                print("Similarity: 100% (equal size and channels)")
                return 1

    return 0
