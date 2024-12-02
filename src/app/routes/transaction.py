import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.services.transaction as transaction_service
import app.services.user as user_service
from app.core.auth import decode_access_token, oauth2_scheme
from app.dependencies import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter()

logger = logging.getLogger("uvicorn")


@router.post("/", response_model=TransactionResponse)
def create_new_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    username = decode_access_token(token).username
    user_id = user_service.get_user_by_username(db, username).id

    return transaction_service.create_transaction(db, transaction, user_id)


@router.get("/", response_model=list[TransactionResponse])
def read_transactions(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    username = decode_access_token(token).username
    user_id = user_service.get_user_by_username(db, username).id
    return transaction_service.get_transactions(db, user_id)


@router.get("/metrics")
def get_transaction_metrics(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    logger.info("Getting transaction metrics")
    try:
        decoded_token = decode_access_token(token)
        username = decoded_token.username
        user = user_service.get_user_by_username(db, username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user_id = user.id
        logger.info(f"User {username} requested transaction metrics")
        return transaction_service.get_transaction_metrics(db, user_id)
    except Exception as e:
        (logger.error(f"Error getting transaction metrics: {e}"))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid token or data",
        )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    username = decode_access_token(token).username
    user_id = user_service.get_user_by_username(db, username).id
    return transaction_service.get_transaction(db, transaction_id, user_id)


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction_details(
    transaction_id: int,
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    username = decode_access_token(token).username
    user_id = user_service.get_user_by_username(db, username).id
    return transaction_service.update_transaction(
        db, transaction_id, transaction, user_id
    )


@router.delete("/{transaction_id}")
def delete_transaction_route(
    transaction_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    username = decode_access_token(token).username
    user_id = user_service.get_user_by_username(db, username).id
    return transaction_service.delete_transaction(db, transaction_id, user_id)
