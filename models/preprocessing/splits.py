import numpy as np

def train_test_split(X:np.ndarray,y:np.ndarray,test:float=0.2):
    if len(X)!=len(y):
        raise ValueError("X and y size mismatch")
    if test>=1:
        raise ValueError("test should be float smaller than 1")
    pivot=int(len(X)*(1-test))
    return X[:pivot], X[pivot:], y[:pivot], y[pivot:]

def train_test_validation_split(X:np.ndarray,y:np.ndarray,test:float=0.1,validation=0.2):
    X_train, X_test, y_train,y_test=train_test_split(X,y,test+validation)
    X_test,X_val,y_test,y_val = train_test_split(X_test,y_test,validation/(test+validation))
    return X_train,X_test,X_val,y_train,y_test,y_val