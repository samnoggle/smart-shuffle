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
    tracks = pd.read_csv("raw_data/tf_mini.csv")

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


def loadCompleteSessionContext():
    """
    Loads in a csv and grabs all of the COMPLETE sessions
    

    :return: a list of dataframes (complete sessions)
    """

    start = time.time()

    sessions = []

    # Load the session dataset
    data = pd.read_csv("raw_data/log_mini.csv")

    # Remove the metadata - needed when using the mini data
    data.drop(columns=['skip_1','skip_2','skip_3','context_switch','no_pause_before_play','short_pause_before_play','long_pause_before_play','hist_user_behavior_n_seekfwd','hist_user_behavior_n_seekback','hist_user_behavior_is_shuffle','hour_of_day','date','premium','context_type','hist_user_behavior_reason_start','hist_user_behavior_reason_end'], inplace=True)


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
    data = pd.read_csv("split_data/final_row.csv")

    return data

def loadSession():
    """
    Loads the incomplete session dataset

    :return: a list of dataframes (sessions w/o final song)
    """
    sessions = []
    data = pd.read_csv("split_data/clean_sessions.csv")

    entries = data['session_length'].iloc[0]
    entries -= 1 # its one less because the final song is missing here
    position = 0

    while(position + entries < len(data.index)):

        # Make them into a subset dataset
        subset = data[position: position + entries]

        # Update to continue
        position = position + entries
        entries = data['session_length'].iloc[position]

        # Append the session to a list of dataframes
        sessions.append(subset)

    return sessions


def splitDataset():

    sessionData = pd.DataFrame()
    finalRowData = pd.DataFrame()

    sessions = loadCompleteSessionContext()

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
    # Spit it out to a csv
    sessionData.to_csv('split_data/clean_sessions.csv', index=False)
    finalRowData.to_csv('split_data/final_row.csv', index=False)



############## DRIVER CODE #################
def main():
    splitDataset()


# Calling main function
if __name__ == "__main__":
    main()


