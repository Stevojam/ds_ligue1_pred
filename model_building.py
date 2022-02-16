import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

df = pd.read_csv('L1_squad_standings_cleaned.csv')

to_keep = [
    "Points",
    "Market_value",
    "Pts_year_before"
]

### Function to split the dataframe for the 10-fold cross validation

def train_test_split_by_year(year, df):
    test_df = df.loc[df["Season"] == year]
    train_df = df.loc[df["Season"] != year]

    test_df2 = test_df.copy()
    train_df2 = train_df2.copy()

    X_train = train_df2.copy()
    y_train = X_train["Points"]

    X_test = test_df2.copy()
    y_test = test_df2["Points"]

    X_train.drop('Points', axis=1, inplace=True)
    cols = X_train.columns
    X_test.drop('Points', axis=1, inplace=True)

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)
    y_test = np.array(y_test)

    return X_train, y_train, X_test, y_test



