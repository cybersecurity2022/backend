from typing import Optional

from pydantic import BaseModel


class CreateStoreSchema(BaseModel):
    title: str
    description: Optional[str]


class StoreResponseSchema(BaseModel):
    id: str
    title: str
    description: Optional[str]


class StoreUpdateSchema(BaseModel):
    description: str
