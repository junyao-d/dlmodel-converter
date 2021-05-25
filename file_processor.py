import os
from pathlib import Path



def get_unconverted_models(path):
    file_path = []
    file_list = os.listdir(path)
    print(file_list)
    for file in file_list:
        filepath = os.path.join(path,file)
        file_path.append(filepath)
    print(file_path)
    return file_path


def model_type_detection(file_path):
    model_type = 'unknown'
    if os.path.isfile(file_path):
        if file_path.endswith('.h5'):
            model_type = 'keras'
        elif file_path.endswith('.onnx'):
            model_type = 'pytorch'
    else:
        saved_model = Path(file_path+'/saved_model.pb')
        variables = Path(file_path+'/variables')
        if saved_model.exists() and variables.exists():
            model_type = 'tensorflow'

    print('This is a ' + model_type + ' model')
    return model_type

# Test
unconverted_model_location = './unconverted_models/'
file_paths = get_unconverted_models(unconverted_model_location)
for file_path in file_paths:
    model_type_detection(file_path)