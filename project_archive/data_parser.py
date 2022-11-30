import pandas as pd
import GBT as t

# The session data
data = pd.read_csv("data/log_mini.csv") 
track_data = pd.read_csv("data/tf_mini.csv")

# Turn each session into one row...

# First session ID and number of rows to start
sessionID = data['session_id'].iloc[0]
entries = data['session_length'].iloc[0] 
position = 0

# Add the track features into the subset... must be a better way? 

# Rename that column so it matches and can be merged
data.rename(columns = {'track_id_clean':'track_id'}, inplace = True)
data = pd.merge(data, track_data, on = "track_id", how = "left")

scores = []

while(1):
    # Make them into a subset dataset
    subset = data[position : position + entries]

    # Update to continue
    position = position + entries
    sessionID = data['session_id'].iloc[position]
    entries = data['session_length'].iloc[position]


    # Add the track features into the subset... must be a better way? 

    # Rename that column so it matches and can be merged
    subset.rename(columns = {'track_id_clean':'track_id'}, inplace = True)
    subset = pd.merge(subset, track_data, on = "track_id", how = "left")

    # print("==========")
    # print(subset)

    # Make a very basic tree with just that session?
    score = t.create_tree(subset)

    scores.append(score)
    avg = sum(scores)/len(scores)
    print("\n\n\n")
    print(score)
    print(avg)
    print(f"The random forest classifiers averaged an Accuracy score of: {0}".format(avg))


# Average all the session scores
avg = sum(scores)/len(scores)
print(f"The random forest classifiers averaged an Accuracy score of: {0}".format(avg))

Make a very basic tree with the whole data and sessions as rows
tree = t.create_tree(data)
