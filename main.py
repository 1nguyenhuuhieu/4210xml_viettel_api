import configparser
import requests

from pathlib import Path
import os

import datetime
config = configparser.ConfigParser()
config.read('config.conf')

user = config['AUTH']['Username']
pwd = config['AUTH']['Password']


data_get_token = {
    'username': user,
    'password': pwd
}


get_token_url = config['URL']['LoginURL']
upload_xml_url = config['URL']['UploadURL']

directory_upload = config['DICRECTORY']['Folder4210']
log_directory = config['DICRECTORY']['Logs']

def rename_file(file_path):
    file = Path(file_path)
    file.rename(file.with_suffix('.xml'))

def rename_files_directory(directory):
    for filename in os.listdir(directory):
        extension = os.path.splitext(filename)[1]
        if extension == ".XML":
            file_path = directory + '/' + filename
            rename_file(file_path)

def get_token_request(url, data):
    headers= {
    "Content-Type":"application/json"
    }
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        access_token = response_json['data']['access_token']
        return access_token
    else:
        return False


def write_log(data):
    timestamp = datetime.datetime.now()
    timestamp = '{:%b_%d_%Y}'.format(timestamp)
    file_path = log_directory + "/" + timestamp + '.txt'
    log_file = open(file_path, 'a+')
    log_file.write(data + "/n")



def uploadxml_request(url, token, file_path):
    authorization = "Bearer " + token
    file = open(file_path, 'rb')
    files = {'file': file}
    headers = {
        "Content-Type": "multipart/form-data",
        "Authorization": authorization
    }

    response = requests.post(url, files=files, headers=headers)
    file.close()
    write_log(response.text)
    print(response.status_code)
    if response.status_code == 200:
        os.remove(file_path)
    else:
        print('RRR')

access_token = get_token_request(get_token_url, data_get_token )


rename_files_directory(directory_upload)

def uploadxml_Directory(directory):
    for filename in os.listdir(directory):
        file_path = directory + '/' + filename
        uploadxml_request(upload_xml_url, access_token, file_path)

uploadxml_Directory(directory_upload)
