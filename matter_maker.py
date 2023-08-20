#!/usr/bin/env python3
import sys
import requests as req
import json

#NOTE: a contact ID is also needed to create a matter

def create_matter(matter_data, contact_data, client_creds):

    with open(client_creds, 'r') as client_creds_file:
        client_creds_json = json.load(client_creds_file)
    access_token = client_creds_json['access_token']
    client_id = client_creds_json['client_id']

    matter_data_json = {}
    with open(matter_data, 'r') as matter_data_file:
        matter_data_json = json.load(matter_data_file)

    contact_data_json = {}
    with open(contact_data_json, 'r') as f:
        contact_data_json = json.load(f)
    

    # print('create_matter(): client_creds', endswith="")
    # print(client_creds)

    headers = {
        'Authorization': f'Bearer {access_token}',
        # 'Content-Type': 'application/json'
    }

    contact_response = create_contact(contact_data, client_creds_json)
    contact_json = contact_response.json()
    matter_data_json["data"]["client"]["id"] = contact_json["data"]["id"]
    
    response = req.post('https://app.clio.com/api/v4/matters.json', json=matter_data_json, headers=headers)

    if response.status_code == 201:
        print('Matter successfully created!')
    else:
        print('Matter creation failed with status code: ' + str(response.status_code))
        print(response.text)

    return response.json()

#for now just dicts
def create_contact(contact_data, client_creds):

    access_token = client_creds["access_token"]
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        # 'Content-Type': 'application/json'
    }
    response = req.post('https://app.clio.com/api/v4/contacts.json', json=contact_data, headers=headers)

    return response
    

if __name__ == '__main__':
    create_matter(sys.argv[1], sys.argv[2])
