import os
from PIL import Image
import glob
import cv2 as cv
from imageai.Detection import ObjectDetection as od
import numpy as np
import requests as req
import os as os
import xml.etree.ElementTree as et


def main():
    image_list = load_images()
    pole_coordinates = get_pole_coords()
    transformer_coordinates = get_transformer_coords()


def load_images():
    image_list = []
    my_path = r'C:\Users\Michael Stiffler\Desktop\HackOHIO\images\*.JPG'
    for filename in glob.glob(my_path):
        im = Image.open(filename)
        image_list.append(im)
    return image_list


def get_pole_coords():
    my_path = r'C:\Users\Michael Stiffler\Desktop\HackOHIO\images\Poles.kml'
    doc = et.parse("kml/Poles.kml")
    print(doc.__sizeof__())
    nmsp = '{http://earth.google.com/kml/2.1}'

    for pm in doc.iterfind('.//{0}Placemark'.format(nmsp)):
        print(pm.find('{0}name'.format(nmsp)).text)

        for ls in pm.iterfind('{0}MultiGeometry/{0}LineString/{0}coordinates'.format(nmsp)):
            print(ls.text.strip().replace('\n', ''))


def get_transformer_coords():
    my_path = r'C:\Users\Michael Stiffler\Desktop\HackOHIO\images\Transformers.kml'
    pass


if __name__ == "__main__":
    main()
