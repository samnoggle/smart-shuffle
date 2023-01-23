"""
    Generates a new dataset.
    Each record contains session context about the final track in
    a session, distance metrics between it and the session history, and 
    whether or not that song was skipped (for training)
"""

import preprocessing as p
import session as s
import metrics as m
import time
import pandas as pd

# grabbing the data
p.loadTracks()
sessions = p.loadSessionContext()

# initialize dataframe
newData = pd.DataFrame(columns=['session_id', 'not_skipped'])


# going through each session
start = time.time()
for i, session in enumerate(sessions):
    # make a session object
    current = s.Session(session)

    finalSong = current.userTracks[-1]

    # Only useful metadata right now is the session id and skipped category
    r = current.contextMatrix.iloc[-1:]
    index = r.index
    context = r.to_dict('index')
    context = context[index.start]
    context = {'session_id': context['session_id'],
               'not_skipped': context['not_skipped']}

    print(finalSong)

    # Rebuilding the dataframe of track's features
    # SO UGLY 
    trackFeatures = {'duration': finalSong[0], 'release_year': finalSong[1], 'us_popularity_estimate': finalSong[2], 'acousticness': finalSong[3], 'beat_strength': finalSong[4], 'bounciness': finalSong[5], 'danceability': finalSong[6], 'dyn_range_mean': finalSong[7], 'energy': finalSong[8], 'flatness': finalSong[9], 'instrumentalness': finalSong[10], 'key': finalSong[11], 'liveness': finalSong[12], 'loudness': finalSong[13], 'mechanism': finalSong[14],
                     'mode': finalSong[15], 'organism': finalSong[16], 'speechiness': finalSong[17], 'tempo': finalSong[18], 'time_signature': finalSong[19], 'valence': finalSong[20], 'acoustic_vector_0': finalSong[21], 'acoustic_vector_1': finalSong[22], 'acoustic_vector_2': finalSong[23], 'acoustic_vector_3': finalSong[24], 'acoustic_vector_4': finalSong[25], 'acoustic_vector_5': finalSong[26], 'acoustic_vector_6': finalSong[27], 'acoustic_vector_7': finalSong[28]}

    # merge the context and the metrics
    dictData = context | trackFeatures

    # make a row for the decision tree (song context, all metrics, and if it was skipped or not)
    newData = newData.append(dictData, ignore_index=True)


# Spit it out to a csv
newData.to_csv('lastSongOnlyTF.csv', index=False)


end = time.time()
t = end - start

print("Calculating metrics for {0} sessions took {1} seconds".format(
    len(sessions), t))
