import os,sys
sys.path.append("./precision-medicine-toolbox/")
from pmtool.ToolBox import ToolBox
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pymongo
from modules.nodule_features import get_all_features
from pymongo import MongoClient


'''
How to run:
$ python dicom_to_nrrd.py PACIENT_FOLDER
'''
# Arguments
name_of_pacient = sys.argv[1]

path_to_data = "C:\\Users\\fabi2\\OneDrive\\Desktop\\Betty's idea of doing shit\\"

parameters = {'data_path': path_to_data + name_of_pacient + "\\dcms\\", # path to your DICOM data
              'data_type': 'dcm', # original data format: DICOM
              'multi_rts_per_pat': True}   # when False, it will look only for 1 rtstruct in the patient folder, 
                                            # this will speed up the process, 
                                            # if you have more then 1 rtstruct per patient, set it to True

export_path = path_to_data + name_of_pacient + "\\" # the function will create 'converted_nrrd' folder in the specified directory
data_ct = ToolBox(**parameters)
data_ct.convert_to_nrrd(export_path, 'gtv')

# Generate the 2D PNG files of the nodule
data_path = path_to_data + name_of_pacient + "\\converted_nrrds\\"
data_ct_nrrd = ToolBox(data_path, data_type='nrrd')
data_ct_nrrd.get_jpegs(path_to_data + name_of_pacient + "\\") # the function will create 'images_quick_check' folder in the specified directory 

# Your MongoDB Atlas cluster connection string
MONGO_CONNECTION_STRING = "mongodb+srv://dianavelciov:parola@cluster0.qqmezlq.mongodb.net/cool_notes_app?retryWrites=true&w=majority"

# Create a MongoClient to the running MongoDB Atlas cluster instance
client = MongoClient(MONGO_CONNECTION_STRING)

# Getting a Database
db = client.cool_notes_app

# Getting a Collection
collection = db.patients

def get_subdirectories(folder):
    return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

path_to_data += name_of_pacient + "\\"
data_folder = path_to_data + "converted_nrrds\\"
subdirectories = get_subdirectories(data_folder)

# Initialize the vectors for features
nodule_volume = []
nodule_fractal_dimension = []
nodule_area = []
calcification = []
spiculation = []
type_of_nodule = []

nodule_volume, nodule_fractal_dimension, nodule_area, calcification, spiculation, type_of_nodule = get_all_features(data_folder, subdirectories) 

data = []
for i, selected_folder in enumerate(subdirectories):
    data.append({
        "nodule_volume": nodule_volume[i],
        "nodule_area": nodule_area[i],
        "fractal_dimension": nodule_fractal_dimension[i],
        "calcification": calcification[i].tolist() if isinstance(calcification[i], np.ndarray) else calcification[i],
        "spiculation": spiculation[i].tolist() if isinstance(spiculation[i], np.ndarray) else spiculation[i],
        "type_of_nodule": type_of_nodule[i]
    })
    print("Data is:", data[i])

result = collection.update_one({"cnp": name_of_pacient}, {"$set": {"Data": data}}, upsert=True)
