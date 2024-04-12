from keras import Input
from keras.src.optimizers import Adam
from sklearn.base import BaseEstimator, RegressorMixin
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import tensorflow as tf


class LSTMRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, input_shape,
                 units=(64, 32), activations=('relu','relu'), activation_output='linear',
                 loss='mean_squared_error', metrics=('mean_absolute_error','mse'),learning_rate=1e-6):
        tf.random.set_seed(42069)
        self.model = Sequential()
        self.model.add(Input(input_shape))
        self.model.add(LSTM(units[0], activation=activations[0], return_sequences=True))
        for unit,activation in zip(units[1:-1],activations[1:-1]):
            self.model.add(LSTM(unit, activation=activation, return_sequences=True))
        self.model.add(LSTM(units[-1], activation=activations[-1]))  # Last LSTM layer
        self.model.add(Dense(1, activation=activation_output))  # Output a single value
        self.model.compile(optimizer=Adam(learning_rate=learning_rate), loss=loss, metrics=list(metrics))

    def fit(self, X, y, epochs=10, batch_size=32):
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size)

    def predict(self, X):
        return self.model.predict(X).flatten()


if __name__=='__main__':
    from models.preprocessing.timeseries_array import xy_to_ts
    from data.reader import Reader

    df = Reader.get_pd("EURUSD", "M1")
    X, y = xy_to_ts(df[['Close']], df[['Close']].shift(-1))
    model = LSTMRegressor(
        input_shape=X.shape[1:],
        units=(64, 64, 32,64,64),
        activations=['relu']*5,
        activation_output='linear',
        loss='mean_squared_error',
        metrics=['mean_absolute_error']
    )
    model.fit(X,y)
    y_pred = model.predict(X)
    print(y.shape)
    print(y_pred.shape)
    import matplotlib.pyplot as plt
    plt.plot(y, label="y_true")
    plt.plot(y_pred, label='y_pred')
    plt.title("LSTM regression")
    plt.grid()
    plt.show()



