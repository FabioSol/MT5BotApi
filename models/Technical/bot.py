from datetime import timedelta, datetime
import joblib
from data.reader import Reader
from models.Technical import get_hyperparams
from models.Technical.pipelines import x_pipeline
from models.Technical import module_path
hyperparams = get_hyperparams()
model=joblib.load(module_path+"/model.pkl")

def get_signal():
    needed = 99
    df = Reader.get_pd("EURUSD", "M5",datetime.now()-timedelta(minutes=5*(needed+1)))
    X = x_pipeline(df, **hyperparams).dropna().values
    return model.predict([X[-1]])[0]

def OnBar(mt5):
    symbol = "EURUSD"
    decs = 5
    sl=0.0001
    tp=0.00012
    signal = get_signal()

    if signal == 1:
        price = mt5.symbol_info_tick(symbol).ask
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "type": mt5.ORDER_TYPE_BUY,
            "volume": 1,
            "price": price,
            "sl": round(price * (1 - sl), decs),
            "tp": round(price * (1 + tp), decs),
            "magic": 2208,
            "deviation": 20,# Specify a magic number for the order
            "comment": "Opening position",
            "type_time": mt5.ORDER_TIME_GTC,  # Good Till Cancel (GTC) order
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        print(request)
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to open position: {result.comment}")
        else:
            print(f"Position opened successfully: {result.order}")

