from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.services.category as category_service
from app.core.auth import decode_access_token, oauth2_scheme
from app.dependencies import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.user import get_user_by_username

router = APIRouter()


# Create a new category
@router.post("/", response_model=CategoryResponse)
def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    username = decode_access_token(token).username
    user = get_user_by_username(db, username)
    return category_service.create_category(db, category, user.id)


# Get all categories
@router.get("/", response_model=list[CategoryResponse])
def get_all_categories(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    username = decode_access_token(token).username
    user = get_user_by_username(db, username)
    return category_service.get_categories(db, user.id)


@router.get("/metrics")
def get_category_financial_metrics(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    username = decode_access_token(token).username
    user = get_user_by_username(db, username)
    return category_service.get_category_metrics(db, user.id)


# Get a category by ID
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_details(
    category_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    username = decode_access_token(token).username
    user = get_user_by_username(db, username)

    category = category_service.get_category_by_id(db, category_id, user.id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


# Update a category by ID
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category_details(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    username = decode_access_token(token).username
    user = get_user_by_username(db, username)

    category = category_service.update_category_by_id(
        db, category_id, category, user.id
    )
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


# Delete a category by ID
@router.delete("/{category_id}")
def delete_category(
    category_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    username = decode_access_token(token).username
    user = get_user_by_username(db, username)

    category = category_service.get_category_by_id(db, category_id, user.id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    category_service.delete_category_by_id(db, category_id, user.id)
    return {"message": "Category deleted successfully"}
