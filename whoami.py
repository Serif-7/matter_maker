#!/usr/bin/env python3

import requests as req
import json
import sys

#hit whoami endpoint
def whoami(client_creds):

    creds = {}
    
    if type(client_creds) != dict:
        with open(client_creds, 'r') as f:
            creds = json.load(f)
    else:
        creds = client_creds

    access_token = creds['access_token']

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    res = req.get("https://app.clio.com/api/v4/users/who_am_i", headers=headers)

    print(res.text)


if __name__ == '__main__':
    whoami(sys.argv[1])