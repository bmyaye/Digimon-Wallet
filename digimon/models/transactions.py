from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship

from . import items
from . import merchants
from . import wallets
from . import users


class BaseTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sender: int
    receiver: int
    amount: float
    user_id: int | None = 0


class CreatedTransaction(BaseTransaction):
    pass


class UpdatedTransaction(BaseTransaction):
    pass


class Transaction(BaseTransaction):
    id: int



class DBTransaction(Transaction, SQLModel, table=True):
    __tablename = "transaction"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()


class TransactionList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transactions: list[Transaction]
    page: int
    page_count: int
    size_per_page: int
