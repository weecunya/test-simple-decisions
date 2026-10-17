import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.ticker import TickerData
from src.api.endpoints import db_manager



# 1. Тесты для эндпоинта /api/prices 

@pytest.mark.asyncio
async def test_get_prices_success(async_test_client: AsyncClient, get_test_db: AsyncSession):
    get_test_db.add_all([
        TickerData(ticker="btc_usd", price=80000.0, timestamp=1700000000),
        TickerData(ticker="btc_usd", price=81000.0, timestamp=1700000060),
        TickerData(ticker="eth_usd", price=3000.0, timestamp=1700000000),
    ])
    await get_test_db.commit()

    response = await async_test_client.get("/api/prices", params={"ticker": "btc_usd"})

    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) == 2
    assert all(item["ticker"] == "btc_usd" for item in data)
    assert data[0]["price"] == 80000.0


@pytest.mark.asyncio
async def test_get_prices_empty_database(async_test_client: AsyncClient):
    response = await async_test_client.get("/api/prices", params={"ticker": "btc_usd"})
    
    assert response.status_code == 200
    assert response.json() == []


# 2. Тесты для эндпоинта /api/prices/latest 

@pytest.mark.asyncio
async def test_get_latest_price_sorting(async_test_client: AsyncClient, get_test_db: AsyncSession):
    get_test_db.add_all([
        TickerData(ticker="btc_usd", price=75000.0, timestamp=1000),  # Самая старая
        TickerData(ticker="btc_usd", price=82000.0, timestamp=3000),  # Самая свежая
        TickerData(ticker="btc_usd", price=80000.0, timestamp=2000),  # Средняя
    ])
    await get_test_db.commit()

    response = await async_test_client.get("/api/prices/latest", params={"ticker": "btc_usd"})

    assert response.status_code == 200
    data = response.json()
    
    assert data["price"] == 82000.0
    assert data["timestamp"] == 3000


# 3. Тесты для эндпоинта /api/prices/filter 

@pytest.mark.asyncio
async def test_get_price_by_filter_exact_match(async_test_client: AsyncClient, get_test_db: AsyncSession):
    get_test_db.add_all([
        TickerData(ticker="btc_usd", price=80000.0, timestamp=1700000000),
        TickerData(ticker="btc_usd", price=85000.0, timestamp=1700000100),
    ])
    await get_test_db.commit()

    response = await async_test_client.get(
        "/api/prices/filter", 
        params={"ticker": "btc_usd", "timestamp": "1700000100"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 85000.0
    assert data["timestamp"] == 1700000100


# 4. Проверка негативных сценариев и валидации

@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint", ["/api/prices", "/api/prices/latest"])
async def test_missing_required_ticker_param(async_test_client: AsyncClient, endpoint: str):
    response = await async_test_client.get(endpoint)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_ticker_value(async_test_client: AsyncClient):
    response = await async_test_client.get("/api/prices", params={"ticker": "doge_usd"})
    
    assert response.status_code == 422
