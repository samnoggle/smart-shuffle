"""
Creates a matrix of preprocessed data, normalized with minmax
Also has a list of the track IDs mapped for the matrix's rows
"""
import pandas as pd
import time

import session as s


def loadTracks():
    """
    Creates a numpy array of every track from the dataset
    (with a list of track ids for mapping)
    """

    start = time.time()

    # Load in the track features dataset
    tracks = pd.read_csv("data/tf_mini.csv")

    # Turn "mode" into int value
    tracks['mode'] = tracks['mode'].str.replace('major', '1')
    tracks['mode'] = tracks['mode'].str.replace('minor', '0')

    tracks["mode"] = tracks["mode"].astype(int)

    # Extract track_id column into a list
    trackID = tracks['track_id'].to_list()
    tracks.drop('track_id', axis=1, inplace=True)

    # Normalize the data
    # normal_tracks = tracks.copy()
    # normal_tracks = (normal_tracks - normal_tracks.min()) / \
    #     (normal_tracks.max()-normal_tracks.min())

    end = time.time()
    t = end - start
    print("Loading {0} tracks took {1} seconds".format(len(trackID), t))

    # set the public index lists
    s.trackIDs = trackID
    s.tracks = tracks.to_numpy()


def loadSessionContext():

    start = time.time()

    sessions = []

    # Load the session dataset
    data = pd.read_csv("data/log_mini.csv")

    # First session ID and number of rows to start
    entries = data['session_length'].iloc[0]
    position = 0

    while(position + entries < len(data.index)):

        # Make them into a subset dataset
        subset = data[position: position + entries]

        # Update to continue
        position = position + entries
        entries = data['session_length'].iloc[position]

        # Append the session to a list of dataframes
        sessions.append(subset)

    end = time.time()
    t = end - start
    print("Loading {0} sessions took {1} seconds".format(len(sessions), t))

    return sessions
