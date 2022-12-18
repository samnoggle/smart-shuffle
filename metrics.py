"""
Calculates different distance metrics    
"""
import numpy as np
from scipy import spatial


def averageTracks(trackList):
    """
    Calculates an average vector with the array of song vectors given

    :param trackList: Numpy array of song vectors
    """

    # Number of songs
    n = np.shape(trackList)[0]
    # Makes an array w/ the sum of the columns
    sums = np.sum(trackList, axis=0)
    # Divides by N
    averageVect = np.array([num / n for num in sums])

    return averageVect


def weightedAverageTracks(trackList):
    """
    Calculates a weighted average vector with the array of song vectors given

    :param trackList: Numpy array of song vectors
    """
    pass


def euclidian(p1, p2):
    return np.linalg.norm(p1 - p2)


def manhattan(p1, p2):
    return sum(abs(val1-val2) for val1, val2 in zip(p1, p2))


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(p1, p2):
    v1_u = unit_vector(p1)
    v2_u = unit_vector(p2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def is_neighbor_skipped(vector, skipped, listened):
    """
    Finds if the nearest neighbor(s) were skipped or not

    :param k: How many neighbors to check
    :param vector: The vector to find neighbors for
    :param skipped: vectors for skipped songs in the sessison
    :param listened: vectors for non-skipped songs in the session
    :returns: True if the closest neighbor was skipped
    """
    # combine all the vectors, but save the midpoint
    skippedCutoff = len(skipped)

    # Handle if one of the arrays is empty
    if not skipped:
        return False
    elif not listened:
        return True
    
    sessionSongs = np.concatenate((skipped, listened), axis=0)

    # build and use spatial tree to quickly find closest neighbor
    tree = spatial.KDTree(sessionSongs)
    t = tree.query(vector)

    if t[1] > skippedCutoff - 1:
        return True
    else:
        return False


############## DRIVER CODE #################
def main():
    tracks = np.array([[1, 2, 3], [10, 2, 2], [2, 3, 1]])
    print(averageTracks(tracks))


# Calling main function
if __name__ == "__main__":
    main()
