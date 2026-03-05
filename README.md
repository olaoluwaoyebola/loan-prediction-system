# Loan Approval Prediction System

### End-to-End Machine Learning Project (SQL → FastAPI → Streamlit)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Scikit-Learn](https://img.shields.io/badge/ScikitLearn-ML-orange)
![Status](https://img.shields.io/badge/Project-Active-success)

---

# Project Overview

This project implements a **complete end-to-end machine learning system** for predicting whether a loan application should be **approved or rejected**.

The project simulates a **real-world ML deployment pipeline**, covering:

* Data ingestion and storage using SQL
* Machine learning model training using Scikit-Learn
* API deployment using FastAPI
* Interactive user interface using Streamlit
* Version control and project hosting with GitHub

The model is trained using a **loan dataset containing applicant financial and demographic information**.

The trained model is served through a **REST API**, and users can interact with it via a **web application interface**.

---

# System Architecture

```text
User Input (Streamlit UI)
        │
        ▼
FastAPI REST API
        │
        ▼
Trained ML Model (.pkl)
        │
        ▼
Prediction Response
        │
        ▼
Result Displayed to User
```

---

# Project Structure

```text
loan-prediction-system/

│
├── data/
│   └── loan.csv
│
├── database/
│   └── load_data.py
│
├── notebook/
│   └── loan_model_training.ipynb
│
├── model/
│   └── loan_model.pkl
│
├── backend/
│   ├── main.py
│   ├── schemas.py
│   └── predictor.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Dataset Description

The dataset contains information about loan applicants, including:

| Feature           | Description              |
| ----------------- | ------------------------ |
| Gender            | Applicant gender         |
| Married           | Marital status           |
| Dependents        | Number of dependents     |
| Education         | Education level          |
| Self_Employed     | Employment status        |
| ApplicantIncome   | Primary applicant income |
| CoapplicantIncome | Co-applicant income      |
| LoanAmount        | Loan amount requested    |
| Loan_Amount_Term  | Loan repayment duration  |
| Credit_History    | Applicant credit history |
| Property_Area     | Property location        |

### Target Variable

`Loan_Status`

* **1 → Loan Approved**
* **0 → Loan Rejected**

---

# Machine Learning Model

The model is trained inside a **Jupyter Notebook**:

```
notebooks/loan_model_training.ipynb
```

### Training Workflow

1. Data Loading
2. Data Cleaning
3. Missing Value Handling
4. Encoding Categorical Variables
5. Feature Selection
6. Train/Test Split
7. Model Training
8. Model Evaluation
9. Model Serialization

### Algorithm Used

```
RandomForestClassifier
```

The trained model is saved as:

```
model/loan_model.pkl
```

This file is later loaded by the FastAPI backend.

---

# Backend API (FastAPI)

FastAPI serves the trained model as a **REST API**.

Main API file:

```
backend/main.py
```

### Start the API

```
uvicorn backend.main:app --reload
```

API documentation automatically generated:

```
http://127.0.0.1:8000/docs
```

Example API Request:

```json
{
 "Gender": 1,
 "Married": 1,
 "Dependents": 0,
 "Education": 1,
 "Self_Employed": 0,
 "ApplicantIncome": 5000,
 "CoapplicantIncome": 2000,
 "LoanAmount": 150,
 "Loan_Amount_Term": 360,
 "Credit_History": 1,
 "Property_Area": 2
}
```

API Response:

```json
{
 "prediction": 1
}
```

---

# Frontend Application (Streamlit)

A **Streamlit web interface** allows users to interact with the model without coding.

Frontend file:

```
frontend/app.py
```

Run the interface:

```
streamlit run frontend/app.py
```

Users can input loan application details and receive instant predictions.

---

# Installation Guide

### 1. Clone the Repository

```
git clone https://github.com/yourusername/loan-prediction-system.git
cd loan-prediction-system
```

---

### 2. Create Virtual Environment

```
python -m venv venv
```

Activate environment:

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

# Running the Project

### Step 1 — Train the Model

Open the notebook:

```
notebooks/loan_model_training.ipynb
```

Run all cells to generate:

```
model/loan_model.pkl
```

---

### Step 2 — Start the API

```
uvicorn backend.main:app --reload
```

---

### Step 3 — Launch the Frontend

```
streamlit run frontend/app.py
```

---

# Example Prediction Workflow

1. User opens the Streamlit app
2. User inputs applicant information
3. Data is sent to FastAPI
4. FastAPI loads the trained model
5. Model generates prediction
6. Result returned to Streamlit UI

---

# Possible Future Improvements

* Add **Scikit-Learn Pipeline for preprocessing**
* Implement **feature scaling and encoding pipelines**
* Add **model evaluation metrics dashboard**
* Deploy FastAPI on **Render or Railway**
* Deploy Streamlit on **Streamlit Cloud**
* Add **Docker containerization**
* Implement **model monitoring and logging**

---

# Skills Demonstrated

This project demonstrates practical skills in:

* Data preprocessing
* Machine learning model development
* API development
* Web application integration
* Model deployment
* GitHub project structuring
* End-to-end ML system design

---

# Author

**Olaoluwa Isaac**

Data Analyst | Machine Learning Enthusiast

GitHub:
https://github.com/yourusername
