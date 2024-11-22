from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class TransactionCreate(BaseModel):
    amount: float
    description: str | None
    transaction_type: TransactionType
    category_id: int


class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: str | None
    transaction_type: TransactionType
    transaction_date: datetime
    category_name: str

    class Config:
        from_attributes = True
