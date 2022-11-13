"""
Creates a matrix of preprocessed data, normalized with minmax
Also has a list of the track IDs mapped for the matrix's rows
"""
import pandas as pd
from annoy import AnnoyIndex

# Load in the track features dataset
tracks = pd.read_csv("data/tf_mini.csv")

# Turn "mode" into int value
tracks['mode'] = tracks['mode'].str.replace('major', '1')
tracks['mode'] = tracks['mode'].str.replace('minor', '0')

tracks["mode"] = tracks["mode"].astype(int)

# Extract track_id column into a list
trackID = tracks['track_id'].to_list()
tracks.drop('track_id', axis=1, inplace=True)

# Normalize that data!
normal_tracks = tracks.copy()
normal_tracks = (normal_tracks - normal_tracks.min()) / \
    (normal_tracks.max()-normal_tracks.min())

# Now I have a matrix of every song, and a list mapping the track ids

