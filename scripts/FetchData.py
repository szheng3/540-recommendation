import os
import zipfile

import requests


def fetchFiles():
    if not os.path.isfile("./data/recipes.csv"):
        # Download the file from S3 using requests library
        local_file_path = os.path.join(os.getcwd(), 'data.zip')
        response = requests.get("https://szdataset.s3.us-east-2.amazonaws.com/data.zip")
        with open(local_file_path, 'wb') as f:
            f.write(response.content)
        # Unzip the file
        with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
        os.remove(local_file_path)