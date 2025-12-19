from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ExpenseCreate(BaseModel):
    """Request model for creating expense"""
    description: str
    amount: float = Field(gt=0)
    paid_by: str
    split_between: str  # Comma-separated: "Alice,Bob,Charlie"
    category: str = Field(default="General")

class ExpenseUpdate(BaseModel):
    """Request model for updating expense"""
    description: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    paid_by: Optional[str] = None
    split_between: Optional[str] = None
    category: Optional[str] = None

class ExpenseResponse(BaseModel):
    """Response model for expense"""
    id: int
    description: str
    amount: float
    paid_by: str
    split_between: str
    category: str
    created_at: str

class SettlementRecord(BaseModel):
    """Response model for settlement details"""
    debtor: str  # Person who owes money
    creditor: str  # Person who should receive money
    amount: float  # Amount owed

class UserSummary(BaseModel):
    """Summary of a user's balance"""
    name: str
    total_paid: float
    total_owed: float
    balance: float  # Positive = owed money, Negative = owes money
