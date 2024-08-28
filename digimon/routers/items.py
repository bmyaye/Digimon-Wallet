from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, Annotated
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship, func
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import models
from .. import deps

import math


router = APIRouter(prefix="/items", tags=["items"])

SIZE_PER_PAGE = 50


@router.get("")
async def read_items(
    session: Annotated[AsyncSession, Depends(models.get_session)],
    page: int = 1,
) -> models.ItemList:
    result = await session.exec(
        select(models.DBItem).offset((page - 1) * SIZE_PER_PAGE).limit(SIZE_PER_PAGE)
    )
    items = result.all()

    page_count = int(
        math.ceil(
            (await session.exec(select(func.count(models.DBItem.id)))).first()
            / SIZE_PER_PAGE
        )
    )

    print("page_count", page_count)
    print("items", items)

    return models.ItemList.from_orm(dict(items=items, page_count=page_count, page=page, size_per_page=SIZE_PER_PAGE))


@router.post("")
async def create_item(
    item: models.CreatedItem,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
) -> models.Item | None:
    # print("create_item", item)
    data = item.dict()
    dbitem = models.DBItem(**data)
    session.add(dbitem)
    await session.commit()
    await session.refresh(dbitem)

    return models.Item.from_orm(dbitem)


@router.get("/{item_id}")
async def read_item(
    item_id: int, 
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.Item:
    db_item = await session.get(models.DBItem, item_id)
    if db_item:
        return models.Item.from_orm(db_item)
    
    raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{item_id}")
async def update_item(
    item_id: int,
    item: models.UpdatedItem,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
) -> models.Item:
    print("update_item", item)
    data = item.dict()
    db_item = await session.get(models.DBItem, item_id)
    db_item.sqlmodel_update(data)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)

    return models.Item.from_orm(db_item)


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
) -> dict:
    db_item = await session.get(models.DBItem, item_id)
    await session.delete(db_item)
    await session.commit()

    return dict(message="delete success")
