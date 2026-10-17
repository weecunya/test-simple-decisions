from typing import AsyncGenerator

from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import pytest
from httpx import AsyncClient, ASGITransport

from src.core.config import Config
from src.main import app
from src.core.database import Base
from src.api.endpoints import db_manager


config = Config()

test_engine = create_async_engine(
    config.TEST_DATABASE_URL if config.TEST_DATABASE_URL else 'sqlite+aiosqlite:///:memory:', 
    echo=False, 
    poolclass=StaticPool)

TestSessionLocal = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture
async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
async def override_db_dependency(get_test_db: AsyncSession):
    async def _override_get_db():
        yield get_test_db
    
    app.dependency_overrides[db_manager.get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest.fixture(autouse=True)
async def async_test_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
