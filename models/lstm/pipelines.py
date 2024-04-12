from ta.trend import EMAIndicator
from ta.volatility import BollingerBands


def x_pipeline(df, window_1:int=14,window_2:int=40,window_3:int=100, window_b:int=40,window_dev:int=1):
    df = df.copy()
    ema1 = EMAIndicator(close=df['Close'],window=window_1)
    df[f'ema_{window_1}'] = ema1.ema_indicator()
    ema2 = EMAIndicator(close=df['Close'], window=window_2)
    df[f'ema_{window_2}'] = ema2.ema_indicator()
    ema3 = EMAIndicator(close=df['Close'], window=window_3)
    df[f'ema_{window_3}'] = ema3.ema_indicator()
    bb = BollingerBands(close=df['Close'], window=window_b,window_dev=window_dev)
    df[f"bb_high"]=bb.bollinger_hband()
    df[f"bb_low"] = bb.bollinger_lband()
    return df[['Close',f'ema_{window_1}',f'ema_{window_2}',f'ema_{window_3}','bb_high','bb_low']]

def y_pipeline(df):
    return df[['Close']].shift(-1)
