import asyncio
import time
from .celery_app import celery_app
from ..clients.client import Client 
from ..core.database import DatabaseManager
from ..models.ticker import TickerData
from ..core.config import Config

config = Config()
db_manager = DatabaseManager(config.SQLALCHEMY_DATABASE_URL if config.SQLALCHEMY_DATABASE_URL else 'sqlite+aiosqlite:///:memory:')


async def async_fetch_and_save():
    client = Client(config.BASE_URL)
    tickers = ["btc_usd", "eth_usd"]
    
    async with db_manager.get_db() as session:
        for ticker in tickers:
            try:
                result = await client.fetch("/get_index_price", params={"index_name": ticker})
                print(result)
                price = result.get("result").get("index_price")
                print(price)
                
                if price:
                    
                    new_record = TickerData(
                        ticker=ticker,
                        price=price,
                        timestamp=int(time.time())
                    )
                    session.add(new_record)
                    await session.commit()
                    print("success")
            except Exception as e:
                print(f"Ошибка при получении {ticker}: {e}")
        
        
        await session.commit()


@celery_app.task
def fetch_and_save_prices():
    
    asyncio.run(async_fetch_and_save())