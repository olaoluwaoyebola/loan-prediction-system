# Loan Approval Prediction System

### End-to-End Machine Learning Project (SQL → FastAPI → Streamlit)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Scikit-Learn](https://img.shields.io/badge/ScikitLearn-ML-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Project-Active-success)

---

## Quick Start

```bash
git clone https://github.com/olaoluwaoyebola/loan-prediction-system.git
cd loan-prediction-system
python -m venv venv && venv\Scripts\activate     # Windows
pip install -r requirements.txt
# 1. Run notebook/Loan_Prediction_model.ipynb to generate model files
# 2. Start the API
uvicorn backend.main:app --reload
# 3. In a new terminal, launch the frontend
streamlit run frontend/app.py
```

---

## Prerequisites

* **Python 3.10+**
* **pip** (comes with Python)
* **Dataset** — download from the link below and place it in `data/loan.csv`

---

## Dataset

📂 [Download the loan dataset from Google Drive](https://drive.google.com/file/d/1RCaK2-LYD3NLHEzcmk9pOAr8N0c_gnk4/view?usp=sharing)

> **Note:** The `data/` and `model/` directories are git-ignored. After cloning you must download the dataset and run the training notebook before the API will work.

---

# Project Overview

This project implements a **complete end-to-end machine learning system** for predicting whether a loan application should be **approved or rejected**.

The project simulates a **real-world ML deployment pipeline**, covering:

* Data ingestion and storage using SQL
* Machine learning model training using Scikit-Learn **Pipelines**
* Feature engineering and automated preprocessing
* Multi-model comparison with cross-validation
* Hyperparameter tuning via GridSearchCV
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
Feature Engineering          ← Computes TotalIncome, EMI,
(backend/prediction.py)        BalanceIncome, log transforms
        │
        ▼
Sklearn Pipeline (.pkl)      ← Preprocessing + Classifier
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
│   └── Loan_Prediction_model.ipynb
│
├── model/
│   ├── loan_model.pkl          ← Full sklearn Pipeline (preprocessor + classifier)
│   ├── loan_columns.pkl        ← List of expected feature column names
│   └── metrics.pkl             ← Dict of evaluation metrics
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── prediction.py           ← Includes server-side feature engineering
│
├── frontend/
│   └── app.py
│
├── .env.example
├── requirements.txt
├── LICENSE
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
notebook/Loan_Prediction_model.ipynb
```

### Training Pipeline

The notebook implements a **production-ready, reproducible ML workflow**:

1. Data Loading & Exploration
2. Exploratory Data Analysis (EDA) with visualizations
3. Feature Engineering — derives predictive features from raw inputs
4. Preprocessing via `sklearn.Pipeline` and `ColumnTransformer` (prevents data leakage)
5. Stratified Train/Test Split
6. Multi-Model Comparison with Stratified 5-Fold Cross-Validation
7. Hyperparameter Tuning via `GridSearchCV`
8. Final Evaluation on held-out test set
9. Model & Metrics Serialization

### Engineered Features

The following features are computed from the raw dataset and significantly boost prediction accuracy:

| Feature          | Formula                                        |
| ---------------- | ---------------------------------------------- |
| `TotalIncome`    | `ApplicantIncome + CoapplicantIncome`           |
| `EMI`            | `LoanAmount / Loan_Amount_Term`                 |
| `BalanceIncome`  | `TotalIncome - (EMI × 1000)`                    |
| `Log_TotalIncome`| `log1p(TotalIncome)`                            |
| `Log_LoanAmount` | `log1p(LoanAmount)`                             |

> The raw columns `ApplicantIncome`, `CoapplicantIncome`, and `LoanAmount` are dropped after engineering since they are represented by the derived features.

### Preprocessing Pipeline

```text
sklearn Pipeline (ColumnTransformer → Classifier)
     ├── Numeric features  → SimpleImputer(median) → StandardScaler
     └── Categorical features → SimpleImputer(most_frequent) → OrdinalEncoder
```

The **entire pipeline** (preprocessing + model) is serialized to a single `.pkl` file. This eliminates data leakage and makes deployment trivial.

### Models Compared

| Model                  | Cross-Validation Metric |
| ---------------------- | ----------------------- |
| Logistic Regression    | F1 (5-Fold CV)          |
| Random Forest          | F1 (5-Fold CV)          |
| Gradient Boosting      | F1 (5-Fold CV)          |
| SVM                    | F1 (5-Fold CV)          |

The best-performing model is selected automatically and tuned with `GridSearchCV`.

### Model Performance

The trained model achieves the following metrics on the held-out test set:

| Metric    | Score  |
| --------- | ------ |
| Accuracy  | ~85.4% |
| F1 Score  | ~90.3% |
| Precision | ~83.2% |
| Recall    | ~98.8% |
| ROC-AUC   | ~77.0% |

> Full evaluation details (classification report, confusion matrix, feature importances) are available in the training notebook. Metrics are also saved to `model/metrics.pkl`.

### Model Artifacts

After running the notebook, three files are generated:

| File                | Contents                                          |
| ------------------- | ------------------------------------------------- |
| `loan_model.pkl`    | Full sklearn Pipeline (preprocessor + classifier) |
| `loan_columns.pkl`  | Ordered list of feature column names              |
| `metrics.pkl`       | Dictionary of evaluation metrics                  |

---

# Backend API (FastAPI)

FastAPI serves the trained model as a **REST API**.

Main API file:

```
backend/main.py
```

### Server-Side Feature Engineering

The backend implements **Option A** from the model rebuild strategy: the API schema accepts the **original raw fields** (ApplicantIncome, CoapplicantIncome, LoanAmount), and the backend computes the engineered features (`TotalIncome`, `EMI`, `BalanceIncome`, `Log_TotalIncome`, `Log_LoanAmount`) inside `prediction.py` before passing data to the model.

This means the **frontend and API contract remain unchanged** — callers send the same raw fields they always have, and the feature engineering is handled transparently on the server.

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

The application features a **multi-step form** with three stages:

1. **Personal Information** — Gender, Married, Dependents, Education
2. **Employment Information** — Self Employed, Applicant Income, Coapplicant Income
3. **Financial Information** — Loan Amount, Loan Term, Credit History, Property Area

Users progress through each step, and upon submission the app sends the data to the FastAPI backend and displays an instant approval/rejection result.

---

# Installation Guide

### 1. Clone the Repository

```
git clone https://github.com/olaoluwaoyebola/loan-prediction-system.git
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

### 4. Configure Environment (Optional)

Copy the example environment file and adjust if needed:

```
cp .env.example .env
```

The `.env` file lets you configure the API URL used by the Streamlit frontend.

---

# Running the Project

### Step 1 — Train the Model

Open the notebook:

```
notebook/Loan_Prediction_model.ipynb
```

Run all cells to generate:

```
model/loan_model.pkl
model/loan_columns.pkl
model/metrics.pkl
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
2. User inputs applicant information across three form steps
3. Data is sent to FastAPI as a JSON payload
4. FastAPI computes engineered features (TotalIncome, EMI, etc.)
5. Engineered data is passed to the sklearn Pipeline for prediction
6. Result returned to Streamlit UI (Approved ✅ or Rejected ❌)

---

# Possible Future Improvements

* Deploy FastAPI on **Render or Railway**
* Deploy Streamlit on **Streamlit Cloud**
* Add **Docker containerization**
* Implement **model monitoring and logging**
* Add a **model evaluation metrics dashboard** in the frontend
* Implement **A/B testing** for model versions

---

# Skills Demonstrated

This project demonstrates practical skills in:

* Data preprocessing and feature engineering
* Scikit-Learn Pipelines and ColumnTransformers
* Multi-model comparison and hyperparameter tuning
* Machine learning model development and evaluation
* API development with FastAPI
* Web application integration with Streamlit
* Server-side feature transformation
* Model deployment and serialization
* GitHub project structuring
* End-to-end ML system design

---

# License

This project is licensed under the [MIT License](LICENSE).

---

# Author

**Olaoluwa Isaac**

Data Analyst | Machine Learning Enthusiast

GitHub: [olaoluwaoyebola](https://github.com/olaoluwaoyebola)
