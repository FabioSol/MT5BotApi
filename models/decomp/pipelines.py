from datetime import datetime

import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from statsmodels.tsa.arima.model import ARIMA


class Decomposer(BaseEstimator, TransformerMixin):
    def __init__(self, window_x=10,window_y=20):
        self.window_x=window_x
        self.window_y=window_y

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return self._decompose(X)

    def _decompose(self, X):
        drift, stationary, noise = self._separate_components(X)
        return np.array([self._to_ts(drift),self._to_ts(stationary),self._to_ts(noise)]).reshape((len(X)-self.window_x,3,self.window_x,4))

    def _separate_components(self, X):
        X = X.copy()[['Open', 'High', 'Low', 'Close']]
        X_noise = pd.DataFrame()
        X_stationary = pd.DataFrame()
        X_drift = pd.DataFrame()
        for col_name, series in X.items():
            drift_model = LinearRegression()
            y_t = np.array(range(len(series))).reshape(-1, 1)
            x_full = series.values
            drift_model.fit(y_t, x_full)
            x_drift = drift_model.predict(y_t)
            x_noise = x_full - x_drift
            p = 1
            d = 1
            q = 1
            stationary_model = ARIMA(x_noise, order=(p, d, q))
            x_stationary = stationary_model.fit().predict()
            x_noise = x_noise - x_stationary
            X_noise[col_name] = x_noise
            X_drift[col_name] = x_drift
            X_stationary[col_name] = x_stationary
        return X_drift, X_stationary, X_noise

    def _to_ts(self, X):
        X=X.values
        return np.array([X[i:i + self.window_x] for i in range(len(X) - self.window_x)])

    def _get_slopes(self, y):
        ...


class Decomposer(BaseEstimator, TransformerMixin):
    def __init__(self):
        ...




if __name__ == '__main__':
    from data.reader import Reader

    df = Reader.get_pd("EURUSD", "M1",datetime(2024,4,8))
    X = Decomposer().fit_transform(df)
    print(X)
