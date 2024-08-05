from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select

from . import items
from . import merchants
from . import wallets


class BaseTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sender: str
    receiver: str
    amount: float


class CreatedTransaction(BaseTransaction):
    pass


class UpdatedTransaction(BaseTransaction):
    pass


class Transaction(BaseTransaction):
    id: int



class DBTransaction(Transaction, SQLModel, table=True):
    __tablename = "transaction"
    id: Optional[int] = Field(default=None, primary_key=True)


class TransactionList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transactions: list[Transaction]
    page: int
    page_size: int
    size_per_page: int