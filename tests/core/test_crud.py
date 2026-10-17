import fastapi
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.crud import read_crypto_data, read_crypto_all_data
from src.models.ticker import TickerData
from src.schemas.schemas import TickerRequest


@pytest.mark.asyncio
async def test_read_crypto_all_data(get_test_db: AsyncSession):
 
    get_test_db.add_all([
        TickerData(ticker="btc_usd", price=10.0, timestamp=100),
        TickerData(ticker="btc_usd", price=20.0, timestamp=200),
        TickerData(ticker="eth_usd", price=5.0, timestamp=300),
    ])
    await get_test_db.commit()

    request = TickerRequest(ticker="btc_usd", timestamp=None)
    result = await read_crypto_all_data(request, get_test_db)

    assert len(result) == 2
    assert all(r.ticker == "btc_usd" for r in result)


@pytest.mark.asyncio
async def test_read_crypto_data_latest(get_test_db: AsyncSession):
    get_test_db.add_all([
        TickerData(ticker="eth_usd", price=100.0, timestamp=1000),
        TickerData(ticker="eth_usd", price=300.0, timestamp=3000),
        TickerData(ticker="eth_usd", price=200.0, timestamp=2000),
    ])
    await get_test_db.commit()

    request = TickerRequest(ticker="eth_usd", timestamp=None)
    result = await read_crypto_data(request, get_test_db)

    assert result.price == 300.0
    assert result.timestamp == 3000


@pytest.mark.asyncio
async def test_read_crypto_all_data_empty(get_test_db: AsyncSession):
    request = TickerRequest(ticker="btc_usd", timestamp=None)
    result = await read_crypto_all_data(request, get_test_db)

    assert result == []
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_read_crypto_data_latest_not_found(get_test_db: AsyncSession):
    request = TickerRequest(ticker="btc_usd", timestamp=None)
    try:
        result = await read_crypto_data(request, get_test_db)
    except fastapi.HTTPException as e:
        assert e.status_code == 404