import os
from datetime import datetime, timedelta

import keras

from models.lstm.LSTM import LSTMRegressor
from models.lstm.pipelines import x_pipeline,y_pipeline
from models.preprocessing.splits import train_test_split
from models.preprocessing.timeseries_array import xy_to_ts
from data.reader import Reader
from models.lstm import get_hyperparams, module_path

model_metadata,pipeline_params,hyperparams =get_hyperparams()

def train_and_save(epochs:int=30):
    df = Reader.get_pd(model_metadata["symbol"],
                       model_metadata["timeframe"],
                       datetime.today()-timedelta(days=15))
    pre_x = x_pipeline(df,**pipeline_params['x'])
    pre_y = y_pipeline(df)
    X, y = xy_to_ts(pre_x, pre_y,**pipeline_params['ts'])
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    model = LSTMRegressor(**hyperparams,learning_rate=1e-6)
    model.fit(X_train,y_train,epochs)
    y_pred = model.predict(X_test)
    import matplotlib.pyplot as plt
    plt.plot(y_train, label="y_true")
    plt.plot(model.predict(X_train), label='y_pred')
    plt.title("LSTM regression train")
    plt.grid()
    plt.legend()
    plt.show()

    plt.plot(y_test, label="y_true")
    plt.plot(y_pred, label='y_pred')
    plt.title("LSTM regression")
    plt.grid()
    plt.legend()
    plt.show()
    model_path = os.path.join(module_path, f"model.keras")
    model.model.save(model_path)
    print("Model saved successfully.")



if __name__=='__main__':
    train_and_save(100)


