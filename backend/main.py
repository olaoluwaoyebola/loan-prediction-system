# API

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

# import from the backend package to ensure module resolution when the app
# is started from the repository root (e.g. uvicorn backend.main:app).
from backend.prediction import predict_loan
from backend.schemas import LoanRequest, LoanResponse

app = FastAPI(
    title="Loan Prediction API",
    description="REST API for predicting loan approval status",
    version="1.0.0",
)

# CORS middleware — allows the Streamlit frontend (or any other client)
# to call the API from a different origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# health check endpoint
@app.get("/health")
def home():
    return {"status": "ok"}

# prediction endpoint
@app.post("/predict", response_model=LoanResponse)
def predict(request: LoanRequest):
    data = request.model_dump()         # convert pydantic model to dict
    prediction = predict_loan(data)     # get prediction from model
    return {"prediction": prediction}   # return prediction as JSON response