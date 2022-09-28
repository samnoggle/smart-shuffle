import pandas as pd

# The session data
data = pd.read_csv("../data/log_mini.csv") 
track_data = pd.read_csv("../data/tf_mini.csv")

# Get one session 

# First session ID and number of rows to start
sessionID = data['session_id'].iloc[0]
entries = data['session_length'].iloc[0] 
position = 0

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

    print("==========")
    print(subset)





# Split into feature columns
feature_cols = ['skip_1', 'skip_2', 'skip_3', 'not_skipped']

# print(data)
# data.head()