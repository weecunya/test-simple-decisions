from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.crud import (
    read_crypto_by_stamp,
    read_crypto_data,
    read_crypto_all_data
)
from ..core.database import DatabaseManager
from ..schemas.schemas import (
    TickerResponse,
    TickerRequest
)
from ..core.config import Config

router = APIRouter()

config = Config()
db_manager = DatabaseManager(config.SQLALCHEMY_DATABASE_URL)


DbSession = Annotated[AsyncSession, Depends(db_manager.get_db)]


@router.get("/prices")
async def prices(
    db: DbSession,
    ticker: str = Query(...)
) -> list[TickerResponse]:
    data = await read_crypto_all_data(
        TickerRequest.model_validate({
            "ticker": ticker,
            "timestamp": None
            }), db)
    return data


@router.get("/prices/latest")
async def latest(
    db: DbSession,
    ticker: str = Query(...)
) -> TickerResponse:
    data = await read_crypto_data(
        TickerRequest.model_validate({
            "ticker": ticker,
            "timestamp": None
             }), db)
    return data


@router.get("/prices/filter")
async def filter(
    db: DbSession,
    ticker: str = Query(...),
    timestamp: str = Query(...)
) -> TickerResponse:
    data = await read_crypto_by_stamp(
        TickerRequest.model_validate({
            "ticker": ticker, 
            "timestamp": timestamp
            }), db)
    return data
    