from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.ticker import TickerData

from ..schemas.schemas import *

async def read_crypto_data( query_input: TickerRequest, db: AsyncSession ) -> TickerResponse:
    data = await db.execute(select(TickerData).where(TickerData.ticker == query_input.ticker).order_by(TickerData.timestamp.desc()))
    result = data.scalars().first()
    return TickerResponse.model_validate({
        "ticker": result.ticker,
        "price": result.price,
        "timestamp": result.timestamp
    })


async def read_crypto_all_data( query_input: TickerRequest, db: AsyncSession ) -> TickerResponseList:
    query = select(TickerData).where(TickerData.ticker == query_input.ticker)
    data = await db.execute(query)
    result = data.scalars().all()
    return list(TickerResponse.model_validate({
        "ticker": res.ticker,
        "price": res.price,
        "timestamp": res.timestamp
    }) for res in result )



async def read_crypto_by_stamp( query_input: TickerRequest, db: AsyncSession) -> TickerResponse:
    query = select(TickerData).where(TickerData.ticker == query_input.ticker).where(TickerData.timestamp == query_input.timestamp)
    data = await db.execute(query)
    result = data.scalars().first()
    return TickerResponse.model_validate({
            "ticker": result.ticker,
            "price": result.price,
            "timestamp": result.timestamp
        })