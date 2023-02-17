"""
Decision tree to decide if a token is a claim number or not
"""
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns


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
    X = data.loc[:, ~data.columns.isin(['not_skipped', 'session_id', 'angleAvPlay', 'angleAvSkip', 'angleLastPlay', 'angleLastSkip', 'eucAvPlay', 'eucAvSkip', 'euclidLastPlay', 'euclidLastSkip', 'duration','release_year','us_popularity_estimate','acousticness','beat_strength','bounciness','danceability','dyn_range_mean','energy','flatness','instrumentalness','key','liveness','loudness','mechanism','mode','organism','speechiness','tempo','time_signature','valence','acoustic_vector_0','acoustic_vector_1','acoustic_vector_2','acoustic_vector_3','acoustic_vector_4','acoustic_vector_5','acoustic_vector_6','acoustic_vector_7', 'hour_of_day','day_of_week','month','premium'])]

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
    y_pred_test = rf_tree.predict(X_test)
    print('Training Accuracy : ', metrics.accuracy_score(y_train, rf_tree.predict(X_train))*100) # accuracy on train set
    print('Validation Accuracy : ', metrics.accuracy_score(y_test, y_pred_test)*100) # accuracy on test set

    # Generate confusion matrix
    matrix = confusion_matrix(y_test, y_pred_test)

    # Get and reshape confusion matrix data
    matrix = confusion_matrix(y_test, y_pred_test)
    matrix = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]

    # Build the plot
    plt.figure(figsize=(16,7))
    sns.set(font_scale=1.4)
    sns.heatmap(matrix, annot=True, annot_kws={'size':10},
                cmap=plt.cm.Greens, linewidths=0.2)

    # Add labels to the plot
    class_names = ['prevSongPlayed', 'percent_skipped', 'manLastSkip', 'manLastPlay', 'neighborSkipped', 'manAvPlay', 'manAvSkip',]
    tick_marks = np.arange(len(class_names))
    tick_marks2 = tick_marks + 0.5
    plt.xticks(tick_marks, class_names, rotation=25)
    plt.yticks(tick_marks2, class_names, rotation=0)
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.title('Confusion Matrix for Random Forest Model')
    plt.savefig('../../home/students/sjnoggle/confusionMatrix_OurData.pdf')

    #Visualize important features
    feature_imp = pd.Series(rf_tree.feature_importances_,index=X.columns).sort_values(ascending=False)

    print(feature_imp)

    # feature_imp = feature_imp[:10]

    # # Creating a bar plot
    # sns.barplot(x=feature_imp, y=feature_imp.index)
    # # Add labels to your graph
    # plt.xlabel('Feature Importance Score')
    # plt.ylabel('Features')
    # plt.title("Important Features: All Metrics")
    # plt.legend()
    # plt.show()
    # plt.tight_layout()
    # plt.savefig('../../home/students/sjnoggle/newGraphs/impFeats_AllMetrics.pdf')



def load_model():
    rf_tree = pickle.load(open('randForest.sav', 'rb'))
    return rf_tree



############## DRIVER CODE #################
def main():
    create_tree()


# Calling main function
if __name__ == "__main__":
    main()
