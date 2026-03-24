# Area Price Prediction Web Service

FastAPI • Machine Learning • Scikit-Learn • SQLite • REST API

A lightweight machine learning web service that predicts housing prices based on the **area in square meters** using a pre-trained **Linear Regression model**. Each prediction request is stored in a **SQLite database** together with the input area, predicted price, and timestamp, allowing the application to keep a history of predictions for later analysis.

---

## Quick Start

Install dependencies

pip install -r requirements.txt

Run the API

uvicorn app.main:app --reload

Open the API documentation

http://127.0.0.1:8000/docs

---

## Example Request

GET /predictarea/50

Response

{
  "msg": "The predicted price in EURO",
  "area": 50,
  "predicted_price": 240000
}

---

## Project Structure

03_ML_Webservice
│
├── app
│   ├── main.py
│   ├── model_service.py
│   ├── database.py
│   └── config.py
│
├── models
│   └── model_linear_reg_v1.pkl
│
├── data
│   └── predictions.db
│
├── requirements.txt
└── README.md

---

## Architecture

The project follows a simple modular architecture. The FastAPI application handles HTTP requests and exposes the REST endpoints. A dedicated **model service** is responsible for loading the serialized machine learning model and performing predictions. A separate **database layer** manages persistence using SQLite, storing each prediction together with its input parameters and timestamp. This separation of concerns improves maintainability and reflects the structure commonly used in production ML services.

---

## Technologies

Python  
FastAPI  
Uvicorn  
Scikit-Learn  
NumPy  
SQLite