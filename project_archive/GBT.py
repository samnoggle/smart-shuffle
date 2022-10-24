from IPython.display import Image
import pydotplus
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.tree import export_graphviz
from six import StringIO

# THIS IS JUST A NORMAL TREE RIGHT NOW


def create_tree(dataframe):
    """
    Creates, trains, and tests a decision tree using 
    data from '******************'
    Then, saves the model to tree/tree_model.sav
    """

    # split dataset into features(token) and target variable(isClaimNumber)
    feature_cols = ['duration', 'release_year', 'us_popularity_estimate', 'acousticness', 'beat_strength', 'bounciness', 'danceability', 'dyn_range_mean', 'energy', 'flatness', 'instrumentalness', 'key', 'liveness', 'loudness', 'mechanism',
                    'organism', 'speechiness', 'tempo', 'time_signature', 'valence', 'acoustic_vector_0', 'acoustic_vector_1', 'acoustic_vector_2', 'acoustic_vector_3', 'acoustic_vector_4', 'acoustic_vector_5', 'acoustic_vector_6', 'acoustic_vector_7', 'context_switch','no_pause_before_play','short_pause_before_play','long_pause_before_play','hist_user_behavior_n_seekfwd','hist_user_behavior_n_seekback']
    X = dataframe[feature_cols]
    y = dataframe['not_skipped']

    # Split dataset into training set and test set
    # 70% training and 30% test to start
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=1)

    # Create Decision Tree classifer object
    rfc = RandomForestClassifier(n_estimators=100)

    # Train Decision Tree Classifer
    rfc= rfc.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = rfc.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    score = metrics.accuracy_score(y_test, y_pred)
    print("Model Accuracy:", score)
    return score

    # graph_tree(d_tree, feature_cols)


def graph_tree(d_tree, feature_cols):
    """
    Graphs a decision tree on a png
    :param d_tree: the tree object to graph
    :param feature_cols: a list of the tree's feature colums
    """

    dot_data = StringIO()
    export_graphviz(d_tree, out_file=dot_data,
                    filled=True, rounded=True,
                    special_characters=True, feature_names=feature_cols, class_names=['Yes', 'No'])
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png('tree.png')
    Image(graph.create_png())
