import tensorflow as tf
import os

import file_processor as fp
import tflite_converter as cv


#unconverted_model_location = './unconverted_models/'

def conversion(unconverted_model_location):
    file_paths = fp.get_unconverted_models(unconverted_model_location)
    for file_path in file_paths:
        model_type = fp.model_type_detection(file_path)
        if model_type == 'keras':
            cv.keras_to_tflite(file_path)
            print("Model has been convereted")