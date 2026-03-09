__title__ = "Rent-Price Predicter"
__version__ = "0.1.0"
__author__ = "capsgit"
__doc__ = """
Predict -throw a model- and Save into a db the rent-price-prediction for a home-area
"""
from app.config import DB_PATH, MODEL_PATH
from app.database import PredictionRepository
from app.model_service import ModelService
from app.schemas import PredictionRecord, PredictionResponse
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="PredictionPrice -> Web-service",
    version="0.1.0",
    description="Predicts the Rentprice for an input area and save both in DB",
)

model_service = ModelService(MODEL_PATH)  # load model (one time)
repository = PredictionRepository(DB_PATH)


@app.get("/")
async def root():
    return {"msg": "Welcome to my Area/price prediction"}


@app.get("/predict_price", response_model=PredictionResponse)
async def predict_price(area: int):
    """
    Predic the price for a home-area (m²) using => model_linear_reg_v1.pkl
    """
    try:
        if area <= 0:
            raise HTTPException(status_code=400, detail="Area must be greater than 0")

        predicted_price = model_service.predict_price(area)
        repository.save_prediction(area, predicted_price)

        return PredictionResponse(
            msg="The predicted price in EURO",
            area=area,
            predicted_price=round(predicted_price, 2),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/all_predictions")
async def get_predictions():
    """
    Show predictions record
    """
    rows = repository.get_all_predictions()

    return [
        PredictionRecord(
            id=row[0], area=row[1], predicted_price=row[2], created_at=row[3]
        )
        for row in rows
    ]
