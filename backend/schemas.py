# pydantic for data validation and settings management library
# basemodel for schema definition

from pydantic import BaseModel

class PersonalInformation(BaseModel):
    Gender: int
    Married: int
    Dependents: int
    Education: int

class EmploymentInformation(BaseModel):
    Self_Employed: int
    ApplicantIncome: float
    CoapplicantIncome: float

class FinancialInformation(BaseModel):
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: int

class LoanRequest(BaseModel):
    # Personal Information
    Gender: int
    Married: int
    Dependents: int
    Education: int
    
    # Employment Information
    Self_Employed: int
    ApplicantIncome: float
    CoapplicantIncome: float
    
    # Financial Information
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: int