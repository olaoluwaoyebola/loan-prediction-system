# pydantic for data validation and settings management library
# basemodel for schema definition

from pydantic import BaseModel, Field


class LoanRequest(BaseModel):
    """Schema for incoming loan prediction requests with validation bounds."""

    # Personal Information
    Gender: int = Field(..., ge=0, le=1, description="0 = Male, 1 = Female")
    Married: int = Field(..., ge=0, le=1, description="0 = No, 1 = Yes")
    Dependents: int = Field(..., ge=0, le=5, description="Number of dependents (0-5)")
    Education: int = Field(..., ge=0, le=1, description="0 = Graduate, 1 = Undergraduate")

    # Employment Information
    Self_Employed: int = Field(..., ge=0, le=1, description="0 = No, 1 = Yes")
    ApplicantIncome: float = Field(..., ge=0, description="Primary applicant income")
    CoapplicantIncome: float = Field(..., ge=0, description="Co-applicant income")

    # Financial Information
    LoanAmount: float = Field(..., gt=0, description="Loan amount requested (in thousands)")
    Loan_Amount_Term: float = Field(..., gt=0, description="Loan repayment term in months")
    Credit_History: float = Field(..., ge=0, le=1, description="0 = No history, 1 = Has history")
    Property_Area: int = Field(..., ge=0, le=2, description="0 = Urban, 1 = Semiurban, 2 = Rural")


class LoanResponse(BaseModel):
    """Schema for the prediction response."""

    prediction: int = Field(..., ge=0, le=1, description="1 = Approved, 0 = Rejected")