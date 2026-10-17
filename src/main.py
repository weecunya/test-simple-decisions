from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api.endpoints import router as api_router
from .core.database import DatabaseManager, Base
from .core.config import Config


config = Config()
db_manager = DatabaseManager(config.SQLALCHEMY_DATABASE_URL if config.SQLALCHEMY_DATABASE_URL else 'sqlite+aiosqlite:///:memory:')

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
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


from fastapi import Request
from pydantic import ValidationError


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Response serialization error",
            "errors": exc.errors()  
        },
    )