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
            print("Keras model has been convereted to tflite")
        elif model_type == 'tensorflow':
            cv.tensorflow_to_tflite(file_path)
            print("Tensorflow Model has been convereted to tflite")
        elif model_type == 'pytorch':
            cv.pytorch_to_tflite(file_path)
        else:
            print("Model type can not be recognized")