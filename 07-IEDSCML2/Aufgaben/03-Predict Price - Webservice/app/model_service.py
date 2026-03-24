"""
class to load model and run ->(predict)
"""

import pickle


class ModelService:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        with open(self.model_path, "rb") as file:
            model = pickle.load(file)
        return model

    def predict_price(self, area: int) -> float:
        prediction = self.model.predict([[area]])[0]
        return float(prediction)
