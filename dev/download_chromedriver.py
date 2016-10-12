#!/usr/bin/env python

import os
import requests
import zipfile

DESTINATION_DIR=os.path.join(os.path.dirname(os.path.realpath(__file__)),'files')
DOWNLOAD_URL ="http://chromedriver.storage.googleapis.com"
MAC_DRIVER_NAME='chromedriver_mac64.zip'

if not os.path.exists(DESTINATION_DIR):
    os.mkdir(DESTINATION_DIR)

def get_chromedriver_latest_version():
    url = DOWNLOAD_URL + '/LATEST_RELEASE'
    return str(requests.get(url).content.strip()).replace("'",'')[1:]

def download(version='LATEST'):
    if version == 'LATEST':
        download_version = get_chromedriver_latest_version()
    else:
        download_version = version
    latest_path = "%s/%s/%s" % ( DOWNLOAD_URL, download_version, MAC_DRIVER_NAME)
    destination_file_path = os.path.join(DESTINATION_DIR, MAC_DRIVER_NAME)
    destination_unzip_path = os.path.join(DESTINATION_DIR, 'chromedriver')
    with open(destination_file_path, 'wb') as f:
        for chunk in requests.get(latest_path, stream=True).iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    with zipfile.ZipFile(destination_file_path,'r') as f:
        with open(destination_unzip_path,'wb') as d:
            d.write(f.read('chromedriver'))
    return destination_file_path


if __name__ == '__main__':
    print(download())
