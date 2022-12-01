"""
    Class to store a session's data
"""
# public track index where all track features
# are loaded into
trackIDs = []
tracks = []


class Session:
    def __init__(self, _contextMatrix):
        self.contextMatrix = _contextMatrix

        # The answer, only used for training
        self.isLastSkipped = False

        # all of the track vectors in a users session
        self.userTracks = []

        # all of the skipped track vectors in a users session
        self.skipped = []

        # all of the non skipped track vectors ina  users session
        self.nonSkipped = []

        self.initializeTracks()

    def initializeTracks(self):
        """
        Uses the content matrix of a session to initialize 
        the skipped and nonskipped lists
        """
        # puts the track vector of each song into a list of the user's history
        # and sorts into divided lists skipped and nonSkipped
        index = self.contextMatrix.index
        number_of_rows = len(index)

        for i, track in self.contextMatrix.iterrows():
            trackID = track['track_id_clean']
            notSkipped = track['not_skipped']

            trackIndex = trackIDs.index(trackID)
            trackFeats = tracks[trackIndex]

            self.userTracks.append(trackFeats)

            # the last track will not be added into the 2 lists
            if i != number_of_rows - 1:
                if notSkipped:
                    self.nonSkipped.append(trackFeats)
                else:
                    self.skipped.append(trackFeats)

    def isPrevSongSkipped(self, k):
        """
        Returns true if the previous song of k was skipped
        :param k: the index in userTracks
        """
        if (k < len(self.userTracks)) and (len(self.userTracks) >= 2):
            prevVect = self.userTracks[k - 1]

            # this seems like a botched way to do this
            for array in self.skipped:
                comparison = prevVect == array
                equal_arrays = comparison.all()
                if equal_arrays == True:
                    return True
            return False
            

