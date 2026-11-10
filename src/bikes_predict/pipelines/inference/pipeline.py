"""
This is a boilerplate pipeline 'inference'
generated using Kedro 1.5.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from bikes_predict.pipelines.data_processing.nodes import add_features, clean_data
from .nodes import predict


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(clean_data, ["new_raw_data", "params:drop_columns"],
             "new_cleaned_data", name="inference_clean_data_node"),
        node(add_features, ["new_cleaned_data", "params:lags"],
             "new_featured_data", name="inference_add_features_node"),
        node(predict, ["champion_model", "new_featured_data"],
             "predictions", name="predict_node"),
    ])