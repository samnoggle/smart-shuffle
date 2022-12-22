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
newData = pd.DataFrame(columns=['euclidLastPlay', 'euclidLastSkip', 'manLastPlay', 'manLastSkip',
                  'eucAvPlay', 'eucAvSkip', 'angleAvPlay', 'angleAvSkip', 'prevSongSkipped', 'neighborSkipped'])


# going through each session
start = time.time()
for i, session in enumerate(sessions):
    # make a session object
    current = s.Session(session)

    # calculate metrics (predicting final song in session)
    # what if one of the lists is empty? they skipped all/listened to all?

    metrics = {}
    finalSong = current.userTracks[-1]

    # get all those variables
    if current.skipped:
        euclidLastSkip = m.euclidian(finalSong, current.skipped[-1])
        manLastSkip = m.manhattan(finalSong, current.skipped[-1])
        avSkipped = m.averageTracks(current.skipped)
        eucAvSkip = m.euclidian(finalSong, avSkipped)
        angleAvSkip = m.angle_between(finalSong, avSkipped)
    else:
        euclidLastSkip = -1
        manLastSkip = -1
        eucAvSkip = -1
        angleAvSkip = -1

    if current.nonSkipped:
        euclidLastPlay = m.euclidian(finalSong, current.nonSkipped[-1])
        manLastPlay = m.manhattan(finalSong, current.nonSkipped[-1])
        avPlayed = m.averageTracks(current.nonSkipped)
        eucAvPlay = m.euclidian(finalSong, avPlayed)
        angleAvPlay = m.angle_between(finalSong, avPlayed)
    else:
        euclidLastPlay = -1
        manLastPlay = -1
        eucAvPlay = -1
        angleAvPlay = -1

    prevSongSkipped = current.isPrevSongSkipped(len(current.userTracks) - 1)

    neighborSkipped = m.is_neighbor_skipped(
        finalSong, current.skipped, current.nonSkipped)

    # 0 euclidian from last played
    metrics['euclidLastPlay'] = euclidLastPlay

    # 1 euclidian from last skipped
    metrics['euclidLastSkip'] = euclidLastSkip

    # 2 manhattan from last played
    metrics['manLastPlay'] = manLastPlay

    # 3 manhattan from last skipped
    metrics['manLastSkip'] = manLastSkip

    # 4 euclidian from averaged played vector
    metrics['eucAvPlay'] = eucAvPlay

    # 5 euclidian from averaged skipped vector
    metrics['eucAvSkip'] =- eucAvSkip

    # 6 angle with averaged played vector
    metrics['angleAvPlay'] = angleAvPlay

    # 7 angle with averaged skipped vector
    metrics['angleAvSkip'] = angleAvSkip

    # 8 is the prev song skipped?
    metrics['prevSongSkipped'] = prevSongSkipped

    # 9 is the nearest neighbor skipped?
    metrics['neighborSkipped'] = neighborSkipped


    # Get the context of the session and add these features to the dictionary
    # NEVERMIND THIS PART. CONTEXT IS NOT ALLOWED TO BE KNOWN WHEN PREDICTING
    # ONLY KEEP THE SESSION ID HERE AND NOT SKIPPED TO CLASSIFY

    r = current.contextMatrix.iloc[-1:]
    index = r.index
    context = r.to_dict('index')

    # Turns into nested dict with the index, remove that
    context = context[index.start]

    # # Irrelevant context data (may change)
    # # Will keep the session ID, but need to remove for tree
    # del context['skip_1']
    # del context['skip_2']
    # del context['skip_3']
    # del context['track_id_clean']

    context = {'session_id': context['session_id'],
               'not_skipped': context['not_skipped']}

    # merge the context and the metrics
    dictData = context | metrics


    # make a row for the decision tree (song context, all metrics, and if it was skipped or not)
    newData = newData.append(dictData, ignore_index=True)


# Spit it out to a csv
newData.to_csv('lastSongMetrics.csv', index=False)


end = time.time()
t = end - start

print("Calculating metrics for {0} sessions took {1} seconds".format(
    len(sessions), t))
