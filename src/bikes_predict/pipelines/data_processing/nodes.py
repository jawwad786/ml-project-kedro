"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.5.0
"""

import pandas as pd

def clean_data(df: pd.DataFrame , drop_columns: list) -> pd.DataFrame:
    "returns a cleaned dataframe by dropping specified columns"
    """
    Args:
        df: input dataframe to be cleaned
        drop_columns: list of columns to be dropped from the dataframe
    Returns:
        cleaned dataframe with specified columns dropped
    """
    return df.drop(columns=drop_columns)
    


def add_features(df: pd.DataFrame, lags: list) -> pd.DataFrame:
    """Add lag features of the target column.

    Args:
        df: Input dataframe, sorted in time order.
        lags: Lag steps to create, e.g. [1, 2, 3].

    Returns:
        Dataframe with lag_<n> columns added.
    """
    df = df.copy()
    for n in lags:
        df[f"lag_{n}"] = df["cnt"].shift(n).fillna(df["cnt"])
    return df