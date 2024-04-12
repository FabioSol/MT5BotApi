from datetime import datetime, timedelta
from typing import Union

import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import asc
from data.schema import *


class Reader:
    schemas = {
        "T": FXTickData,
        "M1": FXM1CandleData,
        "M5": FXM5CandleData,
        "M30": FXM30CandleData,
        "H1": FXH1CandleData,
        "H4": FXH4CandleData,
        "D1": FXD1CandleData}

    @staticmethod
    def get(symbol: str, timeframe: str, start: Union[datetime, None] = None, end: datetime = datetime.now()):
        local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with local_session() as session:
            schema = Reader.schemas.get(timeframe)
            query = session.query(schema).filter_by(currency_pair=symbol)

            if start:
                query = query.filter(schema.timestamp >= start)
            if end:
                query = query.filter(schema.timestamp <= end)

            query = query.order_by(asc('timestamp'))
            result = query.all()
            return result

    @staticmethod
    def get_pd(symbol: str, timeframe: str, start: Union[datetime, None] = None, end: datetime = datetime.now()):
        local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with local_session() as session:
            schema = Reader.schemas.get(timeframe)
            query = session.query(schema).filter_by(currency_pair=symbol)

            if start:
                query = query.filter(schema.timestamp >= start)
            if end:
                query = query.filter(schema.timestamp <= end)

            query = query.order_by(asc('timestamp'))
            c_to_drop = ['currency_pair']
            index = ['timestamp']
            new_c = {"open_price": "Open", "high_price": "High", "low_price": "Low", "close_price": "Close",
                     "volume": "Volume"}
            if timeframe == "T":
                c_to_drop += ["id"]
                new_c = {"ask": "Ask", "bid": "Bid"}

            df = pd.read_sql_query(query.statement, session.bind).drop(c_to_drop, axis=1).set_index(index).rename(
                columns=new_c)
        return df

if __name__ == "__main__":
    print(Reader.get_pd("EURUSD", "M1"))



