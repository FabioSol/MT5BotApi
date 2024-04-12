import pandas as pd


def bullish_categorical_pipeline(df: pd.DataFrame, max_len: int, sl: float, tp: float):
    df = df.copy()
    y = []
    for n, (idx, row) in enumerate(df.iterrows()):
        current_price = row['Close']
        current_sl = current_price * (1 - sl)
        current_tp = current_price * (1 + tp)
        cat = 0

        for sub_idx, sub_row in df.iloc[n + 1:n + max_len + 1].iterrows():
            #print(idx, sub_idx)
            prices = [sub_row['Low'], sub_row['High'], sub_row['Close']]
            for price in prices:
                if price > current_tp:
                    cat = 1
                    break
                elif price <= current_sl:
                    cat = -1
                    break
            if cat == 1:
                break
            if cat == -1:
                cat = 0
                break
        y.append(cat)
    df["y"] = y
    return df
