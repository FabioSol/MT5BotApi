import json
from datetime import datetime, timedelta
import pandas as pd
from models.Technical.pipelines import y_pipeline,x_pipeline
from models.Technical.SVM import SVM
from data.reader import Reader
from sklearn.metrics import fbeta_score
import optuna

def optimize_hyperparams(n_trials=15, symbol: str = "EURUSD", timeframe: str = "M5",
                  start: datetime = datetime.today() - timedelta(days=15),beta=0.9):
    df = Reader.get_pd(symbol, timeframe,start)
    Y = y_pipeline(df)

    def objective(trial:optuna.trial):
        X = x_pipeline(df, trial)
        df_c = pd.concat([X, Y], axis=1).dropna()
        X = df_c[X.columns].values
        y = df_c[Y.columns].values.reshape(len(df_c))
        pivot1=int(len(df_c)*0.7)
        pivot2 = int(len(df_c) * 0.85)

        X_train,X_test = X[:pivot1], X[pivot1:pivot2]
        y_train,y_test = y[:pivot1], y[pivot1:pivot2]
        C = trial.suggest_float('C', 1e-5, 100)
        kernel = trial.suggest_categorical('kernel', ['rbf', 'sigmoid']) #poly is too slow and linear doesnt converge
        if kernel =='linear':
            gamma = 'scale'
        else:
            gamma = trial.suggest_float('gamma', 1e-5, 10)

        m = SVM(C=C,kernel=kernel,gamma=gamma)
        m.fit(X_train,y_train)
        y_p = m.predict(X_test)
        return  fbeta_score(y_test, y_p, beta=beta)

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)

    best_params = study.best_params
    best_metric = study.best_value
    print("Best metric: ",best_metric)

    with open("hyperparams.json", "w") as json_file:
        json.dump(best_params, json_file,
                  indent=4)
    study_df = study.trials_dataframe()

    # Save the DataFrame to a file
    study_df.to_csv(f'studies/optuna_study{datetime.today().date().isoformat()}.csv', index=False)

if __name__=="__main__":
    optimize_hyperparams(100)





