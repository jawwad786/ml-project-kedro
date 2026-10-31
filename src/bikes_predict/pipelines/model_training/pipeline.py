"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 1.5.0
"""

from kedro.pipeline import Node, Pipeline  # noqa
from .nodes import prepare_dataset


from kedro.pipeline import Pipeline, node, pipeline
from .nodes import prepare_dataset, train_model, evaluate_model

MODELS = ["random_forest", "linear_regression", "gradient_boosting"]
SPLITS = {"X_train", "X_test", "y_train", "y_test"}


def create_pipeline(**kwargs) -> Pipeline:
    split = pipeline([
        node(prepare_dataset, ["model_input_table", "params:train_fraction"],
             ["X_train", "X_test", "y_train", "y_test"], name="prepare_dataset_node"),
    ])

    template = pipeline([
        node(train_model, ["X_train", "y_train", "params:model_options"],
             "regressor", name="train_model"),
        node(evaluate_model, ["regressor", "X_test", "y_test"],
             "metrics", name="evaluate_model"),
    ])

    result = split
    for m in MODELS:
        result += pipeline(template, namespace=m, inputs=SPLITS)
    return result
