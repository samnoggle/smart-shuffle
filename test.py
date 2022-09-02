import spotipy
import json
import webbrowser
import os
from dotenv import load_dotenv


load_dotenv('secrets.env')

USER = os.getenv('USERNAME')
C_ID = os.getenv('CLIENT_ID')
C_SECRET = os.getenv('CLIENT_SECRET')
RED_URI = os.getenv('REDIRECT_URI')

# Create OAuth Object
oauth_object = spotipy.SpotifyOAuth(C_ID, C_SECRET, RED_URI)

# Create token
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']

# Create Spotify Object
spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()

# To print the response in readable format.
print(json.dumps(user, sort_keys=True, indent=4))

# Can only do 50 at a time, will need to loop through and do multiple calls to get everything
likes = spotifyObject.current_user_saved_tracks(20, 0, 'US')
print(json.dumps(likes ,sort_keys=True, indent=4))

while likes:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + likes['offset'], likes['uri'],  likes['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None