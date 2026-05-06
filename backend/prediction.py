import pickle
import logging
import os

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Get the absolute path to the model directory
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")

MODEL_PATH = os.path.join(MODEL_DIR, "loan_model.pkl")
COLUMNS_PATH = os.path.join(MODEL_DIR, "loan_columns.pkl")


def _load_pickle(path: str):
    """Safely load a pickle file with proper file-handle management."""
    with open(path, "rb") as f:
        return pickle.load(f)


try:
    model = _load_pickle(MODEL_PATH)
    columns = _load_pickle(COLUMNS_PATH)
    logger.info("Model and columns loaded successfully from %s", MODEL_DIR)
except FileNotFoundError as exc:
    logger.error("Model files not found in %s: %s", MODEL_DIR, exc)
    raise SystemExit(
        f"ERROR: Required model files not found in '{MODEL_DIR}'. "
        "Run the training notebook first to generate loan_model.pkl and loan_columns.pkl."
    ) from exc
except Exception as exc:
    logger.error("Failed to load model files: %s", exc)
    raise SystemExit(f"ERROR: Could not load model files — {exc}") from exc


def _engineer_features(data: dict) -> dict:
    """Compute engineered features from raw API inputs.

    The rebuilt model expects these derived columns instead of the raw
    ApplicantIncome, CoapplicantIncome, and LoanAmount fields:
      - TotalIncome        = ApplicantIncome + CoapplicantIncome
      - EMI                = LoanAmount / Loan_Amount_Term
      - BalanceIncome      = TotalIncome - (EMI * 1000)
      - Log_TotalIncome    = log1p(TotalIncome)
      - Log_LoanAmount     = log1p(LoanAmount)
    """
    applicant_income = data["ApplicantIncome"]
    coapplicant_income = data["CoapplicantIncome"]
    loan_amount = data["LoanAmount"]
    loan_term = data["Loan_Amount_Term"]

    total_income = applicant_income + coapplicant_income
    emi = loan_amount / loan_term if loan_term else 0.0
    balance_income = total_income - (emi * 1000)

    # Build the feature dict with only the columns the model expects
    features = {
        "Gender": data["Gender"],
        "Married": data["Married"],
        "Dependents": data["Dependents"],
        "Education": data["Education"],
        "Self_Employed": data["Self_Employed"],
        "Loan_Amount_Term": loan_term,
        "Credit_History": data["Credit_History"],
        "Property_Area": data["Property_Area"],
        # Engineered features
        "TotalIncome": total_income,
        "EMI": emi,
        "BalanceIncome": balance_income,
        "Log_TotalIncome": np.log1p(total_income),
        "Log_LoanAmount": np.log1p(loan_amount),
    }
    return features


def predict_loan(data: dict) -> int:
    """Run prediction with the model based on applicant data.

    Accepts the raw API payload (with ApplicantIncome, CoapplicantIncome,
    LoanAmount), computes the engineered features, then feeds the
    transformed input to the sklearn pipeline.
    """
    features = _engineer_features(data)
    input_df = pd.DataFrame([features], columns=columns)
    prediction = model.predict(input_df)

    result = int(prediction[0])
    logger.info("Prediction result: %s", result)
    return result