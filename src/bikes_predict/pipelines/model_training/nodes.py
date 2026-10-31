"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 1.5.0
"""
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Union
from sklearn.metrics import mean_absolute_error, mean_squared_error
import importlib


def prepare_dataset(
    df: pd.DataFrame, 
    train_fraction: float = 0.8
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Splits a DataFrame into training and testing sets for features and target.

    Parameters:
    ----------
    df : pd.DataFrame
        The input DataFrame that must contain a 'target' column.
    train_fraction : float, optional (default=0.8)
        The fraction of data to use for training (between 0 and 1).

    Returns:
    -------
    x_train : pd.DataFrame
        Training features.
    x_test : pd.DataFrame
        Testing features.
    y_train : pd.Series
        Training target values.
    y_test : pd.Series
        Testing target values.
    """
    feats = [col for col in df.columns if col != 'target']
    x, y = df[feats], df['target']
    train_size = int(train_fraction * df.shape[0])
    x_train, x_test = x[:train_size], x[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    return x_train, x_test, y_train, y_test


def compute_metrics(
    y_true: Union[np.ndarray, list], 
    y_pred: Union[np.ndarray, list]
) -> Dict[str, float]:
    """
    Compute evaluation metrics between true and predicted values.

    Metrics returned:
    - MAPE: Mean Absolute Percentage Error (in %)
    - MAE: Mean Absolute Error
    - RMSE: Root Mean Squared Error

    Parameters:
    ----------
    y_true : array-like
        Ground truth values.
    y_pred : array-like
        Predicted values.

    Returns:
    -------
    dict
        Dictionary with keys 'MAPE', 'MAE', and 'RMSE' and their float values.
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred, squared=False)

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    mape = np.mean(np.abs((y_true - y_pred) / np.where(y_true == 0, 0.01, y_true))) * 100

    return {
        'MAE': round(mae, 2),
        'RMSE': round(rmse, 2),
        'MAPE': round(mape, 2)
    }

def train_model(X_train: pd.DataFrame, y_train: pd.Series, model_options: dict):
    """
    Train a model based on the provided model options.

    Parameters:
    ----------
    X_train : pd.DataFrame
        Training features.
    y_train : pd.Series
        Training target values.
    model_options : dict
        Dictionary containing model class path and optional keyword arguments.
        Example:
        {
            "class": "sklearn.linear_model.LinearRegression",
            "kwargs": {"fit_intercept": True}
        }

    Returns:
    -------
    model
        Trained model instance.
    """
    module, cls = model_options["class"].rsplit(".", 1)
    ModelClass = getattr(importlib.import_module(module), cls)
    model = ModelClass(**model_options.get("kwargs", {}))
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """
    Evaluate the trained model on the test set and compute metrics.

    Parameters:
    ----------
    model : Trained model instance
        The model to evaluate.
    X_test : pd.DataFrame
        Testing features.
    y_test : pd.Series
        Testing target values.

    Returns:
    -------
    dict
        Dictionary containing evaluation metrics with their values and step.
    """
    y_pred = model.predict(X_test)
    metrics = compute_metrics(y_test.values, y_pred)
    return {k: {"value": float(v), "step": 0} for k, v in metrics.items()}