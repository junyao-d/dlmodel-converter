import os
import requests

# Get original model file from ontology api
pwd = os.path.dirname(__file__)
source_filename = "anyfilename.h5" 
source_file_path = os.path.join(pwd, source_filename)
# Change the value to your api url
file_source = "your_ontology_api_file_url"
source_file_request = requests.get(f"{file_source}", allow_redirects=True)
open(source_file_path, 'wb').write(source_file_request.content)

# Post the file to converter api
with open(source_file_path,'rb') as file_obj:
        file_dict = {"file":file_obj}
        rsp = requests.post('http://52.63.221.18/convert',files=file_dict)
        print(rsp.text) 
        download_url = rsp.text

# remove the temporary source model file
os.remove(source_file_path)

# Download converted model file from api and name any you want, example just simply extra the filename from url
download_filename = download_url.split("=")[1]
download_request = requests.get(f"{download_url}", allow_redirects=True)
open(download_filename, 'wb').write(download_request.content)


