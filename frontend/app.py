import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("Loan Application")

# Personal Information Section
with st.expander("📋 Personal Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", [0, 1], help="0: Male, 1: Female")
        dependents = st.number_input("Dependents", min_value=0, max_value=5)
    with col2:
        married = st.selectbox("Married", [0, 1], help="0: No, 1: Yes")
        education = st.selectbox("Education", [0, 1], help="0: Graduate, 1: Undergraduate")

# Employment Information Section
with st.expander("💼 Employment Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        self_employed = st.selectbox("Self Employed", [0, 1], help="0: No, 1: Yes")
    with col2:
        income = st.number_input("Applicant Income", min_value=0)
    co_income = st.number_input("Coapplicant Income", min_value=0)

# Financial Information Section
with st.expander("💰 Financial Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        loan_amount = st.number_input("Loan Amount", min_value=0)
        credit = st.selectbox("Credit History", [0, 1], help="0: No history, 1: History available")
    with col2:
        loan_term = st.number_input("Loan Term (months)", min_value=0)
        area = st.selectbox("Property Area", [0, 1, 2], help="0: Urban, 1: Semiurban, 2: Rural")

if st.button("Predict Loan Status", use_container_width=True):

    payload = {
        "Gender": gender,
        "Married": married,
        "Dependents": dependents,
        "Education": education,
        "Self_Employed": self_employed,
        "ApplicantIncome": income,
        "CoapplicantIncome": co_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_term,
        "Credit_History": credit,
        "Property_Area": area
    }

    response = requests.post(API_URL, json=payload)

    prediction = response.json()["prediction"]

    if prediction == 1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Rejected")