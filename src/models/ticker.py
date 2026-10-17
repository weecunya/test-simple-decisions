#from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import Index
from sqlalchemy.orm import mapped_column, Mapped
from ..core.database import Base



class TickerData(Base):
    __tablename__ = "deribit_data"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    timestamp: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (
        Index('ix_ticker_timestamp', 'ticker', 'timestamp'),
    )




        # id = Column(Integer, primary_key=True, index=True)
    # ticker = Column(String(20), nullable=False)
    # price = Column(Float, nullable=False)
    # timestamp = Column(Integer, nullable=False)

    # # Составной индекс для быстрого поиска по тикеру и фильтрации по дате
    # __table_args__ = (
    #     Index('ix_ticker_timestamp', 'ticker', 'timestamp'),
    # )