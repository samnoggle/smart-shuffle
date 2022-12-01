import preprocessing as p
import session as s
import metrics as m

# grabbing the data
p.loadTracks()
sessions = p.loadSessionContext()

# going through each session
for i, session in enumerate(sessions):
    # make a session object
    current = s.Session(session)

    # calculate metrics (predicting final song in session)
    # what if one of the lists is empty? they skipped all/listened to all?

    metrics = []
    finalSong = current.userTracks[-1]

    # get all those variables
    if current.skipped:
        euclidLastSkip = m.euclidian(finalSong, current.skipped[-1])
        manLastSkip = m.manhattan(finalSong, current.skipped[-1])
        avSkipped = m.averageTracks(current.skipped)
        eucAvSkip = m.euclidian(finalSong, avSkipped)
        angleAvSkip = m.angle_between(finalSong, avSkipped)
    else:
        euclidLastSkip = 0
        manLastSkip = 0
        eucAvSkip = 0
        angleAvSkip = 0
        

    if current.nonSkipped:
        euclidLastPlay = m.euclidian(finalSong, current.nonSkipped[-1])
        manLastPlay = m.manhattan(finalSong, current.nonSkipped[-1])
        avPlayed = m.averageTracks(current.nonSkipped)
        eucAvPlay = m.euclidian(finalSong, avPlayed)
        angleAvPlay = m.angle_between(finalSong, avPlayed)
    else:
        euclidLastPlay = 0
        manLastPlay = 0
        eucAvPlay = 0
        angleAvPlay = 0

    prevSongSkipped = current.isPrevSongSkipped(len(current.userTracks) - 1)

    neighborSkipped = m.is_neighbor_skipped(finalSong, current.skipped, current.nonSkipped)


    # 0 euclidian from last played
    metrics.append(euclidLastPlay)

    # 1 euclidian from last skipped
    metrics.append(euclidLastSkip)

    # 2 manhattan from last played
    metrics.append(manLastPlay)

    # 3 manhattan from last skipped
    metrics.append(manLastSkip)

    # 4 euclidian from averaged played vector
    metrics.append(eucAvPlay)

    # 5 euclidian from averaged skipped vector
    metrics.append(eucAvSkip)

    # 6 angle with averaged played vector
    metrics.append(angleAvPlay)

    # 7 angle with averaged skipped vector
    metrics.append(angleAvSkip)

    # 8 is the prev song skipped?
    metrics.append(prevSongSkipped)

    # 9 is the nearest neighbor skipped?
    metrics.append(neighborSkipped)


    # make a record for the decision tree
    print(metrics)