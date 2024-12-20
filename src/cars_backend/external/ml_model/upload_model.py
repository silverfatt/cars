from typing import Any

import joblib


class Model:
    predictor: Any


model = Model()


def load_model():
    model.predictor = joblib.load("model.joblib")
