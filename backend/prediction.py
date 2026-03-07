import pickle
import pandas as pd
import os

# Get the absolute path to the model directory
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")

model = pickle.load(open(os.path.join(MODEL_DIR, "loan_model.pkl"), "rb"))            # model
columns = pickle.load(open(os.path.join(MODEL_DIR, "loan_columns.pkl"), "rb"))        # training features

def predict_loan(data):
    """Run prediction with the model based on applicant data"""
    input_df = pd.DataFrame([data], columns=columns)                # convert input data to df
    prediction = model.predict(input_df)                            # run model prediction
    
    # Convert 'Y'/'N' to 1/0
    result = 1 if prediction[0] == 'Y' else 0
    return result                                                   # return prediction as int