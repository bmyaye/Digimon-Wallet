# from fastapi import FastAPI, HTTPException
# from typing import Optional
# from pydantic import BaseModel, ConfigDict
# from sqlmodel import Field, SQLModel, create_engine, Session, select

# class BaseMerchant(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     name: str
#     description: str | None = None
#     merchant_type: str
#     location: str

# class BaseWallet(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     owner: str
#     balance: float

# class BaseTransaction(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     sender: str
#     receiver: str
#     amount: float

# class BaseItem(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     name: str
#     description: str | None = None
#     price: float = 0.00
#     tax: float | None = None
#     merchant_id: int | None = None


# class CreatedItem(BaseItem):
#     pass

# class UpdatedItem(BaseItem):
#     pass


# class CreatedMerchant(BaseMerchant):
#     pass

# class UpdatedMerchant(BaseMerchant):
#     pass


# class CreatedWallet(BaseWallet):
#     pass

# class UpdatedWallet(BaseWallet):
#     pass


# class CreatedTransaction(BaseTransaction):
#     pass

# class UpdatedTransaction(BaseTransaction):
#     pass


# class Wallet(BaseWallet):
#     id: int

# class Merchant(BaseMerchant):
#     id: int

# class Transaction(BaseTransaction):
#     id: int

# class Item(BaseItem):
#     id: int
#     merchant_id: int


# class DBItem(Item, SQLModel, table=True):
#     __tablename = "item"
#     id: Optional[int] = Field(default=None, primary_key=True)
#     merchant_id: Optional[int] = Field(default=None, foreign_key="merchant.id")

# class DBMerchant(Merchant, SQLModel, table=True):
#     __tablename = "merchant"
#     id: Optional[int] = Field(default=None, primary_key=True)

# class DBWallet(Wallet, SQLModel, table=True):
#     __tablename = "wallet"
#     id: Optional[int] = Field(default=None, primary_key=True)

# class DBTransaction(Transaction, SQLModel, table=True):
#     __tablename = "transaction"
#     id: Optional[int] = Field(default=None, primary_key=True)


# class ItemList(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     items: list[Item]
#     page: int
#     page_size: int
#     size_per_page: int

# class MerchantList(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     merchants: list[Merchant]
#     page: int
#     page_size: int
#     size_per_page: int

# class WalletList(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     wallets: list[Wallet]
#     page: int
#     page_size: int
#     size_per_page: int

# class TransactionList(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     transactions: list[Transaction]
#     page: int
#     page_size: int
#     size_per_page: int


# connect_args = {}


# engine = create_engine(
#     "postgresql+pg8000://postgres:123456@localhost/digimondb",
#     echo=True,
#     connect_args=connect_args,
# )


# SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# app = FastAPI()


# @app.get("/")
# def root():
#     return {"message": "Hello World"}


# @app.get("/items")
# async def read_items() -> ItemList:
#     with Session(engine) as session:
#         items = session.exec(select(DBItem)).all()

#     return ItemList.from_orm(dict(items=items, page_size=0, page=0, size_per_page=0))

# @app.post("/items")
# async def create_item(item: CreatedItem) -> Item:
#     print("create_item", item)
#     data = item.dict()
#     dbitem = DBItem(**data)
#     with Session(engine) as session:
#         session.add(dbitem)
#         session.commit()
#         session.refresh(dbitem)

#     # return Item.parse_obj(dbitem.dict())
#     return Item.from_orm(dbitem)

# @app.get("/items/{item_id}")
# async def read_item(item_id: int) -> Item:
#     with Session(engine) as session:
#         db_item = session.get(DBItem, item_id)
#         if db_item:
#             return Item.from_orm(db_item)
#     raise HTTPException(status_code=404, detail="Item not found")


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: UpdatedItem) -> Item:
#     print("update_item", item)
#     data = item.dict()
#     with Session(engine) as session:
#         db_item = session.get(DBItem, item_id)
#         db_item.sqlmodel_update(data)
#         session.add(db_item)
#         session.commit()
#         session.refresh(db_item)

#     return Item.from_orm(db_item)

# @app.delete("/items/{item_id}")
# async def delete_item(item_id: int) -> dict:
#     with Session(engine) as session:
#         db_item = session.get(DBItem, item_id)
#         session.delete(db_item)
#         session.commit()

#     return dict(message="delete success")


# @app.get("/merchants")
# async def read_merchants() -> MerchantList:
#     with Session(engine) as session:
#         merchants = session.exec(select(DBMerchant)).all()

#     return MerchantList.from_orm(dict(merchants=merchants, page_size=0, page=0, size_per_page=0))

# @app.post("/merchants")
# async def create_merchant(merchant: CreatedMerchant) -> Merchant:
#     data = merchant.dict()
#     dbmerchant = DBMerchant(**data)
#     with Session(engine) as session:
#         session.add(dbmerchant)
#         session.commit()
#         session.refresh(dbmerchant)

#     return Merchant.from_orm(dbmerchant)

# @app.get("/merchants/{merchant_id}")
# async def read_merchant(merchant_id: int) -> Merchant:
#     with Session(engine) as session:
#         db_merchant = session.get(DBMerchant, merchant_id)
#         if db_merchant:
#             return Merchant.from_orm(db_merchant)
#     raise HTTPException(status_code=404, detail="Merchant not found")

# @app.put("/merchants/{merchant_id}")
# async def update_merchant(merchant_id: int, merchant: UpdatedMerchant) -> Merchant:
#     data = merchant.dict()
#     with Session(engine) as session:
#         db_merchant = session.get(DBMerchant, merchant_id)
#         db_merchant.sqlmodel_update(data)
#         session.add(db_merchant)
#         session.commit()
#         session.refresh(db_merchant)

#     return Merchant.from_orm(db_merchant)

# @app.delete("/merchants/{merchant_id}")
# async def delete_merchant(merchant_id: int) -> dict:
#     with Session(engine) as session:
#         db_merchant = session.get(DBMerchant, merchant_id)
#         session.delete(db_merchant)
#         session.commit()

#     return dict(message="delete success")


# @app.get("/wallets")
# async def read_wallets() -> WalletList:
#     with Session(engine) as session:
#         wallets = session.exec(select(DBWallet)).all()

#     return WalletList.from_orm(dict(wallets=wallets, page_size=0, page=0, size_per_page=0))

# @app.post("/wallets")
# async def create_wallet(wallet: CreatedWallet) -> Wallet:
#     data = wallet.dict()
#     dbwallet = DBWallet(**data)
#     with Session(engine) as session:
#         session.add(dbwallet)
#         session.commit()
#         session.refresh(dbwallet)

#     return Wallet.from_orm(dbwallet)

# @app.get("/wallets/{wallet_id}")
# async def read_wallet(wallet_id: int) -> Wallet:
#     with Session(engine) as session:
#         db_wallet = session.get(DBWallet, wallet_id)
#         if db_wallet:
#             return Wallet.from_orm(db_wallet)
#     raise HTTPException(status_code=404, detail="Wallet not found")

# @app.put("/wallets/{wallet_id}")
# async def update_wallet(wallet_id: int, wallet: UpdatedWallet) -> Wallet:
#     data = wallet.dict()
#     with Session(engine) as session:
#         db_wallet = session.get(DBWallet, wallet_id)
#         db_wallet.sqlmodel_update(data)
#         session.add(db_wallet)
#         session.commit()
#         session.refresh(db_wallet)

#     return Wallet.from_orm(db_wallet)

# @app.delete("/wallets/{wallet_id}")
# async def delete_wallet(wallet_id: int) -> dict:
#     with Session(engine) as session:
#         db_wallet = session.get(DBWallet, wallet_id)
#         session.delete(db_wallet)
#         session.commit()

#     return dict(message="delete success")


# @app.get("/transactions")
# async def read_transactions() -> TransactionList:
#     with Session(engine) as session:
#         transactions = session.exec(select(DBTransaction)).all()

#     return TransactionList.from_orm(dict(transactions=transactions, page_size=0, page=0, size_per_page=0))

# @app.post("/transactions")
# async def create_transaction(transaction: CreatedTransaction) -> Transaction:
#     data = transaction.dict()
#     dbtransaction = DBTransaction(**data)
#     with Session(engine) as session:
#         session.add(dbtransaction)
#         session.commit()
#         session.refresh(dbtransaction)

#     return Transaction.from_orm(dbtransaction)

# @app.get("/transactions/{transaction_id}")
# async def read_transaction(transaction_id: int) -> Transaction:
#     with Session(engine) as session:
#         db_transaction = session.get(DBTransaction, transaction_id)
#         if db_transaction:
#             return Transaction.from_orm(db_transaction)
#     raise HTTPException(status_code=404, detail="Transaction not found")

# @app.put("/transactions/{transaction_id}")
# async def update_transaction(transaction_id: int, transaction: UpdatedTransaction) -> Transaction:
#     data = transaction.dict()
#     with Session(engine) as session:
#         db_transaction = session.get(DBTransaction, transaction_id)
#         db_transaction.sqlmodel_update(data)
#         session.add(db_transaction)
#         session.commit()
#         session.refresh(db_transaction)

#     return Transaction.from_orm(db_transaction)

# @app.delete("/transactions/{transaction_id}")
# async def delete_transaction(transaction_id: int) -> dict:
#     with Session(engine) as session:
#         db_transaction = session.get(DBTransaction, transaction_id)
#         session.delete(db_transaction)
#         session.commit()

#     return dict(message="delete success")