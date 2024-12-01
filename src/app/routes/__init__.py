from fastapi import APIRouter

from app.routes import category, transaction, user

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(category.router, prefix="/categories", tags=["Categories"])
api_router.include_router(
    transaction.router, prefix="/transactions", tags=["Transactions"]
)
