"""
Decision tree to decide if a token is a claim number or not
"""
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn import metrics


def create_tree():
    """
    Creates, trains, and tests a decision tree using 
    data from 'lastSongMetrics.csv'

    Then, saves the model to randForest.sav
    """

    # load dataset
    data = pd.read_csv("../lastSongMetricsBig.csv", header=0)

    # All Data
    # X = data.loc[:, ~data.columns.isin(['not_skipped', 'session_id', 'angleAvPlay', 'angleAvSkip', 'angleLastPlay', 'angleLastSkip', 'eucAvPlay', 'eucAvSkip', 'euclidLastPlay', 'euclidLastSkip'])]

    # Our Data
    X = data.loc[:, ~data.columns.isin(['not_skipped', 'session_id', 'percent_skipped', 'prevSongPlayed', 'month', 'premium', 'hour_of_day', 'day_of_week', 'duration','release_year','us_popularity_estimate','acousticness','beat_strength','bounciness','danceability','dyn_range_mean','energy','flatness','instrumentalness','key','liveness','loudness','mechanism','mode','organism','speechiness','tempo','time_signature','valence','acoustic_vector_0','acoustic_vector_1','acoustic_vector_2','acoustic_vector_3','acoustic_vector_4','acoustic_vector_5','acoustic_vector_6','acoustic_vector_7', 'hour_of_day','day_of_week','month','premium'])]

   # X = data.loc[:, ~data.columns.isin(['not_skipped', 'session_id', 'angleAvPlay', 'angleAvSkip', 'angleLastPlay', 'angleLastSkip', 'euclidLastPlay', 'euclidLastSkip', 'eucAvSkip', 'eucAvPlay', 'duration','release_year','us_popularity_estimate','acousticness','beat_strength','bounciness','danceability','dyn_range_mean','energy','flatness','instrumentalness','key','liveness','loudness','mechanism','mode','organism','speechiness','tempo','time_signature','valence','acoustic_vector_0','acoustic_vector_1','acoustic_vector_2','acoustic_vector_3','acoustic_vector_4','acoustic_vector_5','acoustic_vector_6','acoustic_vector_7'])]


    # split dataset into features and target variable(not_skipped)
    y = data.not_skipped
    
    print(X.to_string(max_rows=10))
  
    # Split dataset into training set and test set
    # 70% training and 30% test to start
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=0)

    # Create Decision Tree classifer object
    rf_tree = RandomForestClassifier(max_depth=6, random_state=0)

    # clf = RandomizedSearchCV(rf_model, model_params, n_iter=100, cv=5, random_state=1)

    # Train Decision Tree Classifer
    rf_tree = rf_tree.fit(X_train, y_train)

    # Save model
    pickle.dump(rf_tree, open('randForest.sav', 'wb'))


    # Model Accuracy, how often is the classifier correct?
    print('Training Accuracy : ', metrics.accuracy_score(y_train, rf_tree.predict(X_train))*100) # accuracy on train set
    print('Validation Accuracy : ', metrics.accuracy_score(y_test, rf_tree.predict(X_test))*100) # accuracy on test set

    # Generate confusion matrix
    y_pred_test = rf_tree.predict(X_test)
    confusion_matrix(y_test, y_pred_test)

    #Visualize important features
    feature_imp = pd.Series(rf_tree.feature_importances_,index=X.columns).sort_values(ascending=False)

    print(feature_imp)

    feature_imp = feature_imp[:10]

    import matplotlib.pyplot as plt
    import seaborn as sns

    # Creating a bar plot
    sns.barplot(x=feature_imp, y=feature_imp.index)
    # Add labels to your graph
    plt.xlabel('Feature Importance Score')
    plt.ylabel('Features')
    plt.title("Important Features: All Metrics")
    plt.legend()
    plt.show()
    plt.tight_layout()
    plt.savefig('../../home/students/sjnoggle/newGraphs/impFeats_AllMetrics.pdf')



def load_model():
    rf_tree = pickle.load(open('randForest.sav', 'rb'))
    return rf_tree



############## DRIVER CODE #################
def main():
    create_tree()


# Calling main function
if __name__ == "__main__":
    main()
