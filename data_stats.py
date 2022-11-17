"""
Script to grab stats about the dataset
"""

import preprocessing as p

def finalSongSkip(sessions):
    """
    Calculates the proportion of sessions with the last song 
    in the session being skipped.
    """
    skippedNum = 0
    for session in sessions:
        lastRow = session.tail(1)
        notSkipped = lastRow.iloc[0]['not_skipped']
        if notSkipped == False:
            skippedNum += 1
    
    print("In {0} sessions the last song was skipped. Out of {1} sessions".format(skippedNum, len(sessions)))
    percent = (skippedNum / len(sessions))
    print("The last song was skipped {0} of the time".format(percent))




############## DRIVER CODE #################
def main():
    sessions = p.loadSessionContext()
    finalSongSkip(sessions)
   




# Calling main function
if __name__ == "__main__":
    main()
