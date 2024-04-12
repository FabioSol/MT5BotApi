from sqlalchemy import Column, Integer, String, DateTime, create_engine,Float,Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from data.settings import SQLALCHEMY_DATABASE_URL
Base = declarative_base()


class FXTickData(Base):
    __tablename__ = "fx_tick_data"
    id = Column(Integer,primary_key=True,autoincrement=True)
    currency_pair = Column(String)
    timestamp = Column(DateTime, default=func.now())
    bid = Column(Float)
    ask = Column(Float)

    __table_args__ = (
        Index('idx_fx_tick_data_currency_pair_timestamp', 'currency_pair', 'timestamp'),
    )

class FXM1CandleData(Base):
    __tablename__ = "fx_m1_candle_data"

    currency_pair = Column(String,primary_key=True,)
    timestamp = Column(DateTime,primary_key=True, default=func.now())
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)

    __table_args__ = (
        Index('idx_fx_M1_candle_data_currency_pair_timestamp', 'currency_pair', 'timestamp'),
    )

class FXM5CandleData(Base):
    __tablename__ = "fx_m5_candle_data"

    currency_pair = Column(String,primary_key=True,)
    timestamp = Column(DateTime,primary_key=True, default=func.now())
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)

    __table_args__ = (
        Index('idx_fx_M5_candle_data_currency_pair_timestamp', 'currency_pair', 'timestamp'),
    )
class FXM30CandleData(Base):
    __tablename__ = "fx_m30_candle_data"

    currency_pair = Column(String,primary_key=True,)
    timestamp = Column(DateTime,primary_key=True, default=func.now())
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)

    __table_args__ = (
        Index('idx_fx_M3_candle_data_currency_pair_timestamp', 'currency_pair', 'timestamp'),
    )
class FXH1CandleData(Base):
    __tablename__ = "fx_h1_candle_data"

    currency_pair = Column(String,primary_key=True,)
    timestamp = Column(DateTime,primary_key=True, default=func.now())
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)

    __table_args__ = (
        Index('idx_fx_H1_candle_data_currency_pair_timestamp', 'currency_pair', 'timestamp'),
    )
class FXH4CandleData(Base):
    __tablename__ = "fx_h4_candle_data"

    currency_pair = Column(String,primary_key=True,)
    timestamp = Column(DateTime,primary_key=True, default=func.now())
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)

    __table_args__ = (
        Index('idx_fx_H4_candle_data_currency_pair_timestamp', 'currency_pair', 'timestamp'),
    )
class FXD1CandleData(Base):
    __tablename__ = "fx_d1_candle_data"

    currency_pair = Column(String,primary_key=True,)
    timestamp = Column(DateTime,primary_key=True, default=func.now())
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)

    __table_args__ = (
        Index('idx_fx_D1_candle_data_currency_pair_timestamp', 'currency_pair', 'timestamp'),
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL)
