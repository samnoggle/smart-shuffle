import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

scope = "user-library-read, user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# This prints the name of every one of their liked songs, could save this to a data structure 
likes = sp.current_user_saved_tracks(20, 0, 'US')
print(json.dumps(likes, sort_keys=True, indent=4))

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


#Need methods to play, pause, and skip playback
# make a class object? No. pass that sp object to each one!
