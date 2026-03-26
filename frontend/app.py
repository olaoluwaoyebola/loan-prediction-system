# Loan Application Prediction System - Streamlit Frontend
# This Streamlit app collects user input for loan application and sends it to the FastAPI backend

# Import necessary libraries
import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# Configure page layout to maximize space
st.set_page_config(layout="wide", page_title="Loan Application", initial_sidebar_state="collapsed")

# API endpoint for prediction — configurable via environment variable
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

# Mapping dictionaries for categorical values
gender_map = {"Male": 0, "Female": 1}
married_map = {"No": 0, "Yes": 1}
education_map = {"Graduate": 0, "Undergraduate": 1}
self_employed_map = {"No": 0, "Yes": 1}
credit_history_map = {"No History": 0, "History Available": 1}
property_area_map = {"Urban": 0, "Semiurban": 1, "Rural": 2}

# Initialize session state for multi-step form
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.form_data = {}


def get_step_class(step_number: int) -> str:
    """Return the CSS class for a step indicator based on the current step."""
    current = st.session_state.step
    if step_number == current:
        return "step-active"
    elif step_number < current:
        return "step-completed"
    else:
        return "step-pending"


# Custom CSS for styling
st.markdown("""
    <style>
    /* Maximize page width and spacing */
    .main {
        max-width: 100%;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    
    /* Remove default margins */
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
    
    .header-container {
        background: linear-gradient(135deg, #6C5CE7 0%, #A29BFE 100%);
        padding: 30px 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-title {
        color: white;
        font-size: 2.5em;
        font-weight: bold;
        margin: 0;
    }
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1em;
        margin: 8px 0 0 0;
    }
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
        gap: 8px;
    }
    .step-circle {
        flex: 1;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 0.9em;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .step-active {
        background-color: #6C5CE7;
        color: white;
        box-shadow: 0 2px 8px rgba(108, 92, 231, 0.3);
    }
    .step-completed {
        background-color: #00B894;
        color: white;
    }
    .step-pending {
        background-color: #ECF0F1;
        color: #7F8C8D;
    }
    .form-section {
        background: #F8F9FA;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .button-container {
        display: flex;
        gap: 10px;
        justify-content: center;
        margin-top: 20px;
    }
    
    /* Darken input fields */
    input[type="text"],
    input[type="number"],
    select,
    textarea {
        background-color: #2D3436 !important;
        color: #FFFFFF !important;
        border: 1px solid #4A4A4A !important;
    }
    
    input[type="text"]::placeholder,
    textarea::placeholder {
        color: #B0B0B0 !important;
    }
    
    input[type="text"]:focus,
    input[type="number"]:focus,
    select:focus,
    textarea:focus {
        background-color: #353A40 !important;
        border: 1px solid #6C5CE7 !important;
        color: #FFFFFF !important;
    }
    
    /* Streamlit specific selectors */
    [data-testid="stTextInput"] input,
    [data-testid="stSelectbox"] select,
    [data-testid="stTextArea"] textarea {
        background-color: #2D3436 !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <div class="header-title">Loan Application 💰</div>
        <div class="header-subtitle">Complete your application!</div>
    </div>
""", unsafe_allow_html=True)

# Dynamic step indicators — highlights based on current step
step1_cls = get_step_class(1)
step2_cls = get_step_class(2)
step3_cls = get_step_class(3)

st.markdown(f"""
    <div class="step-indicator">
        <div class="step-circle {step1_cls}">
            <span>1️⃣</span><br>Personal Information
        </div>
        <div class="step-circle {step2_cls}">
            <span>2️⃣</span><br>Employment Information
        </div>
        <div class="step-circle {step3_cls}">
            <span>3️⃣</span><br>Financial Information
        </div>
    </div>
""", unsafe_allow_html=True)

# Step 1: Personal Information
if st.session_state.step == 1:
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.subheader("📋 Personal Information")
    
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", list(gender_map.keys()), index=None, placeholder="Select Gender")
        dependents_text = st.text_input("Dependents", placeholder="0-5", value=st.session_state.form_data.get("dependents_text", ""))
    with col2:
        married = st.selectbox("Married", list(married_map.keys()), index=None, placeholder="Select Option")
        education = st.selectbox("Education", list(education_map.keys()), index=None, placeholder="Select Education Level")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Next →", use_container_width=True, key="next_step1"):
            if gender is None or married is None or education is None or dependents_text == "":
                st.error("⚠️ Please fill all fields to continue")
            else:
                try:
                    dependents = int(dependents_text)
                    if not (0 <= dependents <= 5):
                        st.error("⚠️ Dependents must be between 0-5")
                    else:
                        st.session_state.form_data["gender"] = gender
                        st.session_state.form_data["married"] = married
                        st.session_state.form_data["education"] = education
                        st.session_state.form_data["dependents"] = dependents
                        st.session_state.form_data["dependents_text"] = dependents_text
                        st.session_state.step = 2
                        st.rerun()
                except ValueError:
                    st.error("⚠️ Dependents must be a number")

# Step 2: Employment Information
elif st.session_state.step == 2:
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.subheader("💼 Employment Information")
    
    col1, col2 = st.columns(2)
    with col1:
        self_employed = st.selectbox("Self Employed", list(self_employed_map.keys()), index=None, placeholder="Select Option")
        income_text = st.text_input("Applicant Income", placeholder="Enter amount", value=st.session_state.form_data.get("income_text", ""))
    with col2:
        st.write("")
        st.write("")
        co_income_text = st.text_input("Coapplicant Income", placeholder="Enter amount", value=st.session_state.form_data.get("co_income_text", ""))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Previous", use_container_width=True, key="prev_step2"):
            st.session_state.step = 1
            st.rerun()
    with col3:
        if st.button("Next →", use_container_width=True, key="next_step2"):
            if self_employed is None or income_text == "" or co_income_text == "":
                st.error("⚠️ Please fill all fields to continue")
            else:
                try:
                    income = float(income_text)
                    co_income = float(co_income_text)
                    if income < 0 or co_income < 0:
                        st.error("⚠️ Income values must be positive")
                    else:
                        st.session_state.form_data["self_employed"] = self_employed
                        st.session_state.form_data["income"] = income
                        st.session_state.form_data["income_text"] = income_text
                        st.session_state.form_data["co_income"] = co_income
                        st.session_state.form_data["co_income_text"] = co_income_text
                        st.session_state.step = 3
                        st.rerun()
                except ValueError:
                    st.error("⚠️ Income values must be valid numbers")

# Step 3: Financial Information
elif st.session_state.step == 3:
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.subheader("💰 Financial Information")
    
    col1, col2 = st.columns(2)
    with col1:
        loan_amount_text = st.text_input("Loan Amount", placeholder="Enter amount", value=st.session_state.form_data.get("loan_amount_text", ""))
        credit = st.selectbox("Credit History", list(credit_history_map.keys()), index=None, placeholder="Select Status")
    with col2:
        loan_term_text = st.text_input("Loan Term (months)", placeholder="Enter term", value=st.session_state.form_data.get("loan_term_text", ""))
        area = st.selectbox("Property Area", list(property_area_map.keys()), index=None, placeholder="Select Area")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Previous", use_container_width=True, key="prev_step3"):
            st.session_state.step = 2
            st.rerun()
    with col3:
        if st.button("🎯 Submit", use_container_width=True, key="submit"):
            if loan_amount_text == "" or loan_term_text == "" or credit is None or area is None:
                st.error("⚠️ Please fill all fields to continue")
            else:
                try:
                    loan_amount = float(loan_amount_text)
                    loan_term = int(loan_term_text)
                    if loan_amount < 0 or loan_term < 0:
                        st.error("⚠️ Values must be positive")
                    else:
                        st.session_state.form_data["loan_amount"] = loan_amount
                        st.session_state.form_data["loan_amount_text"] = loan_amount_text
                        st.session_state.form_data["loan_term"] = loan_term
                        st.session_state.form_data["loan_term_text"] = loan_term_text
                        st.session_state.form_data["credit"] = credit
                        st.session_state.form_data["area"] = area
                        
                        # Prepare payload
                        payload = {
                            "Gender": gender_map[st.session_state.form_data["gender"]],
                            "Married": married_map[st.session_state.form_data["married"]],
                            "Dependents": st.session_state.form_data["dependents"],
                            "Education": education_map[st.session_state.form_data["education"]],
                            "Self_Employed": self_employed_map[st.session_state.form_data["self_employed"]],
                            "ApplicantIncome": st.session_state.form_data["income"],
                            "CoapplicantIncome": st.session_state.form_data["co_income"],
                            "LoanAmount": loan_amount,
                            "Loan_Amount_Term": loan_term,
                            "Credit_History": credit_history_map[credit],
                            "Property_Area": property_area_map[area]
                        }
                        
                        # Make API request
                        try:
                            response = requests.post(API_URL, json=payload, timeout=10)
                            
                            if response.status_code == 200:
                                prediction = response.json()["prediction"]
                                
                                if prediction == 1:
                                    st.success("✅ Loan Approved!")
                                    st.balloons()
                                else:
                                    st.error("❌ Loan Rejected")
                                
                                # Reset form
                                if st.button("Start New Application"):
                                    st.session_state.step = 1
                                    st.session_state.form_data = {}
                                    st.rerun()
                            else:
                                st.error(f"❌ API Error: {response.status_code}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"❌ Connection Error: {str(e)}")
                except ValueError:
                    st.error("⚠️ Please enter valid numbers")