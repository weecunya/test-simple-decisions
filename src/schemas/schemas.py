from pydantic import BaseModel
from typing import Literal


class Base(BaseModel):
    pass

class TickerResponse(Base):   
    ticker: str 
    price: float
    timestamp: int

    class Config:
        from_attributes = True


class TickerRequest(Base):
    ticker: Literal["btc_usd", "eth_usd"]
    timestamp: int | None