"""
This space will consist of the ANNOY object and a list of 
track ids that correlate to the space's indices for track look-up
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


# Create the space

# Length of item vector that will be indexed
f = 29  
space = AnnoyIndex(f, 'euclidean')

# Adding vectors into the space w/ randomized values just to test
for i, row in normal_tracks.iterrows():
    rowVect = row.tolist()
    space.add_item(i, rowVect)

# I dont know what this forest of 10 trees is meant to do
space.build(10)  # 10 trees



# Testing out some things

# Save the space?
space.save('test.ann')

# Now you're able to load the space again from the file
u = AnnoyIndex(f, 'euclidean')
u.load('test.ann')  # super fast, will just mmap the file
print(u.get_nns_by_item(0, 1000))  # will find the 1000 nearest neighbors
