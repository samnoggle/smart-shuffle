"""
Creates a matrix of preprocessed data, normalized with minmax
Also has a list of the track IDs mapped for the matrix's rows
"""
import pandas as pd
import time
import session as s
import glob
import os


def loadTracks():
    """
    Creates a numpy array of every track from the dataset
    (with a list of track ids for mapping)
    """    

    start = time.time()

    # Load in the track features dataset
    tracks = pd.read_csv("../track_features/tf_000000000000.csv")

    # Turn "mode" into int value
    tracks['mode'] = tracks['mode'].str.replace('major', '1')
    tracks['mode'] = tracks['mode'].str.replace('minor', '0')

    tracks["mode"] = tracks["mode"].astype(int)

    # initialize it as a global dataset (for dataset creation)
    s.trackData = tracks.copy()

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


def loadCompleteSessionContext(csvfile):
    """
    Loads in one csv and grabs all of the COMPLETE sessions
    

    :return: a list of dataframes (complete sessions)
    """

    start = time.time()

    sessions = []

    # Load the mini session dataset
    # data = pd.read_csv("raw_data/log_mini.csv")


    try:
        data = pd.read_csv(csvfile, dtype={'session_id': str, 'session_position': int, 'session_length': int, 'track_id_clean': str, 'skip_1': str, 'skip_2': str, 'skip_3': str, 'not_skipped': bool, 'context_switch': str, 'no_pause_before_play': str, 'short_pause_before_play': str,
                    'long_pause_before_play': str, 'hist_user_behavior_n_seekfwd': str, 'hist_user_behavior_n_seekback': str, 'hist_user_behavior_is_shuffle': bool, 'hour_of_day': int, 'date': str, 'premium': bool, 'context_type': str, 'hist_user_behavior_reason_start': str, 'hist_user_behavior_reason_end': str})
    except ValueError:
        print("ValueError: {0}".format(csvfile))

    # Remove the metadata
    # Keep: hour of day, date, premium
    data.drop(columns=['skip_1','skip_2','skip_3','context_switch','no_pause_before_play','short_pause_before_play','long_pause_before_play','hist_user_behavior_n_seekfwd','hist_user_behavior_n_seekback','hist_user_behavior_is_shuffle', 'context_type','hist_user_behavior_reason_start','hist_user_behavior_reason_end'], inplace=True)


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

def loadFinalTracks():
    """
    Loads the final track dataset

    :return: a dataframe of final rows
    """

    # Load the finalSong dataset
    data = pd.read_csv("split_data/final_row0.csv")

    return data

def loadSession():
    """
    Loads the incomplete session dataset

    :return: a list of dataframes (sessions w/o final song)
    """
    sessions = []
    start = time.time()

    data = pd.read_csv("split_data/clean_sessions0.csv")

    entries = data['session_length'].iloc[0]
    entries -= 1 # its one less because the final song is missing here
    position = 0

    while(position + entries < len(data.index)):

        # Make them into a subset dataset
        subset = data[position: position + entries]

        # Update to continue
        position = position + entries
        entries = data['session_length'].iloc[position]
        entries -= 1 # adjust for final song again

        # Append the session to a list of dataframes
        sessions.append(subset)
        
    end = time.time()
    t = end - start
    print("Loading {0} sessions took {1} seconds".format(len(sessions), t))

    return sessions


def splitDataset():

    sessionData = pd.DataFrame()
    finalRowData = pd.DataFrame()

    # the path to your csv file directory
    mycsvdir = '../new_data/training_set'

    # get all the csv files in that directory (assuming they have the extension .csv)
    csvfiles = glob.glob(os.path.join(mycsvdir, '*.csv'))

    for i, csvfile in enumerate(csvfiles):

        sessions = loadCompleteSessionContext(csvfile)

        # Remove the last row of each session
        # Put that last row into a separate structure
        for session in sessions:
            # Extract the final song in a session 
            finalRow = session.tail(1)
            
            # TAKEN OUT AND THEN REMOVED FROM CONTEXT MATRIX
            session.drop(index=session.index[-1],axis=0,inplace=True)

            sessionData = pd.concat([sessionData, session])
            finalRowData = pd.concat([finalRowData, finalRow])

        print(sessionData)

        sessionPath = "split_data/clean_sessions{0}.csv".format(i)
        finalRowPath = "split_data/final_row{0}.csv".format(i)

        # Spit it out to a csv
        sessionData.to_csv(sessionPath, index=False)
        finalRowData.to_csv(finalRowPath, index=False)



############## DRIVER CODE #################
def main():
    splitDataset()


# Calling main function
if __name__ == "__main__":
    main()


