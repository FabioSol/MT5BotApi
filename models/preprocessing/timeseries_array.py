from typing import Tuple, Any
import pandas as pd
import numpy as np


def x_to_ts(X: pd.DataFrame, window: int = 20, flat=False):
    X = X.values
    if flat:
        return np.array([X[i:i + window].flatten() for i in range(len(X) - window)])
    else:
        return np.array([X[i:i + window] for i in range(len(X) - window)])
def xy_to_ts(X: pd.DataFrame, y: pd.DataFrame, window: int = 20, flat=False) -> Tuple[np.ndarray, Any]:
    x_cols = X.columns
    y_cols = y.columns
    df_c = pd.concat([X, y], axis=1).dropna()
    X = x_to_ts(df_c[x_cols],window, flat)
    y = df_c[y_cols].values[window:]
    if len(y_cols) == 1:
        y = y.reshape(len(y))
    return X, y


if __name__ == '__main__':
    from data.reader import Reader

    df = Reader.get_pd("EURUSD","D1")
    print(len(df) - 20 - 1)
    X, y = xy_to_ts(df, df[['Close']].shift(-1))
    print(X.shape, y.shape)

    print(df['Close'].iloc[20], y[0], X[1][-1][3])
