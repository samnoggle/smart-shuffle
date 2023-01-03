"""
    Class to store a session's data
"""
import pandas as pd

# public track index where all track features
# are loaded into
trackIDs = []
tracks = []

trackData = pd.DataFrame()


class Session:
    def __init__(self, _contextMatrix, _finalRow):
        '''
        HERE I WILL HAVE TO EVENTUALLY ACCOUNT FOR FIRST HALF OF SESSION AND SECOND HALF
        CALCULATE METRICS ABOUT THE METADATA OF THE FIRST HALF
        FOR NOW IT IS AS IF I ONLY HAVE THE BARE BONES SECOND HALF W/O ANY METADATA
        '''
        self.contextMatrix = _contextMatrix
        self.finalRow = _finalRow
        self.sessionID = _contextMatrix.iloc[0]['session_id']

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


# broke
    # def isPrevSongSkipped(self, k):
    #     """
    #     Returns true if the previous song of k was skipped
    #     :param k: the index in userTracks
    #     """
    #     if (k < len(self.userTracks)) and (len(self.userTracks) >= 2):
    #         prevVect = self.userTracks[k - 1]

    #         # this seems like a botched way to do this
    #         for array in self.skipped:
    #             comparison = prevVect == array
    #             equal_arrays = comparison.all()
    #             if equal_arrays == True:
    #                 return True
    #         return False
            

