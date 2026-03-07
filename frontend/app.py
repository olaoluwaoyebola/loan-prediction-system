import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

# Mapping dictionaries for categorical values
gender_map = {"Male": 0, "Female": 1}
married_map = {"No": 0, "Yes": 1}
education_map = {"Graduate": 0, "Undergraduate": 1}
self_employed_map = {"No": 0, "Yes": 1}
credit_history_map = {"No History": 0, "History Available": 1}
property_area_map = {"Urban": 0, "Semiurban": 1, "Rural": 2}

st.title("Loan Application")

# Personal Information Section
with st.expander("📋 Personal Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", list(gender_map.keys()), index=None, placeholder="Select Gender")
        dependents_text = st.text_input("Dependents", placeholder="0-5")
    with col2:
        married = st.selectbox("Married", list(married_map.keys()), index=None, placeholder="Select Option")
        education = st.selectbox("Education", list(education_map.keys()), index=None, placeholder="Select Education Level")

# Employment Information Section
with st.expander("💼 Employment Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        self_employed = st.selectbox("Self Employed", list(self_employed_map.keys()), index=None, placeholder="Select Option")
    with col2:
        income_text = st.text_input("Applicant Income", placeholder="Enter amount")
    co_income_text = st.text_input("Coapplicant Income", placeholder="Enter amount")

# Financial Information Section
with st.expander("💰 Financial Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        loan_amount_text = st.text_input("Loan Amount", placeholder="Enter amount")
        credit = st.selectbox("Credit History", list(credit_history_map.keys()), index=None, placeholder="Select Status")
    with col2:
        loan_term_text = st.text_input("Loan Term (months)", placeholder="Enter term")
        area = st.selectbox("Property Area", list(property_area_map.keys()), index=None, placeholder="Select Area")

if st.button("Predict Loan Status", use_container_width=True):

    # Validate all required fields are selected
    required_fields = {
        "Gender": gender,
        "Married": married,
        "Education": education,
        "Self Employed": self_employed,
        "Credit History": credit,
        "Property Area": area
    }
    missing_fields = [field for field, value in required_fields.items() if value is None]

    # Validate numeric fields (text inputs)
    # Dependents should be an integer between 0 and 5, while the others should be positive numbers
    numeric_errors = []

    # Validate dependents separately since it has a specific range and type requirement
    try:
        dependents = int(dependents_text) if dependents_text != "" else None
        if dependents is None or not (0 <= dependents <= 5):
            numeric_errors.append("Dependents (0-5)")
    except ValueError:
        numeric_errors.append("Dependents (integer)")

    # Helper function to parse and validate positive numeric inputs
    def parse_positive(name, text, cast_type=float):
        """Parse and validate positive numeric input"""
        # Check for empty input first
        if text == "":
            numeric_errors.append(name)
            return None
        # Try to convert to the specified type and check if it's positive
        try:
            val = cast_type(text)
            if val < 0:
                numeric_errors.append(name)
                return None
            return val
        except ValueError:
            numeric_errors.append(name)
            return None

    # Validate and parse numeric fields
    income = parse_positive("Applicant Income", income_text)
    co_income = parse_positive("Coapplicant Income", co_income_text)
    loan_amount = parse_positive("Loan Amount", loan_amount_text)
    loan_term = parse_positive("Loan Term", loan_term_text, cast_type=int)

    # If there are any missing fields or numeric errors, show a warning message and do not proceed with the API call
    if missing_fields or numeric_errors:
        messages = []
        if missing_fields:
            messages.append(f"select: {', '.join(missing_fields)}")
        if numeric_errors:
            messages.append(f"provide valid values for: {', '.join(numeric_errors)}")
        st.warning("⚠️ " + "; ".join(messages))
    else:
        payload = {
            "Gender": gender_map[gender],
            "Married": married_map[married],
            "Dependents": dependents,
            "Education": education_map[education],
            "Self_Employed": self_employed_map[self_employed],
            "ApplicantIncome": income,
            "CoapplicantIncome": co_income,
            "LoanAmount": loan_amount,
            "Loan_Amount_Term": loan_term,
            "Credit_History": credit_history_map[credit],
            "Property_Area": property_area_map[area]
        }

        # Make API request to backend for prediction
        # Added error handling for connection issues and invalid responses
        try:
            response = requests.post(API_URL, json=payload, timeout=10)

            # Check if the response is successful
            if response.status_code == 200:                     # successful response, extract prediction,
                prediction = response.json()["prediction"]

                # Display result based on prediction
                if prediction == 1:
                    st.success("✅ Loan Approved")
                else:
                    st.error("❌ Loan Rejected")
            else:
                st.error(f"❌ API Error: {response.status_code} - {response.text}")

        # Handle exceptions for connection errors and invalid responses
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Connection Error: Unable to connect to the prediction service. Please ensure the backend is running. Error: {str(e)}")
        except ValueError as e:
            st.error(f"❌ Response Error: Invalid response from server. Error: {str(e)}")