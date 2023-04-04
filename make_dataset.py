"""
    Generates a new dataset for the decision tree.
    Each record contains session context about the final track in
    a session, distance metrics between it and the session history, and 
    whether or not that song was skipped (for training)
"""

import preprocessing as p
import session as s
import metrics as m
import time
import pandas as pd
import os.path

def export_batch(path, data):
    """
    Prints chunk of data into the specified file

    :param path: The file path to create or append to
    :param data: The data to export
    """

    # turn the last session batch to datatframe
    newData = pd.DataFrame.from_records(data)

    # First check if the file already exists
    if os.path.exists('path'):
        # append to it (dont print column names)
        newData.to_csv(path, mode='a', header=False, index=False)
    else:
        # make it (print the column names)
        newData.to_csv(path, mode='a', index=False)


# grabbing the data
p.loadTracks()
sessions = p.loadSession() # list of dataframes
finalSongs = p.loadFinalTracks() # dataframe of final rows

# make a list of dicts to append them to eachother and convert to a dataframe at the end
listData = []

# going through each session

# lets try printing it out every 500 sessions ??

start = time.time()
for i, session in enumerate(sessions):

    # get the correct final row
    finalRow = finalSongs.loc[finalSongs['session_id'] == session.iloc[0]['session_id']]

    # make a session object
    try:
        current = s.Session(session, finalRow)
    except:
        print("This session was fricked up:")
        print(session)
        print(finalRow.iloc[0]['track_id_clean'])
        continue

    # calculate metrics (predicting final song in session)
    metrics = {}

    # get all those variables
    if current.skipped:
        euclidLastSkip = m.euclidian(current.finalSong, current.skipped[-1])
        manLastSkip = m.manhattan(current.finalSong, current.skipped[-1])
        avSkipped = m.averageTracks(current.skipped)
        eucAvSkip = m.euclidian(current.finalSong, avSkipped)
        angleAvSkip = m.angle_between(current.finalSong, avSkipped)
        manAvSkip = m.manhattan(current.finalSong, avSkipped)
        angleLastSkip = m.angle_between(current.finalSong, current.skipped[-1])
    else:
        euclidLastSkip = -1
        manLastSkip = -1
        eucAvSkip = -1
        angleAvSkip = -1
        manAvSkip = -1
        angleLastSkip = -1

    if current.nonSkipped:
        euclidLastPlay = m.euclidian(current.finalSong, current.nonSkipped[-1])
        manLastPlay = m.manhattan(current.finalSong, current.nonSkipped[-1])
        avPlayed = m.averageTracks(current.nonSkipped)
        eucAvPlay = m.euclidian(current.finalSong, avPlayed)
        angleAvPlay = m.angle_between(current.finalSong, avPlayed)
        manAvPlay = m.manhattan(current.finalSong, avPlayed)
        angleLastPlay = m.angle_between(current.finalSong, current.nonSkipped[-1])

    else:
        euclidLastPlay = -1
        manLastPlay = -1
        eucAvPlay = -1
        angleAvPlay = -1
        manAvPlay = -1
        angleLastPlay = -1

    prevSongPlayed = current.contextMatrix.iloc[-2]['not_skipped']

    neighborSkipped = m.is_neighbor_skipped(
        current.finalSong, current.skipped, current.nonSkipped)

    # # 0 euclidian from last played
    # metrics['euclidLastPlay'] = euclidLastPlay

    # # 1 euclidian from last skipped
    # metrics['euclidLastSkip'] = euclidLastSkip

    # # 2 euclidian from averaged played vector
    # metrics['eucAvPlay'] = eucAvPlay

    # # 3 euclidian from averaged skipped vector
    # metrics['eucAvSkip'] = eucAvSkip

    # 4 manhattan from last played
    metrics['manLastPlay'] = manLastPlay

    # 5 manhattan from last skipped
    metrics['manLastSkip'] = manLastSkip

    # 6 manhattan from average skipped vector
    metrics['manAvSkip'] = manAvSkip

    # 7 manhattan from average played vector
    metrics['manAvPlay'] = manAvPlay

    # #  angle with last played
    # metrics['angleLastPlay'] = angleLastPlay

    # # angle with last skipped
    # metrics['angleLastSkip'] = angleLastSkip

    # # angle with averaged played vector
    # metrics['angleAvPlay'] = angleAvPlay

    # # angle with averaged skipped vector
    # metrics['angleAvSkip'] = angleAvSkip

    # is the prev song skipped?
    metrics['prevSongPlayed'] = prevSongPlayed

    # is the nearest neighbor skipped?
    metrics['neighborSkipped'] = neighborSkipped

    # Tack on if the mini forest thinks it's a skip
    metrics['babyTreeDecision'] = current.babyTreeDecision()[0]

    # Grab the Metadata for the dataset
    percentSkipped = (len(current.skipped) / len(current.userTracks)) * 100
    metadata = {'hour_of_day': current.hourOfDay,
                'day_of_week': current.dayOfWeek,
                'month': current.month,
                'premium': current.premium,
                'percent_skipped': percentSkipped}

    r = current.contextMatrix.iloc[-1:]
    index = r.index
    context = r.to_dict('index')

    # Turns into nested dict with the index, remove that
    context = context[index.start]

    context = {'session_id': context['session_id'],
               'not_skipped': context['not_skipped']}

    # get the original track features of the final track
    finalRowID = finalRow.iloc[0]['track_id_clean']

    # removed inplace = true which i think was removing from the original data. oopsie!!
    # this was making it so songs cant be used twice bc the first time you use it, it
    # removes the ID from the original data hahhahahhhahhahhh oops
    finalTrackFeatures = s.trackData.loc[s.trackData['track_id'] == finalRowID]
    finalTrackFeatures = finalTrackFeatures.drop(columns='track_id')

    features = finalTrackFeatures.to_dict(orient='records')

    # merge the context and the metrics into one dictionary
    dictData = context | metrics | metadata | features[0]

    # make a row for the decision tree (song context, all metrics, and if it was skipped or not)
    listData.append(dictData)


    # TO EXPORT THE BATCHES IN INCREMENTS OF SESSIONS
    if len(listData) == 500:
        export_batch('training_data/lastSongMetricsMiniTree.csv', listData)
        # please release this memory please
        listData = []

# Export the remnant batches
export_batch('training_data/lastSongMetricsMiniTree.csv', listData)

# Time taken
end = time.time()
t = end - start
print("Calculating metrics for {0} sessions took {1} seconds".format(
    len(sessions), t))

# Feature importance of mini forests
mean_importances = s.running_importances / len(sessions)


print(mean_importances)


# Average track length
avTrackLength = sum(s.sessionLengths)/len(s.sessionLengths)
print("Each session on average was {0} tracks long".format(avTrackLength))
