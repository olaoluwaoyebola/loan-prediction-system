# API

from fastapi import FastAPI

# import from the backend package to ensure module resolution when the app
# is started from the repository root (e.g. uvicorn backend.main:app).
from backend.prediction import predict_loan
from backend.schemas import LoanRequest

app = FastAPI()

# health check endpoint
@app.get("/health")
def home():
    return {"status": "ok"}

# prediction endpoint
@app.post("/predict")
def predict(request: LoanRequest):
    data = request.model_dump()         # convert pydantic model to dict
    prediction = predict_loan(data)     # get prediction from model
    return {"prediction": prediction}   # return prediction as JSON response