from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship

from . import items
from . import wallets
from . import transactions
from . import users


class BaseMerchant(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str | None = None
    merchant_type: str
    location: str
    user_id: int | None = 0


class CreatedMerchant(BaseMerchant):
    pass


class UpdatedMerchant(BaseMerchant):
    pass


class Merchant(BaseMerchant):
    id: int


class DBMerchant(Merchant, SQLModel, table=True):
    __tablename = "merchant"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()


class MerchantList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    merchants: list[Merchant]
    page: int
    page_count: int
    size_per_page: int
