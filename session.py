"""
    Class to store a session's data
"""
# public track index where all track features
# are loaded into
trackID = []
tracks = []


class Session:
    def __init__(self, _id, _contextMatrix):
        self.id = _id
        self.contextMatrix = _contextMatrix

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
        for track in self.contextMatrix.iterrows():

            trackID = track['track_id_clean'].iloc[0]
            notSkipped = track['not_skipped'].iloc[0]
            trackFeats = tracks[trackID.index(trackID)]
            self.userTracks.append(trackFeats)
            if notSkipped:
                self.nonSkipped.append(trackFeats)
            else:
                self.skipped.append(trackFeats)
