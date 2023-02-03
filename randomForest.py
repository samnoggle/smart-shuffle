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
    data = pd.read_csv("../lastSongMetrics.csv", header=0)


    # split dataset into features and target variable(not_skipped)
    X = data.loc[:, ~data.columns.isin(['not_skipped', 'session_id'])]
    y = data.not_skipped

    # Think I need to do encoding on the data for categorical string features...
    # DEPRECIATED BECUASE NO LONGER USING THIS DATA
    # X = pd.get_dummies(X, columns=['context_type', 'hist_user_behavior_reason_start'])
    
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


    #Visualize important features
    feature_imp = pd.Series(rf_tree.feature_importances_,index=X.columns).sort_values(ascending=False)

    print(feature_imp[:10])
    feature_imp = feature_imp[:10]

    import matplotlib.pyplot as plt
    import seaborn as sns

    # Creating a bar plot
    sns.barplot(x=feature_imp, y=feature_imp.index)
    # Add labels to your graph
    plt.xlabel('Feature Importance Score')
    plt.ylabel('Features')
    plt.title("Important Features: Track Features, Metrics & Metadata")
    plt.legend()
    plt.show()
    plt.tight_layout()
    plt.savefig('importantFeatures_FeatsMetricsMeta.pdf')



def load_model():
    rf_tree = pickle.load(open('randForest.sav', 'rb'))
    return rf_tree



############## DRIVER CODE #################
def main():
    create_tree()


# Calling main function
if __name__ == "__main__":
    main()
