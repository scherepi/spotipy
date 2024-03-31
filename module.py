# This module will serve to interface with the Spotify web API through python's requests library.
from dotenv import load_dotenv
import os
import json
import requests

# --------------- CONSTANTS ----------------
base_url = "https://api.spotify.com"
accessToken = ""

# --------------- CLASSES ------------------
class Artist:
    def __init__(self, name, id, spotify_url, followers, genres, spotify_uri):
        self.name = name
        self.id = id
        self.spotify_url = spotify_url
        self.followers = followers
        self.genres = genres
        self.spotify_uri = spotify_uri
    def __str__(self):
        return f"Artist: {self.name}\nID: {self.id}\nFollowers: {self.folowers}"
        

# --------------- API METHODS ------------------
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
            return accessToken
        else:
            print("Action failed at access token request. Printing response:")
            print(accessTokenResponse.text)
            return "error"
        #accessToken = json.loads(accessTokenResponse)["access_token"]
    except Exception as e:
        print(e)


def getArtistById(artistID):
    urlToGet = base_url + "/v1/artists/" + artistID
    artistResponse = requests.get(urlToGet, headers = {"Authorization" : "Bearer " + accessToken})
    if (artistResponse.ok):
        artistJSON = artistResponse.json()
        return parseArtist(artistJSON)
    else:
        print("action failed at artist request. Printing response:")
        print(artistResponse.text)

def getPlaylist(playlistID):
    urlToGet = base_url + "/v1/playlists/" + playlistID
    playlistResponse = requests.get(urlToGet, headers = {"Authorization" : "Bearer " + accessToken})
    if (playlistResponse.ok):
        playlistJSON = playlistResponse.json()
        parsePlaylist(playlistJSON)
    else:
        print("action failed at playlist request. printing response:")
        print(playlistResponse.text)

# --------------- HELPER METHODS -----------
def getArtistByName():
    return

def parseArtist(jsonData):
    #returns a new Artist object created with artist JSON data.
    name = jsonData["name"]
    id = jsonData["id"]
    spotify_url = jsonData["external_urls"]["spotify"]
    followers = jsonData["followers"]["total"]
    genres = jsonData["genres"]
    spotify_uri = jsonData["uri"]
    return Artist(name, id, spotify_url, followers, genres, spotify_uri)

def parsePlaylist(jsonData):
    name = jsonData["name"]
    id = jsonData["id"]
    limit = jsonData["tracks"]["limit"]
    print("limit: " + str(limit))
    ownerName = jsonData["owner"]["display_name"]
    playlist_tracks = jsonData["tracks"]["items"]
    # let's just get the track names for now:
    names = []
    for track in playlist_tracks:
        names.append(track["track"]["name"])
    print(name + " by " + ownerName + "[" + id + "]")
    for name in names:
        print(name)


# --------------- TESTING ------------------
accessToken = generateToken()
print("token generated... token value: " + accessToken)
artistID = "4Z8W4fKeB5YxbusRsdQVPb"
print("getting artist info for id " + artistID)
radiohead = getArtistById(artistID)
print(radiohead.followers)
getPlaylist("10PyPsED8W8ocJhbUTCbHy")


