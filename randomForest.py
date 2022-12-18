"""
Decision tree to decide if a token is a claim number or not
"""
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn import metrics, preprocessing
from io import StringIO
from tabulate import tabulate


def create_tree():
    """
    Creates, trains, and tests a decision tree using 
    data from 'lastSongMetrics.csv'

    Then, saves the model to randForest.sav
    """

    # load dataset
    data = pd.read_csv("lastSongMetrics.csv", header=0)


    # split dataset into features and target variable(is_skipped)
    # feature_cols = ['euclidLastPlay', 'euclidLastSkip', 'manLastPlay', 'manLastSkip', 'eucAvPlay', 'eucAvSkip', 'angleAvPlay', 'angleAvSkip', 'prevSongSkipped', 'neighborSkipped', 'context_switch','context_type','date','hist_user_behavior_is_shuffle','hist_user_behavior_n_seekback','hist_user_behavior_n_seekfwd','hist_user_behavior_reason_end','hist_user_behavior_reason_start','hour_of_day','long_pause_before_play','no_pause_before_play','premium','session_length','session_position', 'short_pause_before_play']
    X = data.loc[:, ~data.columns.isin(['not_skipped', 'track_id_clean', 'session_id', 'date', 'session_length'])]
    y = data.not_skipped


    # specify categories
    context_type = ['user_collection', 'editorial_playlist', 'catalog', 'radio', 'personalized_playlist', 'charts']
    behave_end = ['trackdone', 'fwdbtn', 'clickrow', 'logout', 'endplay', 'backbtn', 'remote' ]
    behave_start = ['fwdbtn', 'clickrow', 'appload', 'playbtn', 'backbtn', 'remote']

    # Think I need to do encoding on the data for categorical string features...
    X = pd.get_dummies(X, columns=['context_type', 'hist_user_behavior_reason_end', 'hist_user_behavior_reason_start'])
    
    print(X.to_string(max_rows=10))
  

    # Split dataset into training set and test set
    # 70% training and 30% test to start
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=1)

    # Create Decision Tree classifer object
    rf_tree = RandomForestClassifier(max_depth=10, random_state=0)

    # Train Decision Tree Classifer
    rf_tree = rf_tree.fit(X_train, y_train)

    # Save model
    pickle.dump(rf_tree, open('randForest.sav', 'wb'))

    # Predict the response for test dataset
    y_pred = rf_tree.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Model Accuracy:", metrics.accuracy_score(y_test, y_pred))



def load_model():
    rf_tree = pickle.load(open('randForest.sav', 'rb'))
    return rf_tree



############## DRIVER CODE #################
def main():
    create_tree()


# Calling main function
if __name__ == "__main__":
    main()


    # add conversion rate and the original price
    # and dollars too
    # asl for local curr first


    # flat rate depending on client
    # 3% on the currency exch
    # 3% percent for creditcard if they use
    # nothing if cash deposit
    # 1% for payment withing 8 days