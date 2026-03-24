import os
import pickle

from fastapi import FastAPI
from pathlib import Path

os.chdir(Path(__file__).parent)

# 1) crear la aplicacion FAST API
app = FastAPI()

# 2) cargar el modelo
# -> con pickle
def load_model():
    with open("model_linear_reg_v1.pkl", "rb") as f:
        model = pickle.load(f)

    return model

"""   # -> con joblib
# MODEL_PATH = Path(__file__).parent / "model_linear_reg_v1.pkl"
# model = joblib.load(MODEL_PATH)"""

# test de prueba
@app.get("/")
def read_root():
    """Root Function of the Webservice

    Returns:
        dict: Static wellcome message
    """
    return {"message": "API running. Use /predict to get a price prediction."}

# asignar un path a la funcion
@app.get("/predict/{area}") # "/predict/{area}" si URL->http://127.0.0.1:8000/predict/123456
# o solo "/predict" si URL->http://127.0.0.1:8000/predict?area=123456
async def predict_price(area: int):
    """ Predicts the Rentprice for an input area

    Args:
        area (int): Area of the house to be predicted
    Return:
         dict: includes the predicted prices as a value
    """
    model = load_model()                                                                # 1 load model
    prediction = model.predict([[area]])[0]                                             # 2 use the model
    return {"msg": "El precio predecido esta en Euros", "value": float(prediction)}     # 3 return the prediction
