import os
import sys
from PIL import Image
import glob
import cv2 as cv

from imageai.Classification import ImageClassification as ic
from imageai.Detection import ObjectDetection as od

from imageai.Classification.Custom import ClassificationModelTrainer
from imageai.Detection.Custom import DetectionModelTrainer

import numpy as np
import requests as req
import xml.etree.ElementTree as et
from dotenv import load_dotenv, find_dotenv


def main():
    load_dotenv(find_dotenv())

    
    # image_list = load_images()
    # pole_kml = get_pole_kml()
    # transformer_kml = get_transformer_kml()

    # prediction = ic()
    # detection = od()

   # my_path = os.getenv("poles_folder")
    my_path_ = os.getcwd() + "\poles"

    trainer = DetectionModelTrainer()
    trainer.setModelTypeAsYOLOv3()
    trainer.setDataDirectory(data_directory=my_path_)
    trainer.setTrainConfig(object_names_array=[
                           "pole"], batch_size=4, num_experiments=1, train_from_pretrained_model="pretrained-yolov3.h5")
    trainer.trainModel()

    """
    model_trainer = ClassificationModelTrainer()
    model_trainer.setModelTypeAsResNet50()
    model_trainer.setDataDirectory(my_path)
    model_trainer.trainModel(num_objects=10, num_experiments=100,
                             enhance_data=True, batch_size=32, show_network_summary=True)
    """




def cleanup():
    # my_path = r"{}".format(my_path_)
    my_path_ = os.getcwd() + "/poles" + "/train/annotations/"
    counter = 1
    
    for filename in os.listdir(my_path_):
        
        fileNum = filename[4: len(filename) - 4]
        
        #(fileNum)
        
        #Full path of .jpg file
        newHeader = "img_" + fileNum + ".jpg"
        
        #Full path of XML file
        fullFilename = os.getcwd() + "/poles" + "/train/annotations/" + filename
        
        tree = et.parse(fullFilename)
        root = tree.getroot()
        
        root[0].text = "annotations"
        
        tree.write(fullFilename)
        #used to convert names of .jpg and .xml
        
        #new_filename = my_path_ + filename
        #os.rename(new_filename, string)
        counter += 1
    


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
