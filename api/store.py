"""
    Use store as Dashboard for user
"""

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from database import get_db_session
from models import Store, User
from schemas.store import CreateStoreSchema, StoreResponseSchema, StoreUpdateSchema
from utils import get_current_user

store_router = APIRouter(prefix="/store", tags=['Store'])


@store_router.get("/{store_id}", response_model=StoreResponseSchema)
def get_store(store_id: str, current_user: User = Depends(get_current_user)):
    with get_db_session() as db_session:
        store: Store = db_session.get(Store, store_id)
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Store '{store_id}' cannot be found.",
            )
        return store.to_json()


@store_router.post("", response_model=StoreResponseSchema)
def create_store(store_data: CreateStoreSchema, current_user: User = Depends(get_current_user)):
    with get_db_session() as db_session:
        existing_store = db_session.query(Store).filter_by(title=store_data.title).first()
        if existing_store:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User '{current_user.user_name}' has already one store created.",
            )
        store = Store(**store_data.dict())
        store.user = current_user
        db_session.add(store)
        db_session.commit()

        return store.to_json()


@store_router.delete("/{store_id}", status_code=202)
def delete_store(store_id: str, current_user: User = Depends(get_current_user)):
    with get_db_session() as db_session:
        store: Store = db_session.get(Store, store_id)
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Store '{store_id}' cannot be found.",
            )
        db_session.delete(store)
        db_session.commit()

        return store.to_json()


@store_router.patch("/{store_id}")
def update_store(store_id: str, update_store_data: StoreUpdateSchema, current_user: User = Depends(get_current_user)):
    with get_db_session() as db_session:
        store: Store = db_session.get(Store, store_id)
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Store '{store_id}' cannot be found.",
            )

        store.description = update_store_data.description
        db_session.commit()

        return store.to_json()
