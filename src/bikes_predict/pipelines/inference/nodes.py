"""
This is a boilerplate pipeline 'inference'
generated using Kedro 1.5.0
"""
import pandas as pd


def predict(model, df: pd.DataFrame) -> pd.DataFrame:
    """Predict next-hour demand for each row."""
    X = df[model.feature_names_in_]          # same columns, same order as training
    out = df.copy()
    out["predicted_next_cnt"] = model.predict(X)
    return out