from pydantic import BaseModel

from app.schemas.transaction import TransactionType


class CategoryBase(BaseModel):
    category_name: str
    category_type: TransactionType


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True
