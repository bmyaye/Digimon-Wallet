from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship

from . import items
from . import merchants
from . import transactions
from . import users


class BaseWallet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    owner: int
    balance: float
    user_id: int | None = 0


class CreatedWallet(BaseWallet):
    pass


class UpdatedWallet(BaseWallet):
    pass


class Wallet(BaseWallet):
    id: int



class DBWallet(Wallet, SQLModel, table=True):
    __tablename = "wallet"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()


class WalletList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    wallets: list[Wallet]
    page: int
    page_count: int
    size_per_page: int
