# This module will serve to interface with the Spotify web API through python's requests library.
from dotenv import load_dotenv
import os
import json
import requests

# --------------- CONSTANTS ----------------
base_url = "https://api.spotify.com"
accessToken = ""
# first thing's first, let's get our token!
def generateToken():
    try:
        load_dotenv()
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        accessRequestData = {
            "grant_type": "client_credentials",
            "client_id" : client_id,
            "client_secret" : client_secret
        }
        accessTokenResponse = requests.post("https://accounts.spotify.com/api/token", headers = {'Content-Type': 'application/x-www-form-urlencoded'}, data = accessRequestData)
        if (accessTokenResponse.ok):
            accessToken = accessTokenResponse.json()["access_token"]
        else:
            print("Action failed at access token request. Printing response:")
            print(accessTokenResponse.text)
        #accessToken = json.loads(accessTokenResponse)["access_token"]
    except Exception as e:
        print(e)


def getArtist(artistID):
    urlToGet = base_url + "/v1/artists/" + artistID
    artistResponse = requests.get(urlToGet, headers = {"Authorization" : "Bearer " + accessToken})
    print(artistResponse.text)
    """if (artistResponse.ok):
        for key in artistResponse.json():
            print(key + " : " + artistResponse[key])
    else:
        print("action failed at artist request. Printing response:")
        print(artistResponse.text)"""
    
# now let's actually generate it...
generateToken()
getArtist("4Z8W4fKeB5YxbusRsdQVPb")