import pytest
from unittest.mock import patch, AsyncMock
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.worker import async_fetch_and_save
from src.models.ticker import TickerData

@pytest.mark.asyncio
@patch("src.tasks.worker.db_manager.get_db")
@patch("src.clients.client.Client.fetch")
async def test_worker_fetches_and_saves_data(mock_fetch, mock_get_db, get_test_db: AsyncSession):

    mock_get_db.return_value.__aenter__.return_value = get_test_db

    mock_fetch.return_value = {
        "result": {
            "index_price": 50000.50
        }
    }


    await async_fetch_and_save()

    assert mock_fetch.call_count == 2

    result = await get_test_db.execute(select(TickerData))
    saved_records = result.scalars().all()

    assert len(saved_records) == 2
    tickers_saved = {record.ticker for record in saved_records}
    assert tickers_saved == {"btc_usd", "eth_usd"}
    assert saved_records[0].price == 50000.50

@pytest.mark.asyncio
@patch("src.tasks.worker.db_manager.get_db") 
@patch("src.clients.client.Client.fetch")
async def test_worker_handles_api_error(mock_fetch, mock_get_db, get_test_db: AsyncSession):
    mock_get_db.return_value.__aenter__.return_value = get_test_db 
    mock_fetch.side_effect = Exception("API is down")
    
    await async_fetch_and_save()
    
    
    result = await get_test_db.execute(select(TickerData))
    assert result.scalars().all() == []


@pytest.mark.asyncio
@patch("src.tasks.worker.db_manager.get_db")
@patch("src.clients.client.Client.fetch")
async def test_worker_partial_failure(mock_fetch, mock_get_db, get_test_db: AsyncSession):
    mock_get_db.return_value.__aenter__.return_value = get_test_db

    mock_fetch.side_effect = [
        Exception("Deribit timeout"),                
        {"result": {"index_price": 3000.50}}         
    ]

    await async_fetch_and_save()

    assert mock_fetch.call_count == 2

    result = await get_test_db.execute(select(TickerData))
    saved_records = result.scalars().all()

    assert len(saved_records) == 1
    assert saved_records[0].ticker == "eth_usd"
    assert saved_records[0].price == 3000.50


@pytest.mark.asyncio
@patch("src.tasks.worker.db_manager.get_db")
@patch("src.clients.client.Client.fetch")
async def test_worker_invalid_api_response(mock_fetch, mock_get_db, get_test_db: AsyncSession):
    mock_get_db.return_value.__aenter__.return_value = get_test_db

    mock_fetch.return_value = {
        "jsonrpc": "2.0",
        "error": {"message": "Invalid params", "code": -32602}
    }


    try:
        await async_fetch_and_save()
    except AttributeError:
        pytest.fail("Воркер не перехватил AttributeError при парсинге некорректного ответа")

    result = await get_test_db.execute(select(TickerData))
    saved_records = result.scalars().all()
    assert len(saved_records) == 0