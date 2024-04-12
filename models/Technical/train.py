from datetime import datetime, timedelta

import joblib
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import fbeta_score, confusion_matrix
import seaborn as sns
from data.reader import Reader
from models.Technical.SVM import SVM
from models.Technical.pipelines import y_pipeline, x_pipeline
from models.Technical import get_hyperparams

hyperparams = get_hyperparams()
print(hyperparams)
def train(symbol: str = "EURUSD", timeframe: str = "M5",
                  start: datetime = datetime.today() - timedelta(days=15),beta=0.9):
    df = Reader.get_pd(symbol, timeframe,start).dropna()
    Y = y_pipeline(df)
    X = x_pipeline(df, **hyperparams)
    df_c = pd.concat([X, Y], axis=1).dropna()
    X = df_c[X.columns].values
    y = df_c[Y.columns].values.reshape(len(df_c))
    pivot1 = int(len(df_c) * 0.7)
    pivot2 = int(len(df_c) * 0.85)

    X_train, X_test,X_val = X[:pivot1], X[pivot1:pivot2], X[pivot2:]
    y_train, y_test,y_val = y[:pivot1], y[pivot1:pivot2], y[pivot2:]

    model = SVM(**hyperparams)
    print(model)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    metric = fbeta_score(y_test, y_pred, beta=beta)
    print("fbeta: ",metric)

    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='g', cbar=False)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()

    y_pred_v = model.predict(X_val)
    metric = fbeta_score(y_val, y_pred_v, beta=beta)
    print("fbeta: ", metric)

    cm = confusion_matrix(y_val, y_pred_v)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='g', cbar=False)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix v')
    plt.show()

    model_filename = f"model.pkl"
    joblib.dump(model, model_filename)


if __name__=="__main__":
    train()





