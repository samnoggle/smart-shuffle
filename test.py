import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json


# load_dotenv('secrets.env')

# USER = os.getenv('USERNAME')
# C_ID = os.getenv('CLIENT_ID')
# C_SECRET = os.getenv('CLIENT_SECRET')
# RED_URI = os.getenv('REDIRECT_URI')

# # Create OAuth Object
# oauth_object = spotipy.SpotifyOAuth(C_ID, C_SECRET, RED_URI)

# # Create token
# token_dict = oauth_object.get_access_token()
# token = token_dict['access_token']

# # Create Spotify Object
# spotifyObject = spotipy.Spotify(auth=token)

# user = spotifyObject.current_user()

# To print the response in readable format.
# print(json.dumps(user, sort_keys=True, indent=4))


scope = "user-library-read, user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# This prints the name of every one of their liked songs, could save this to a data structure 

likes = sp.current_user_saved_tracks(20, 0, 'US')

print(json.dumps(likes ,sort_keys=True, indent=4))

while likes:
    for track in likes['items']:
        # print(track['track']['name'])
        pass
    if likes['next']:
        likes = sp.next(likes)
    else:
        likes = None

# Now try to play some music? 
songs_to_play = ["spotify:track:6Rb0ptOEjBjPPQUlQtQGbL"]

sp.start_playback(uris=songs_to_play)
