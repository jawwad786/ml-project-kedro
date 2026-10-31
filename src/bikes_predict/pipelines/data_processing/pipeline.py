"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.5.0
"""

from kedro.pipeline import node, Pipeline  # noqa
from .nodes import clean_data, add_features , create_target

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
            outputs="featured_data",
            name = "add_features_node"
        ),
        node(
            func = create_target,
            inputs = "featured_data",
            outputs="model_input_table",
            name = "create_target_node"
        )
    ])
