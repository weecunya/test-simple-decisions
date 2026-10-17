from pydantic import BaseModel
import datetime


class TickersAvailable(BaseModel):
    btc_usd: str = "btc_usd"
    eth_usd: str = "eth_usd"


class Base(BaseModel):
    pass

class TickerResponse(Base):   
    ticker: str 
    price: float
    timestamp: int

    class Config:
        from_attributes = True

class TickerResponseList(Base):
    prices: list[TickerResponse]



class TickerRequest(Base):
    ticker: str = TickersAvailable
    timestamp: int | None