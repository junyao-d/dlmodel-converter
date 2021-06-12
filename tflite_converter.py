import tensorflow as tf
import os
import onnx
import onnx_tf
import torch
import numpy as np

pwd = os.path.dirname(__file__)
staging_folder = os.path.join(pwd, 'model_file_staging')
OUTPUT_FOLDER = os.path.join(staging_folder,'output_models')
SAVEDMODEL_FOLDER = os.path.join(staging_folder,'saved_models')



def keras_to_tflite(file_path):
    model = tf.keras.models.load_model(file_path)
    filename = os.path.basename(file_path)
    filename_base = os.path.splitext(filename)[0]
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    output_file = os.path.join(OUTPUT_FOLDER, filename_base + '.tflite')
    with open(output_file, 'wb') as f:
        f.write(tflite_model)
    print(output_file)



def tensorflow_to_tflite(file_path):
    filename = os.path.basename(file_path)
    saved_model_path = os.path.join(SAVEDMODEL_FOLDER, filename+'_saved_model')
    print("###################")
    print(saved_model_path)
    print("###################")
    os.rename(file_path, saved_model_path)
    has_saved_model = tf.saved_model.contains_saved_model(saved_model_path)
    if has_saved_model:
        print("saved modol exists")
        converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)
        tflite_model = converter.convert()
        output_file = os.path.join(OUTPUT_FOLDER, filename + '.tflite')
        with open(output_file, 'wb') as f:
            f.write(tflite_model)
        print(output_file)
    else:
        print("saved model does not exist")


def pytorch_to_tflite(file_path):
    dirname = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    filename_base = os.path.splitext(filename)[0]
    # if file_path.endswith('.pkl'):
    #     pytorch_model = torch.load(file_path)
    #     args = torch.autograd.Variable(torch.FloatTensor(32, 128, 9))
    #     onnx_file_path = os.path.join(dirname, filename_base + '.onnx')
    #     torch.onnx.export(pytorch_model, args, 
    #     f=onnx_file_path, 
    #     verbose=False, 
    #     export_params=True,
    #     do_constant_folding=False,
    #     input_names=['input'],
    #     output_names=['output']
    #     )
    onnx_model = onnx.load(file_path)
    tf_rep = onnx_tf.backend.prepare(onnx_model)
    saved_model_path = os.path.join(SAVEDMODEL_FOLDER, filename_base + '_saved_model')
    tf_rep.export_graph(saved_model_path)
    has_saved_model = tf.saved_model.contains_saved_model(saved_model_path)
    if has_saved_model:
        converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)
        tflite_model = converter.convert()
        output_file = os.path.join(OUTPUT_FOLDER, filename_base + '.tflite')
        with open(output_file, 'wb') as f:
                f.write(tflite_model)
                print(output_file)
    else:
        print("saved model does not exist")