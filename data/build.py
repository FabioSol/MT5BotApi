

def main():
    from schema import Base, engine
    from feeder import Feeder
    from settings import MAIN_PAIRS
    Base.metadata.create_all(bind=engine)

    for pair in MAIN_PAIRS:
        f = Feeder()
        f.fast_feed_ticks_range(pair)
        f.fast_feed_candle_range(pair)


if __name__=='__main__':
    main()

