"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.5.0
"""

from kedro.pipeline import node, Pipeline  # noqa
from .nodes import clean_data, add_features

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func = clean_data,
            inputs = ["my_raw_data", "params:drop_columns"],
            outputs = "cleaned_data",
            name = "clean_data_node"
        ),
        node(
            func = add_features,
            inputs = ["cleaned_data", "params:lags"],
            outputs="model_input_table",
            name = "add_features_node"
        ),
    ])
