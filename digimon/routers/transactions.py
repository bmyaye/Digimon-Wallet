from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Annotated
from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import models
from .. import deps


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("")
async def read_transactions() -> models.TransactionList:
    with Session(models.engine) as session:
        transactions = session.exec(select(models.DBTransaction)).all()

    return models.TransactionList.from_orm(dict(transactions=transactions, page_size=0, page=0, size_per_page=0))


@router.post("")
async def create_transaction(
    transaction: models.CreatedTransaction,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
) -> models.Transaction:
    data = transaction.dict()
    dbtransaction = models.DBTransaction.parse_obj(data)
    dbtransaction.user = current_user
    with Session(models.engine) as session:
        session.add(dbtransaction)
        session.commit()
        session.refresh(dbtransaction)

    return models.Transaction.from_orm(dbtransaction)


@router.get("/{transaction_id}")
async def read_transaction(transaction_id: int) -> models.Transaction:
    with Session(models.engine) as session:
        db_transaction = session.get(models.DBTransaction, transaction_id)
        if db_transaction:
            return models.Transaction.from_orm(db_transaction)
    raise HTTPException(status_code=404, detail="Transaction not found")


@router.put("/{transaction_id}")
async def update_transaction(
    transaction_id: int,
    transaction: models.UpdatedTransaction,
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
) -> models.Transaction:
    data = transaction.dict()
    with Session(models.engine) as session:
        db_transaction = session.get(models.DBTransaction, transaction_id)
        db_transaction.sqlmodel_update(data)
        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction)

    return models.Transaction.from_orm(db_transaction)


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
) -> dict:
    with Session(models.engine) as session:
        db_transaction = session.get(models.DBTransaction, transaction_id)
        session.delete(db_transaction)
        session.commit()

    return dict(message="delete success")