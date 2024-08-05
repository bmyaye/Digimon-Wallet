from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select

from . import items
from . import merchants
from . import transactions


class BaseWallet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    owner: str
    balance: float


class CreatedWallet(BaseWallet):
    pass


class UpdatedWallet(BaseWallet):
    pass


class Wallet(BaseWallet):
    id: int



class DBWallet(Wallet, SQLModel, table=True):
    __tablename = "wallet"
    id: Optional[int] = Field(default=None, primary_key=True)


class WalletList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    wallets: list[Wallet]
    page: int
    page_size: int
    size_per_page: int