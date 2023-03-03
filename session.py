"""
    Class to store a session's data
"""
import pandas as pd
import numpy as np
import datetime
from sklearn.ensemble import RandomForestClassifier


# public track index where all track features
# are loaded into
trackIDs = []
tracks = []

# for keeping track of session length on average
sessionLengths = []

trackData = pd.DataFrame()

# Keeping track of the mini forest feature scores
running_importances = np.zeros(29)

class Session:
    def __init__(self, _contextMatrix, _finalRow):

        self.contextMatrix = _contextMatrix
        self.finalRow = _finalRow
        self.sessionID = _contextMatrix.iloc[0]['session_id']

        # metadata
        self.hourOfDay = self.finalRow.iloc[0]['hour_of_day']
        self.date = self.finalRow.iloc[0]['date']
        self.dayOfWeek = self.getDayOfWeek()
        self.month = self.getMonth()
        self.premium = self.finalRow.iloc[0]['premium']

        # The answer, only used for training
        self.isLastSkipped = _contextMatrix.iloc[-1]['not_skipped']

        # Initialize the track features of final song
        trackID = self.finalRow.iloc[0]['track_id_clean']
        trackIndex = trackIDs.index(trackID)
        self.finalSong = tracks[trackIndex]
        
        # the track feature vectors in a users session except final one
        # this is needed to preserve their order
        self.userTracks = []

        # all of the skipped track feature vectors in a users session
        self.skipped = []

        # all of the non skipped track feature vectors in a users session
        self.nonSkipped = []

        self.initializeTracks()

    def initializeTracks(self):
        """
        Uses the content matrix of a session to initialize 
        the skipped and nonskipped lists
        """

        # puts the track vector of each song into a list of the user's history
        # and sorts into divided lists skipped and nonSkipped
        for track in self.contextMatrix.iterrows():

            trackID = track[1]['track_id_clean']
            notSkipped = track[1]['not_skipped']

            trackIndex = trackIDs.index(trackID)
            trackFeats = tracks[trackIndex]

            self.userTracks.append(trackFeats)

            # add it to respective list
            if notSkipped:
                self.nonSkipped.append(trackFeats)
            else:
                self.skipped.append(trackFeats)
        sessionLengths.append(len(self.userTracks))

    def miniForestDecision(self):
        """
        Trains a random forest for one session 
        """
        # training data is the tracks (except final one)
        data = self.contextMatrix

        lastRow = self.finalRow

        # Use everything cept that session id and the not_skipped variable
        X = data.loc[:, ~data.columns.isin(['not_skipped', 'session_id', 'track_id'])]

        y = data.not_skipped

        # ignoring the usual train - test splitting step bc its all going to be used for training

        # Create Decision Tree classifer object
        mini_tree = RandomForestClassifier(max_depth=5, random_state=0)

        mini_tree = mini_tree.fit(X, y)

        # Ask it to make one prediction on the final row

        lastRow_X =  lastRow.loc[:, ~data.columns.isin(['not_skipped', 'session_id'])]
        lastRow_y = lastRow.not_skipped # keep the answer just in case, idk

        prediction = mini_tree.predict(lastRow_X)

        # Add to the aggregates
        running_importances += mini_tree.feature_importances_

        return prediction



    def getDayOfWeek(self):
        date = datetime.datetime.strptime(self.date, "%Y-%m-%d").date()
        x = date.weekday()
        return x

    def getMonth(self):
        date = datetime.datetime.strptime(self.date, "%Y-%m-%d").date()
        x = date.month
        return x
