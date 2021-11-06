import os
from PIL import Image
import glob
import cv2 as cv

from pykml import parser
import pandas as pd
from imageai.Classification import ImageClassification as ic
from imageai.Detection import ObjectDetection as od
from imageai.Classification.Custom import ClassificationModelTrainer
import jinja2
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
    
    my_path = os.getenv("path_to_image_folder")
    
    pole_data = get_kml_data("p")
    pole_str = pole_data.to_string()
    f = open("poledata.txt", "a")
    f.write(pole_str)
    f.close()
    
    tran_data = get_kml_data("t")
    tran_str = tran_data.to_string()
    f = open("transdata.txt", "a")
    f.write(tran_str)
    f.close()
    
    
    #model_trainer = ClassificationModelTrainer()
    #model_trainer.setModelTypeAsResNet50()
    #model_trainer.setDataDirectory(my_path, "Training", "Testing")
    #model_trainer.trainModel(num_objects=1, num_experiments=1)


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

def get_kml_data(x):
    if x =='p':
        my_path = os.getenv("path_to_poles_kml")
    else:
        my_path = os.getenv("path_to_transformers_kml")
    with open(my_path) as f:
        folder = parser.parse(f).getroot().Document.Folder

    plnm=[]
    cordi=[]
    for pm in folder.Placemark:
        plnm1=pm.name
        plcs1=pm.Point.coordinates
        plnm.append(plnm1.text)
        cordi.append(plcs1.text)
        
    kml_data=pd.DataFrame()
    kml_data['place_name']=plnm
    kml_data['cordinates']=cordi
    kml_data['Longitude'], kml_data['Latitude'],kml_data['value'] = zip(*kml_data['cordinates'].apply(lambda x: x.split(',', 2)))
    kml_data
    return kml_data

if __name__ == "__main__":
    main()
