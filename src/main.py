from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models.ticker import TickerData
from .api.endpoints import router as api_router
from .core.database import DatabaseManager, Base
from .core.config import Config

config = Config()
db_manager = DatabaseManager(config.SQLALCHEMY_DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Success")
    yield
    await db_manager.engine.dispose()


app = FastAPI(
    title="Deribit API",
    description="API for fetching cryptocurrency prices from Deribit",
    version="1.0.0",
    contact={
        "name": "developer",
        "email": "wicaszmakowizer@gmail.com"
    },
    lifespan=lifespan
)
app.include_router(api_router, prefix="/api")

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://0.0.0.0:8000"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok"}


