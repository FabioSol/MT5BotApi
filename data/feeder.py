from sqlalchemy import desc
from tqdm import tqdm
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import MetaTrader5 as mt5
from sqlalchemy.orm import sessionmaker
from data.schema import *
from data.settings import MAIN_PAIRS
import concurrent.futures


class Feeder:
    schemas = {
        "M1": [(FXM1CandleData, mt5.TIMEFRAME_M1, "M1")],
        "M5": [(FXM5CandleData, mt5.TIMEFRAME_M5, "M5")],
        "M30": [(FXM30CandleData, mt5.TIMEFRAME_M3, "M30")],
        "H1": [(FXH1CandleData, mt5.TIMEFRAME_H1, "H1")],
        "H4": [(FXH4CandleData, mt5.TIMEFRAME_H4, "H4")],
        "D1": [(FXD1CandleData, mt5.TIMEFRAME_D1, "D1")],
        "all": [(FXM1CandleData, mt5.TIMEFRAME_M1, "M1"),
                (FXM5CandleData, mt5.TIMEFRAME_M5, "M5"),
                (FXM30CandleData, mt5.TIMEFRAME_M3, "M30"),
                (FXH1CandleData, mt5.TIMEFRAME_H1, "H1"),
                (FXH4CandleData, mt5.TIMEFRAME_H4, "H4"),
                (FXD1CandleData, mt5.TIMEFRAME_D1, "D1")]}

    def __init__(self):
        if not mt5.initialize():
            print("Failed to connect to MetaTrader 5!")
            quit()
        self.mt5 = mt5
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def fast_feed_ticks_range(self, symbol, date_from: datetime = datetime.now() - timedelta(days=5),
                              date_to: datetime = datetime.now()):
        ticks = mt5.copy_ticks_range(symbol, date_from, date_to, mt5.COPY_TICKS_ALL)
        if ticks is not None:
            tick_count = len(ticks)
            with self.SessionLocal() as session:
                with tqdm(total=tick_count, desc="Feeding ticks") as pbar:
                    for tick in ticks:
                        if tick:
                            tick_data = FXTickData(currency_pair=symbol, bid=tick[1], ask=tick[2],
                                                   timestamp=datetime.fromtimestamp(tick[0]))
                            session.add(tick_data)
                            pbar.update(1)
                    session.commit()
        elif date_from < date_to:
            self.fast_feed_ticks_range(symbol, date_from + timedelta(days=1), date_to)

    def fast_feed_candle_range(self, symbol, time_frame: str = "all", date_from: datetime = datetime(2022, 1, 1),
                               date_to: datetime = datetime.now()):
        for schema, timeframe_obj, tf in self.schemas.get(time_frame):
            candles = mt5.copy_rates_range(symbol, timeframe_obj, date_from, date_to)
            if candles is not None:
                candle_count = len(candles)
                with self.SessionLocal() as session:
                    with tqdm(total=candle_count, desc=f"Feeding {tf} candles") as pbar:
                        for candle in candles:
                            if candle:
                                candle_data = schema(currency_pair=symbol, open_price=candle[1], high_price=candle[2],
                                                     low_price=candle[3], close_price=candle[4], volume=int(candle[5]),
                                                     timestamp=datetime.fromtimestamp(candle[0]))
                                session.add(candle_data)
                                pbar.update(1)
                        session.commit()
            elif date_from < date_to:
                self.fast_feed_candle_range(symbol, tf, date_from + timedelta(days=1), date_to)

    def feed_ticks_range(self, symbol, date_from: datetime = datetime.now() - timedelta(days=1),
                         date_to: datetime = datetime.now(), motive: str = "Feeding ticks", disable_tqdm: bool = False):
        ticks = mt5.copy_ticks_range(symbol, date_from, date_to, mt5.COPY_TICKS_ALL)
        if ticks is not None:
            tick_count = len(ticks)
            with self.SessionLocal() as session:
                with tqdm(total=tick_count, desc=motive, disable=disable_tqdm) as pbar:
                    for tick in ticks:
                        if tick:
                            tick_data = FXTickData(currency_pair=symbol, bid=tick[1], ask=tick[2],
                                                   timestamp=datetime.fromtimestamp(tick[0]))
                            try:
                                session.add(tick_data)
                                session.commit()
                                pbar.update(1)
                            except IntegrityError:
                                session.rollback()
                                pbar.update(1)
                                continue

        elif date_from < date_to:
            self.feed_ticks_range(symbol, date_from + timedelta(days=1), date_to)

    def feed_candle_range(self, symbol, time_frame, date_from: datetime = datetime(2022, 1, 1),
                          date_to: datetime = datetime.now(), motive: str = "Feeding candles",
                          disable_tqdm: bool = False):
        for schema, timeframe_obj, tf in self.schemas.get(time_frame):
            candles = mt5.copy_rates_range(symbol, timeframe_obj, date_from, date_to)
            if candles is not None:
                candle_count = len(candles)
                with self.SessionLocal() as session:
                    with tqdm(total=candle_count, desc=f"{tf}: {motive}", disable=disable_tqdm) as pbar:
                        for candle in candles:
                            if candle:
                                candle_data = schema(currency_pair=symbol, open_price=candle[1], high_price=candle[2],
                                                     low_price=candle[3], close_price=candle[4], volume=int(candle[5]),
                                                     timestamp=datetime.fromtimestamp(candle[0]))
                                try:
                                    session.add(candle_data)
                                    session.commit()
                                    pbar.update(1)
                                except IntegrityError:
                                    session.rollback()
                                    pbar.update(1)
                                    continue
            elif date_from < date_to:
                self.feed_candle_range(symbol, tf, date_from + timedelta(days=1), date_to)

    def update_ticks(self, symbol, disable_tqdm: bool = False):
        with self.SessionLocal() as session:
            latest_date = session.query(FXTickData).filter_by(currency_pair=symbol).order_by(
                desc('timestamp')).first().timestamp
        self.feed_ticks_range(symbol, latest_date, motive=f"Updating ticks from {latest_date}",
                              disable_tqdm=disable_tqdm)

    def update_candles(self, symbol, time_frame: str = "all", disable_tqdm: bool = False):
        for schema, timeframe_obj, tf in self.schemas.get(time_frame):
            with self.SessionLocal() as session:
                latest_date = session.query(schema).filter_by(currency_pair=symbol).order_by(
                    desc('timestamp')).first().timestamp
            self.feed_candle_range(symbol, tf, latest_date, motive=f"Updating candles from {latest_date}",
                                   disable_tqdm=disable_tqdm)

    def update_all(self, symbol, disable_tqdm=True):
        self.update_ticks(symbol, disable_tqdm=disable_tqdm)
        self.update_candles(symbol, disable_tqdm=disable_tqdm)

    def run(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.update_all, MAIN_PAIRS)


def main():
    f = Feeder()
    f.run()


if __name__ == "__main__":
    main()
