import pickle

model = pickle.load(open("model/loan_model.pkl", "rb"))
columns = pickle.load(open("model/loan_columns.pkl", "rb"))