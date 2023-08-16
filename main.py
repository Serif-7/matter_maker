#!/usr/bin/env python3


#NOTES

from flask import Flask, redirect, request
import requests as req

app = Flask(__name__)

#GLOBALS
client_id = "Db47hy8yiZg9DCW9Len2zYFtjOoPWTBJcza0g3Mp"
client_secret = "Bva1VEFlT3rvkNbZkOzWfpGy0HYMuZgkHDUKZrn7"
access_token = ""
refresh_token = ""
redirect_uri = "http://127.0.0.1:5000/auth_callback"

#Set up a pipeline from docassemble later
matter_data = {
    "name": "Matter name - Test",
    "description": "Matter description",
    "client_id": client_id,
    "practice_area_id": "PRACTICE_AREA_ID"
}

@app.route("/")
def get_auth():
    auth_url = f"https://app.clio.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"

    return redirect(auth_url)

@app.route("/auth_callback")
def handle_callback():
    auth_code = request.args.get("code")

    #exchance auth code for access token
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
        json = response.json()
        access_token = json["access_token"]
        #access token acquired, call main function
        main()
    else:
        return "Token exchange failed"
   
    return f"Authorization code: {auth_code},\n Access token: {access_token}"

#create new matter
def main():
    
    refresh()
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = req.post("https://app.clio.com/api/v4/matters", json=matter_data, headers=headers)

    if response.status_code == 201:
        print("Matter successfully created!")
    else:
        print("Matter creation failed with status code: " + str(response.status_code))
        print(response.text)

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
