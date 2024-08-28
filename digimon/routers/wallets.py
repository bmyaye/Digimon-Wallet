from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Annotated
from sqlmodel import Field, SQLModel, create_engine, Session, select

from .. import models
from .. import deps


router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.get("")
async def read_wallets() -> models.WalletList:
    with Session(models.engine) as session:
        wallets = session.exec(select(models.DBWallet)).all()

    return models.WalletList.from_orm(dict(wallets=wallets, page_size=0, page=0, size_per_page=0))


@router.post("")
async def create_wallet(
    wallet: models.CreatedWallet,
    session: Annotated[models.AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
) -> models.Wallet:
    data = wallet.dict()
    dbwallet = models.DBWallet.parse_obj(data)
    dbwallet.user = current_user
    with Session(models.engine) as session:
        session.add(dbwallet)
        session.commit()
        session.refresh(dbwallet)

    return models.Wallet.from_orm(dbwallet)


@router.get("/{wallet_id}")
async def read_wallet(wallet_id: int) -> models.Wallet:
    with Session(models.engine) as session:
        db_wallet = session.get(models.DBWallet, wallet_id)
        if db_wallet:
            return models.Wallet.from_orm(db_wallet)
    raise HTTPException(status_code=404, detail="Wallet not found")


@router.put("/{wallet_id}")
async def update_wallet(
    wallet_id: int,
    wallet: models.UpdatedWallet,
    session: Annotated[models.AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
) -> models.Wallet:
    data = wallet.dict()
    with Session(models.engine) as session:
        db_wallet = session.get(models.DBWallet, wallet_id)
        db_wallet.sqlmodel_update(data)
        session.add(db_wallet)
        session.commit()
        session.refresh(db_wallet)

    return models.Wallet.from_orm(db_wallet)


@router.delete("/{wallet_id}")
async def delete_wallet(
    wallet_id: int,
    session: Annotated[models.AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
) -> dict:
    with Session(models.engine) as session:
        db_wallet = session.get(models.DBWallet, wallet_id)
        session.delete(db_wallet)
        session.commit()

    return dict(message="delete success")