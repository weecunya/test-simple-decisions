from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.crud import *
from ..core.database import DatabaseManager
from ..schemas.schemas import *
from ..core.config import Config

router = APIRouter()

config = Config()
db_manager = DatabaseManager(config.SQLALCHEMY_DATABASE_URL)


DbSession = Annotated[AsyncSession, Depends(db_manager.get_db)]


@router.get("/prices")
async def prices(
    ticker: str = Query(...),
    db: AsyncSession = Depends(db_manager.get_db)
) -> TickerResponseList:
    data = await read_crypto_all_data(
        TickerRequest.model_validate({
            "ticker": ticker,
            "timestamp": None
            }), db)
    return data


@router.get("/prices/latest")
async def latest(
    ticker: str = Query(...),
    db: AsyncSession = Depends(db_manager.get_db)
) -> TickerResponse:
    data = await read_crypto_data(
        TickerRequest.model_validate({
            "ticker": ticker,
            "timestamp": None
             }), db)
    return data


@router.get("/prices/filter")
async def filter(
    ticker: str = Query(...),
    timestamp: str = Query(...),
    db: AsyncSession = Depends(db_manager.get_db)
) -> TickerResponse:
    data = await read_crypto_by_stamp(
        TickerRequest.model_validate({
            "ticker": ticker, 
            "timestamp": timestamp
            }), db)
    return data
    