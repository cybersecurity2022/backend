from fastapi import APIRouter

item_router = APIRouter(prefix="/item", tags=['Item'])

# @item_router.post("")