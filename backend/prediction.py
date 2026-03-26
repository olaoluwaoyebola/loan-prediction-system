import pickle
import logging
import os

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


def predict_loan(data: dict) -> int:
    """Run prediction with the model based on applicant data."""
    input_df = pd.DataFrame([data], columns=columns)       # convert input data to df
    prediction = model.predict(input_df)                    # run model prediction

    # Convert 'Y'/'N' to 1/0
    result = 1 if prediction[0] == "Y" else 0
    logger.info("Prediction result: %s (raw: %s)", result, prediction[0])
    return result