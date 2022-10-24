"""
This space will consist of the ANNOY object and a list of 
track ids that correlate to the space's indices for track look-up
"""
import pandas as pd
from annoy import AnnoyIndex
import random

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


# Create a list of vectors with the track features

# Create the space and add each vector inside









f = 29  # Length of item vector that will be indexed

t = AnnoyIndex(f, 'euclidean')

# Adding vectors into the space w/ randomized values just to test
for i in range(1000):
    v = [random.gauss(0, 1) for z in range(f)]
    t.add_item(i, v)

# I dont know what this forest of 10 trees is meant to do
t.build(10)  # 10 trees

# Save the space?
t.save('test.ann')

# Now you're able to load the space again from the file
u = AnnoyIndex(f, 'angular')
u.load('test.ann')  # super fast, will just mmap the file
print(u.get_nns_by_item(0, 1000))  # will find the 1000 nearest neighbors
