import pickle
import pandas as pd

model = pickle.load(open("model/loan_model.pkl", "rb"))            # model
columns = pickle.load(open("model/loan_columns.pkl", "rb"))        # training features

def predict_loan(data):
    """Run prediction with the model based on applicant data"""
    input_df = pd.DataFrame([data], columns=columns)                # convert input data to df
    prediction = model.predict(input_df)                            # run model prediction
    return int(prediction[0])                                       # extract prediction value as int