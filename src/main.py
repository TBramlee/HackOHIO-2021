import os
from PIL import Image
import glob


def main():
    image_list = load_images()


def load_images():
    image_list = []
    my_path = r'C:\Users\Michael Stiffler\Desktop\HackOHIO\images\*.JPG'
    for filename in glob.glob(my_path):
        im = Image.open(filename)
        image_list.append(im)
    return image_list


if __name__ == "__main__":
    main()
