from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate


# Transaction CRUD
def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(**transaction.model_dump(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()


def get_transaction(db: Session, transaction_id: int, user_id: int):
    return (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id, Transaction.user_id == user_id)
        .first()
    )


def update_transaction(
    db: Session, transaction_id: int, transaction: TransactionCreate, user_id: int
):
    db.query(Transaction).filter(
        Transaction.id == transaction_id, Transaction.user_id == user_id
    ).update(transaction.model_dump())
    db.commit()
    return (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id, Transaction.user_id == user_id)
        .first()
    )


def delete_transaction(db: Session, transaction_id: int, user_id: int):
    db.query(Transaction).filter(
        Transaction.id == transaction_id, Transaction.user_id == user_id
    ).delete()
    db.commit()
    return True


def get_transaction_metrics(db: Session, user_id: int):
    """
    Calculate total balance, income, and expenses for a user

    Args:
        db (Session): Database session
        user_id (int): ID of the user

    Returns:
        dict: Dictionary containing total balance, income, and expenses
    """
    # Calculate total income (positive transactions)
    total_income = (
        db.query(func.sum(Transaction.amount))
        .filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "income",
        )
        .scalar()
        or 0
    )

    # Calculate total expenses (negative transactions)
    total_expenses = (
        db.query(func.sum(Transaction.amount))
        .filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "expense",
        )
        .scalar()
        or 0
    )

    # Calculate total balance (sum of all transactions)
    total_balance = total_income - total_expenses

    return {
        "total_balance": round(total_balance, 2),
        "total_income": round(total_income, 2),
        "total_expenses": round(abs(total_expenses), 2),
    }
