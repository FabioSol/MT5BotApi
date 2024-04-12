from datetime import timedelta, datetime
from itertools import product

import pandas as pd

from models.preprocessing.X.technical_transformers import *


def x_pipeline(df: pd.DataFrame, trial=None, mask_number=None, **kwargs):
    indicator_transformers = [AwesomeOscillatorTransformer,
                              KAMATransformer,
                              PercentagePriceOscillatorTransformer,
                              ROCTransformer,
                              RSITransformer,
                              StochRSITransformer,
                              StochasticOscillatorTransformer,
                              TSITransformer,
                              UltimateOscillatorTransformer,
                              WilliamsRTransformer]

    masks = list(product([0, 1], repeat=len(indicator_transformers)))

    if mask_number is None:
        if trial is None:
            mask_number = len(masks)-1
        else:
            good_masks = [442,450,974,961,979,1023]
            mask_number = trial.suggest_categorical("mask_number",list(range(len(masks))))


    df = df.copy()
    for ind, msk in zip(indicator_transformers, masks[mask_number]):
        if msk == 1:
            df = ind.transform_or_suggest(df, trial, **kwargs)

    return df


def y_pipeline_(df:pd.DataFrame):
    return pd.DataFrame(df['Close'].pct_change().shift(-1).apply(lambda x: 0 if x<0.00001 else 1)).rename(columns={"Close":"y"})

def y_pipeline(df:pd.DataFrame, max_periods=60,sl=0.0001,tp=0.00012):
    def sim(df_s):
        current=df_s.iloc[0]
        current_price = current['Close']
        stop_loss = current_price*(1-sl)
        take_profit = current_price*(1+tp)
        cat = 0
        broken=False
        for idx,row in df_s.iloc[1:].iterrows():
            check_points = [row['Open'], row['High'], row['Low'], row['Close']]
            for value in check_points:
                if value>=take_profit:
                    cat = 1
                    broken=True
                    break
                elif value<=stop_loss:
                    broken = True
                    break
            if broken:
                break

        return current.name, cat

    y=pd.DataFrame(index=df.index, columns=["y"])
    for start in range(len(df)-max_periods):
        df_slice = df.iloc[start:start+max_periods]
        name,cat=sim(df_slice)
        y.loc[name,"y"]=cat
    return y.dropna().astype(int)


if __name__ == '__main__':
    from data.reader import Reader

    df = Reader.get_pd("EURUSD", "M5",datetime.now()-timedelta(days=15))
    y=y_pipeline(df)
    print((y.sum())/len(y))
    print(y)
    print(y.isna().sum())
