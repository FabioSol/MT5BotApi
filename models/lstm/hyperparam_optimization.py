import json
from datetime import datetime, timedelta
import numpy as np
import optuna
from models.preprocessing.timeseries_array import xy_to_ts
from data.reader import Reader
from models.lstm.LSTM import LSTMRegressor
from models.preprocessing.splits import train_test_validation_split
from models.lstm.pipelines import x_pipeline, y_pipeline


def optimize_lstm(n_trials=15, epochs=20, symbol: str = "EURUSD", timeframe: str = "M5",
                  start: datetime = datetime.today() - timedelta(days=15)):
    df = Reader.get_pd(symbol, timeframe, start)
    pre_y = y_pipeline(df)

    def evaluate(trial):
        pre_x = x_pipeline(df,
                           window_1=trial.suggest_int(f'window_1', 5, 20),
                           window_2=trial.suggest_int(f'window_2', 20, 50),
                           window_3=trial.suggest_int(f'window_3', 50, 200),
                           window_b=trial.suggest_int(f'window_b', 5, 200),
                           window_dev=trial.suggest_float("window_dev", 0.5, 3))

        X, y = xy_to_ts(pre_x, pre_y, trial.suggest_int(f'ts_lags', 5, 100))
        X_train, X_test, X_val, y_train, y_test, y_val = train_test_validation_split(X, y)
        layers = trial.suggest_int('layers', 2, 10)
        units_exps = []
        activations = []
        for i in range(layers):
            units_exps += [trial.suggest_int(f'units_{i + 1}', 4, 9)]
            activations += [trial.suggest_categorical(f'activation_{i + 1}', ['relu', 'tanh', 'linear'])]
        units = tuple([2 ** i for i in units_exps])

        model = LSTMRegressor(
            input_shape=X.shape[1:],
            units=units,
            activations=activations
        )
        model.fit(X_train, y_train, epochs=epochs)
        y_pred = model.predict(X_test)

        return np.sqrt(np.mean(np.square(y_test - y_pred)))

    study = optuna.create_study(direction='minimize')
    study.optimize(evaluate, n_trials=n_trials)
    best_params = study.best_trial.params

    info = {"execution_date": datetime.now().isoformat(),
            "symbol": symbol,
            "timeframe": timeframe,
            "data_start": df.iloc[0].name.to_pydatetime().isoformat(),
            "data_end": df.iloc[-1].name.to_pydatetime().isoformat(),
            "result": study.best_value}

    pipeline_params = {'x': {"window_1": best_params.get("window_1"),
                             "window_2": best_params.get("window_2"),
                             "window_3": best_params.get("window_3"),
                             "window_b": best_params.get("window_b"),
                             "window_dev": best_params.get("window_dev")},
                       "ts": {'window': best_params.get("ts_lags")}}

    pre_x = x_pipeline(df, **pipeline_params.get('x'))

    X, y = xy_to_ts(pre_x, pre_y, **pipeline_params.get("ts"))
    X_train, X_test, X_val, y_train, y_test, y_val = train_test_validation_split(X, y)

    activations = [best_params[i] for i in best_params if i.startswith("activation")]
    units_exps = [best_params[i] for i in best_params if i.startswith("units")]

    hyperparams = {'input_shape': X.shape[1:], 'units': [2 ** i for i in units_exps], 'activations': activations}

    with open("hyperparams.json", "w") as json_file:
        json.dump({"metadata": info, "pipeline_params": pipeline_params, "hyperparams": hyperparams}, json_file,
                  indent=4)

    print("Best trial:")
    print(study.best_trial.params)
    print("Best RMSE:")
    print(study.best_value)
    return study


if __name__ == '__main__':
    optimize_lstm(n_trials=5, epochs=3)
