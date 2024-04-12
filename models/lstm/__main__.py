from models.lstm.hyperparam_optimization import optimize_lstm
from models.lstm.train import train_and_save

if __name__ =='__main__':
    optimize_lstm(100,10)
    train_and_save(100)
