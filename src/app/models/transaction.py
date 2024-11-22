import enum
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.core.database import Base


class TransactionType(enum.Enum):
    income = "income"
    expense = "expense"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    transaction_date = Column(DateTime, default=datetime.now(UTC))
    transaction_type = Column(Enum(TransactionType))

    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

    @hybrid_property
    def category_name(self):
        return self.category.category_name
