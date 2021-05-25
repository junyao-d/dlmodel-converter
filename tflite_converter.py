import tensorflow as tf
import os

saved_models = './saved_models/'
output_path = './tflite_models/'

def keras_to_tflite(file_path):
    model = tf.keras.models.load_model(file_path)
    filename = os.path.basename(file_path)
    filename_base = os.path.splitext(filename)[0]
    saved_model_path = os.path.join(saved_models, filename_base+'_saved_model')
    tf.keras.models.save_model(model, saved_model_path)
    has_saved_model = tf.saved_model.contains_saved_model(saved_model_path)
    if has_saved_model:
        print("saved modol exists")
    print(saved_model_path)
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)
    tflite_model = converter.convert()
    output_file = output_path + filename_base + '.tflite'
    with open(output_file, 'wb') as f:
        f.write(tflite_model)
    print(output_file)

# Test    
keras_to_tflite('./unconverted_models/CNN_Keras.h5')