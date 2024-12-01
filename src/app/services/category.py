from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.category import CategoryBase, CategoryCreate
from app.schemas.transaction import TransactionType


def get_categories(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()


def get_categories_by_user_id(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()


def create_category(db: Session, category: CategoryCreate, user_id: int):
    db_category = Category(
        category_name=category.category_name,
        category_type=category.category_type,
        user_id=user_id,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category_by_id(db: Session, category_id: int, user_id: int):
    return (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == user_id)
        .first()
    )


def update_category_by_id(
    db: Session, category_id: int, category: CategoryBase, user_id: int
):
    db_category = get_category_by_id(db, category_id, user_id)
    if db_category is None:
        return None
    for key, value in category.model_dump().items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category_by_id(db: Session, category_id: int, user_id: int):
    db.query(Category).filter(
        Category.id == category_id, Category.user_id == user_id
    ).delete()
    db.commit()


def get_category_metrics(db: Session, user_id: int):
    """
    Calculate total income and expense metrics grouped by category

    Args:
        db (Session): Database session
        user_id (int): ID of the user

    Returns:
        dict: Metrics for income and expense categories
    """
    # Metrics for income categories
    income_categories = (
        db.query(
            Category.category_name, func.sum(Transaction.amount).label("total_amount")
        )
        .join(Transaction, Category.id == Transaction.category_id)
        .filter(
            Category.user_id == user_id,
            Category.category_type == TransactionType.income,
            Transaction.user_id == user_id,
        )
        .group_by(Category.category_name)
        .all()
    )

    # Metrics for expense categories
    expense_categories = (
        db.query(
            Category.category_name, func.sum(Transaction.amount).label("total_amount")
        )
        .join(Transaction, Category.id == Transaction.category_id)
        .filter(
            Category.user_id == user_id,
            Category.category_type == TransactionType.expense,
            Transaction.user_id == user_id,
        )
        .group_by(Category.category_name)
        .all()
    )

    return {
        "income_categories": [
            {"name": cat.category_name, "total": round(abs(cat.total_amount), 2)}
            for cat in income_categories
        ],
        "expense_categories": [
            {"name": cat.category_name, "total": round(abs(cat.total_amount), 2)}
            for cat in expense_categories
        ],
    }
