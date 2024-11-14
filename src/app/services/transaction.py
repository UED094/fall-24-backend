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
