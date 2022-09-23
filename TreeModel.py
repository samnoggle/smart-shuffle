
from IPython.display import Image
import pydotplus
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
# Visualization libraries
from sklearn.tree import export_graphviz
from six import StringIO

def create_tree():
    """
    Creates, trains, and tests a decision tree using 
    data from 'tree/claimTokens.csv'
    Then, saves the model to tree/tree_model.sav
    """

    col_names = ['token', 'hasCapitalNext', 'formatAligns', 'length', 'lineDepth', 'isClaimNumber']

    # load dataset
    claim = pd.read_csv("tree/claimTokens.csv", header=None, names=col_names)

    # split dataset into features(token) and target variable(isClaimNumber)
    feature_cols = ['hasCapitalNext', 'formatAligns', 'length', 'lineDepth']
    X = claim[feature_cols]
    y = claim.isClaimNumber


    # Split dataset into training set and test set
    # 70% training and 30% test to start
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=1)

    # Create Decision Tree classifer object
    d_tree = DecisionTreeClassifier()

    # Train Decision Tree Classifer
    d_tree = d_tree.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = d_tree.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Model Accuracy:", metrics.accuracy_score(y_test, y_pred))
