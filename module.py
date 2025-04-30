# This module will serve to interface with the Spotify web API through python's requests library.
from dotenv import load_dotenv
import os
import json
import requests

# --------------- CONSTANTS ----------------
base_url = "https://api.spotify.com"
accessToken = ""

# --------------- CLASSES ------------------
# These are mostly faithful to the object models in the Spotify API, but omit some of the details that I, frankly, didn't believe anyone would need.
# Feel free to modify the code if for whatever reason you need to know what market songs are available in or whatever.
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

class Track:
    def __init__(self, album, artists, duration, explicit, url, id, name, popularity, uri, is_local):
        self.name = name
        self.id = id
        self.url = url
        self.duration = duration
        self.album = album
        self.artists = artists
        self.explicit = explicit
        self.popularity = popularity # a special value defined by Spotify that takes into account play density and recency.
        self.uri = uri
        self.is_local = is_local
    def __str__(self):
        return f"Name: {self.name}\nArtists: {self.artists}\nAlbum: {self.album}"
# --------------- EXCEPTIONS ------------------
class IncompatibleTypeError(Exception):
    def __init__(self, type, msg="Type must be tracks, artists, albums, playlists, shows, episodes, or audiobooks."):
        self.type = type
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'{self.type} -> {self.msg}'
    
class ItemNotFoundError(Exception):
    def __init__(self, type, msg="The requested item was searched for and not found."):
        self.type = type
        self.msg = msg
        super().__init__(self.msg)

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

def searchForItem(query, itemType):
    # Searches the Spotify library for any kind of item. Must provide query (which can include filters) and the type of object desired.
    # NOTE: for efficiency, this is going to be a strict search where values must match as exactly as possible.
    availableTypes = ["tracks", "artists", "albums", "playlists", "shows", "episodes", "audiobooks"]
    if itemType not in availableTypes:
        raise IncompatibleTypeError(itemType)
    searchURL = f"{base_url}/v1/search?q={query}&limit=1&type={itemType}"
    searchResponse = requests.get(searchURL, headers = {"Authorization" : "Bearer " + accessToken})
    if (searchResponse.ok):
        searchJSON = searchResponse.json()
        match itemType:
            case "tracks":
                if (searchJSON["tracks"]["total"] == 0):
                    raise ItemNotFoundError
                elif searchJSON["tracks"]["items"][0]["name"] == query:
                    return parseTrack(searchJSON["tracks"]["items"][0])
                else:
                    raise ItemNotFoundError
            case "artists":
                if (searchJSON["artists"]["total"] == 0):
                    raise ItemNotFoundError
                elif searchJSON["artists"]["items"][0]["name"] == query:
                    return parseArtist(searchJSON["artists"]["items"][0])
                else:
                    raise ItemNotFoundError
            case "albums":
                if (searchJSON["albums"]["total"] == 0):
                    raise ItemNotFoundError
                elif searchJSON["albums"]["items"][0]["name"] == query:
                    #TODO: update with implemented parseAlbum function
                    # return parseAlbum(searchJSON["albums"]["items"][0])
                    return 0
                else:
                    raise ItemNotFoundError
            case "playlists":
                if (searchJSON["playlists"]["total"] == 0):
                    raise ItemNotFoundError
                elif searchJSON["playlists"]["items"][0]["name"] == query:
                    return parsePlaylist(searchJSON["playlists"]["items"][0])
                else:
                    raise ItemNotFoundError 
            case "shows":
                if (searchJSON["shows"]["total"] == 0):
                    raise ItemNotFoundError
                elif searchJSON["shows"]["items"][0]["name"] == query:
                    #TODO: update with implemented parseShow function (why? idk.)
                    #return parseShow()
                    return 0
                else:
                    raise ItemNotFoundError
            case "episodes":
                if (searchJSON["episodes"]["total"] == 0):
                    raise ItemNotFoundError
                elif searchJSON["episodes"]["items"][0]["name"] == query:
                    #TODO: update with implemented parseEpisode function
                    #return parseEpisode(searchJSON["episodes"]["items"][0])
                    return 0
                else:
                    raise ItemNotFoundError
            case "audiobooks":
                if (searchJSON["audiobooks"]["total"] == 0):
                    raise ItemNotFoundError
                elif searchJSON["audiobooks"]["items"][0]["name"] == query:
                    # TODO: update with implemented parseAudiobook function
                    return 0
                else:
                    raise ItemNotFoundError
                

# --------------- HELPER METHODS -----------
def getArtistByName(artistName):
    # returns a new Artist object from the name of the artist. Process is to first search for the artist by name, then use the ID to get the artist object.
    try:
        return searchForItem(artistName, "artists")
    except ItemNotFoundError:
        print("Could not find artist.")
        return 0

    

def parseArtist(jsonData):
    #returns a new Artist object created with artist JSON data.
    name = jsonData["name"]
    id = jsonData["id"]
    spotify_url = jsonData["external_urls"]["spotify"]
    followers = jsonData["followers"]["total"]
    genres = jsonData["genres"]
    spotify_uri = jsonData["uri"]
    return Artist(name, id, spotify_url, followers, genres, spotify_uri)

def parseTrack(jsonData):
    #returns a new Track object created with track JSON data.
    name = jsonData["name"]
    artists = []
    for entry in jsonData["artists"]:
        artists.append(entry["name"])
    duration = jsonData["duration_ms"]
    album = jsonData["album"]["name"]
    explicit = jsonData["explicit"]
    popularity = jsonData["popularity"]
    uri = jsonData["uri"]
    is_local = jsonData["is_local"]
    url = jsonData["external_urls"]["spotify"]
    id = jsonData["id"]
    return Track(album, artists, duration, explicit, url, id, name, popularity, uri, is_local)

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


