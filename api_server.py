import os
from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import zipfile
import main
import file_processor as fp
import requests


app = Flask(__name__)
pwd = os.path.dirname(__file__)
staging_folder = os.path.join(pwd, 'model_file_staging')
print(pwd)

UPLOAD_FOLDER = os.path.join(staging_folder, 'uploaded_files')
PROCESS_FOLDER = os.path.join(staging_folder, 'unconverted_models')
OUTPUT_FOLDER = os.path.join(staging_folder, 'output_models')
SAVEDMODEL_FOLDER = os.path.join(staging_folder, 'saved_models')
ALLOWED_EXTENSIONS = {'zip', 'h5', 'onnx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
SAMPLE_FOLDER = os.path.join(pwd, 'samples')

HOST = "0.0.0.0"
PORT = 80


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    """
    Check file type
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/convert', methods=['GET', 'POST'])
def upload_and_convert_file():

    fp.clean_folder(UPLOAD_FOLDER)
    fp.clean_folder(PROCESS_FOLDER)
    fp.clean_folder(OUTPUT_FOLDER)
    fp.clean_folder(SAVEDMODEL_FOLDER)
    file_url = request.args.get('url')
    sample_file = request.args.get('filename')
    if file_url is not None:
        source_file_request = requests.get(file_url, allow_redirects=True)
        filename = file_url.split("/")[-1]
        if allowed_file(filename):
            file_init_loc = os.path.join(UPLOAD_FOLDER, filename)
            open(file_init_loc, 'wb').write(source_file_request.content)

            if filename.endswith('zip'):
                with zipfile.ZipFile(file_init_loc, 'r') as zip_ref:
                    zip_ref.extractall(PROCESS_FOLDER)
            else:
                os.rename(file_init_loc, os.path.join(PROCESS_FOLDER, filename))
            #os.system('python main.py')
            main.conversion(PROCESS_FOLDER)
            filename_base = os.path.splitext(filename)[0]
            output_filename = filename_base+'.tflite'
            file_path = os.path.join(OUTPUT_FOLDER, output_filename)
            # hostname has to be change to the spi public ip / dns
            # 'file uploaded successfully'
            #return f"http://[api_public_ip_or_dns]:{PORT}/download?fileId={output_filename}"
            return send_file(file_path,as_attachment=True)
        return "file uploaded fail, please check file extension or zip file structure"
    elif sample_file is not None:
        filename = sample_file
        file_init_loc = os.path.join(SAMPLE_FOLDER, filename)
        if os.path.exists(file_init_loc):
            os.rename(file_init_loc, os.path.join(PROCESS_FOLDER, filename))
            main.conversion(PROCESS_FOLDER)
            filename_base = os.path.splitext(filename)[0]
            output_filename = filename_base+'.tflite'
            file_path = os.path.join(OUTPUT_FOLDER, output_filename)
            return send_file(file_path,as_attachment=True)
        else:
            return "Sample file does not exist"
    else:
        return "url does not exist or fail to request file"

###############################
# Following is for ui demo only 
###############################
@app.route('/demo', methods=['GET', 'POST'])
def demo_convert_file():

    fp.clean_folder(UPLOAD_FOLDER)
    fp.clean_folder(PROCESS_FOLDER)
    fp.clean_folder(OUTPUT_FOLDER)
    fp.clean_folder(SAVEDMODEL_FOLDER)

    if 'file' not in request.files:
        return "No files are uploaded"
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_init_loc = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_init_loc)

        if filename.endswith('zip'):
            with zipfile.ZipFile(file_init_loc, 'r') as zip_ref:
                zip_ref.extractall(PROCESS_FOLDER)
        else:
            os.rename(file_init_loc, os.path.join(PROCESS_FOLDER, filename))
        #os.system('python main.py')
        main.conversion(PROCESS_FOLDER)
        filename_base = os.path.splitext(filename)[0]
        output_filename = filename_base+'.tflite'
        file_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # hostname has to be change to the spi public ip / dns
        # 'file uploaded successfully'
        #return f"http://[api_public_ip_or_dns]:{PORT}/download?fileId={output_filename}"
        return send_file(file_path,as_attachment=True)
    return "file uploaded fail, only zip files are accepted"


@app.route("/download")
def download_file():
    file_name = request.args.get('fileId')
    file_path = os.path.join(OUTPUT_FOLDER, file_name)
    if os.path.isfile(file_path):
        # return send_file(file_path,as_attachment=True)
        return send_file(file_path, as_attachment=True)
    else:
        return "The downloaded file does not exist"


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
    # app.run(debug=True)





@app.route("/clear")
def clean_folder():
    fp.clean_folder(UPLOAD_FOLDER)
    fp.clean_folder(PROCESS_FOLDER)
    fp.clean_folder(OUTPUT_FOLDER)
    fp.clean_folder(SAVEDMODEL_FOLDER)
