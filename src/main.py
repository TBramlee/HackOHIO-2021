import os
from PIL import Image
import glob
import cv2 as cv
from imageai.Classification import ImageClassification as ic
from imageai.Detection import ObjectDetection as od
import numpy as np
import requests as req
import xml.etree.ElementTree as et
from dotenv import load_dotenv, find_dotenv


def main():
    load_dotenv(find_dotenv())

    image_list = load_images()
    pole_kml = get_pole_kml()
    transformer_kml = get_transformer_kml()
    
    prediction = ic()
    detection = od()
    


def load_images():
    image_list = []
    my_path = os.getenv("path_to_images")
    for filename in glob.glob(my_path):
        im = Image.open(filename)
        image_list.append(im)
    return image_list


def get_pole_kml():
    my_path = os.getenv("path_to_poles_kml")
    doc = et.parse(my_path)
    nmsp = '{http://earth.google.com/kml/2.1}'

    for pm in doc.iterfind('.//{0}Placemark'.format(nmsp)):
        print(pm.find('{0}name'.format(nmsp)).text)

        for ls in pm.iterfind('{0}MultiGeometry/{0}LineString/{0}coordinates'.format(nmsp)):
            print(ls.text.strip().replace('\n', ''))


def get_transformer_kml():
    my_path = os.getenv("path_to_transformers_kml")
    pass


if __name__ == "__main__":
    main()
