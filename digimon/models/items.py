from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select

from . import merchants
from . import wallets
from . import transactions


class BaseItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str | None = None
    price: float = 0.00
    tax: float | None = None
    merchant_id: int | None = None


class CreatedItem(BaseItem):
    pass


class UpdatedItem(BaseItem):
    pass


class Item(BaseItem):
    id: int
    merchant_id: int


class DBItem(Item, SQLModel, table=True):
    __tablename = "item"
    id: Optional[int] = Field(default=None, primary_key=True)
    merchant_id: Optional[int] = Field(default=None, foreign_key="merchant.id")


class ItemList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: list[Item]
    page: int
    page_size: int
    size_per_page: int
