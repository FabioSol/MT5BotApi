from datetime import datetime
from data.feeder import Feeder
import time
from models.Technical.bot import OnBar
f = Feeder()
import MetaTrader5 as mt5

# Initialize MetaTrader 5
mt5.initialize()


def main():
    executed = False
    while True:
        f.run()
        if (datetime.now().minute % 5)==0:
            if not executed:
                try:
                    OnBar(mt5=mt5)
                    ex = True
                except IndexError:
                    pass
        else:
            executed = False

        time.sleep(1)


if __name__ == '__main__':
    main()
