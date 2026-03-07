# API

from fastapi import FastAPI
from prediction import predict_loan
from schemas import LoanRequest

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