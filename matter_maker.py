#!/usr/bin/env python3
import sys
from typing import BinaryIO
import requests as req
import json

#NOTE: a contact ID is also needed to create a matter

#arguments can be either dicts or strings (file paths)
def create_matter(matter_data, client_creds):

    if type(client_creds) != dict:
        with open(client_creds, 'r') as client_creds_file:
            client_creds_json = json.load(client_creds_file)
    access_token = client_creds_json['access_token']
    client_id = client_creds_json['client_id']

    matter_data_json = {}
    if type(matter_data) != dict:
        with open(matter_data, 'r') as matter_data_file:
            matter_data_json = json.load(matter_data_file)
    matter_data_json['client_id'] = client_id
    

    # print('create_matter(): client_creds', endswith="")
    # print(client_creds)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = req.ppost('https://app.clio.com/api/v4/matters.json', json=matter_data_json, headers=headers)

    if response.status_code == 201:
        print('Matter successfully created!')
    else:
        print('Matter creation failed with status code: ' + str(response.status_code))
        print(response.text)
    

if __name__ == '__main__':
    create_matter(sys.argv[1], sys.argv[2])
