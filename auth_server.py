#!/usr/bin/env python3

from flask import Flask, redirect, request
import requests as req
import json

#This flask script prompts the user for authentication and stores the access token locally
#NOTE: THIS IS A VERY BAD IDEA FOR SECURITY

app = Flask(__name__)

client_creds = {}

#check if credentials exist
with open('client_creds.json', 'r') as f:
    if f:
        client_creds = json.load(f)
        
    else:
        print('The client credentials file does not exist. Client_id and client_secret are necessary for authentication. Creating file now. Client_id and client_secret are available in your Clio account settings.')
        file = open('client_creds.json', 'x')
        file.close()
        exit()
     
client_id = client_creds['client_id']
client_secret = client_creds['client_secret']
redirect_uri = client_creds['redirect_uri']

@app.route("/")
def get_auth():
    auth_url = f"https://app.clio.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"

    return redirect(auth_url)

@app.route("/auth_callback")
def handle_callback():
    auth_code = request.args.get("code")

    global access_token

    #exchange auth code for access token
    #https://docs.developers.clio.com/api-docs/authorization/#step-2-exchange-the-authorization-code-for-an-access_token

    token_data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = req.post("https://app.clio.com/oauth/token", data=token_data, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        access_token = response_json["access_token"]
        client_creds['access_token'] = access_token
        with open('client_creds.json', 'w') as f:
            json.dump(client_creds, f)
    else:
        return "Token exchange failed"
  
    return f"Authorization code: {auth_code},\n Access token: {access_token}"


#refresh access token
def refresh():
    token_data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = req.get("https://app.clio.com/oauth/token", data=token_data, headers=headers)

    if response.status_code == 200:
        json = response.json()
        access_token = json["access_token"]
    else:
        print("Token refresh failed with status code: " +str(response.status_code))
        # print(response.text)
    

# Send a POST request to create a new matter
# response = requests.post("https://app.clio.com/api/v4/matters", json=matter_data, headers=headers)
