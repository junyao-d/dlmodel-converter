import os
from string import Template
from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import zipfile

app = Flask(__name__)
pwd = os.path.dirname(__file__)
print(pwd)

UPLOAD_FOLDER = os.path.join(pwd,'uploaded_files')
PROCESS_FOLDER = os.path.join(pwd,'unconverted_models')
OUTPUT_FOLDER = os.path.join(pwd,'tflite_models')
ALLOWED_EXTENSIONS = {'zip', 'tar'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


HOST = "0.0.0.0"
PORT = 5000

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    """
    Check file name
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    upload to uploaded_files directory
    requests example:
    with open('path','rb') as file_obj:
        rsp = requests.post('http://localhost:5000/upload,files={'file':file_obj})
        print(rsp.text) --> file uploaded successfully
    """
    os.system('python test.py')
    if 'file' not in request.files:
        return "No files are uploaded"
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_init_loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_init_loc)
        with zipfile.ZipFile(file_init_loc, 'r') as zip_ref:
            zip_ref.extractall(PROCESS_FOLDER)
        os.system('python main.py')

        filename_base = os.path.splitext(file.filename)[0]
        output_filename = filename_base+'.tflite'
        file_path = os.path.join(OUTPUT_FOLDER,output_filename)
        # return f"http://{HOST}:{PORT}/download?fileId={output_filename}"#'file uploaded successfully'
        return send_file(file_path,as_attachment=True)
    return "file uploaded fail, file type may be not accept"


@app.route("/download")
def download_file():
    file_name = request.args.get('fileId')
    file_path = os.path.join(OUTPUT_FOLDER,file_name)
    if os.path.isfile(file_path):
        return send_file(file_path,as_attachment=True)
    else:
        return "The downloaded file does not exist"

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
    #app.run(debug=True)