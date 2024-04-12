import pandas as pd
from ta.momentum import *
from abc import ABC
import optuna

from typing import List


class TechnicalTransformer(ABC):
    params = List[str]

    @staticmethod
    def transform(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        ...

    @staticmethod
    def suggest(df: pd.DataFrame, trial: optuna.trial) -> pd.DataFrame:
        ...

    @staticmethod
    def transform_or_suggest(df: pd.DataFrame, trial: optuna.trial = None, **kwargs) -> pd.DataFrame:
        ...


class AwesomeOscillatorTransformer(TechnicalTransformer):
    params = ["aws_w1", "aws_w2"]

    @staticmethod
    def transform(df, aws_w1=None, aws_w2=None, **kwargs):
        if aws_w1 is None or aws_w2 is None:
            return df
        aws = AwesomeOscillatorIndicator(high=df["High"], low=df["Low"], window1=aws_w1, window2=aws_w2)
        df[f'aws_{aws_w1}_{aws_w2}'] = aws.awesome_oscillator()
        return df

    @staticmethod
    def suggest(df, trial):
        params_dict = {}
        for param in AwesomeOscillatorTransformer.params:
            params_dict.update({param: trial.suggest_int(param, 2, 100)})
        return AwesomeOscillatorTransformer.transform(df, **params_dict)

    @staticmethod
    def transform_or_suggest(df, trial=None, **kwargs):
        if trial:
            return AwesomeOscillatorTransformer.suggest(df, trial)
        else:
            return AwesomeOscillatorTransformer.transform(df, **kwargs)


class KAMATransformer(TechnicalTransformer):
    params = ["kma_window", "kma_pow1", "kma_pow2"]

    @staticmethod
    def transform(df, kma_window=None, kma_pow1=None, kma_pow2=None, **kwargs):
        if kma_window is None or kma_pow1 is None or kma_pow2 is None:
            return df
        kma = KAMAIndicator(close=df["Close"], window=kma_window, pow1=kma_pow1, pow2=kma_pow2)
        df[f"kma_{kma_window}_{kma_pow1}_{kma_pow2}"] = kma.kama()
        return df

    @staticmethod
    def suggest(df, trial):
        params_dict = {}
        for param in KAMATransformer.params:
            params_dict.update({param: trial.suggest_int(param, 2, 50)})  # Adjust range as needed
        return KAMATransformer.transform(df, **params_dict)

    @staticmethod
    def transform_or_suggest(df, trial=None, **kwargs):
        if trial:
            return KAMATransformer.suggest(df, trial)
        else:
            return KAMATransformer.transform(df, **kwargs)


class PercentagePriceOscillatorTransformer(TechnicalTransformer):
    params = ["ppo_wslow", "ppo_wfast", "ppo_wsign"]

    @staticmethod
    def transform(df, ppo_wslow=None, ppo_wfast=None, ppo_wsign=None, **kwargs):
        if ppo_wslow is None or ppo_wfast is None or ppo_wsign is None:
            return df
        pposc = PercentagePriceOscillator(close=df["Close"], window_slow=ppo_wslow, window_fast=ppo_wfast,
                                          window_sign=ppo_wsign)
        df[f"ppo_{ppo_wslow}_{ppo_wfast}_{ppo_wsign}"] = pposc.ppo()
        return df

    @staticmethod
    def suggest(df, trial):
        params_dict = {}
        for param in PercentagePriceOscillatorTransformer.params:
            params_dict.update({param: trial.suggest_int(param, 2, 50)})  # Adjust range as needed
        return PercentagePriceOscillatorTransformer.transform(df, **params_dict)

    @staticmethod
    def transform_or_suggest(df, trial=None, **kwargs):
        if trial:
            return PercentagePriceOscillatorTransformer.suggest(df, trial)
        else:
            return PercentagePriceOscillatorTransformer.transform(df, **kwargs)


class PercentageVolumeOscillatorTransformer(TechnicalTransformer):
    params = ["pvo_wslow", "pvo_wfast", "pvo_wsign"]

    @staticmethod
    def transform(df, pvo_wslow=None, pvo_wfast=None, pvo_wsign=None, **kwargs):
        if pvo_wslow is None or pvo_wfast is None or pvo_wsign is None:
            return df
        pvos = PercentageVolumeOscillator(volume=df["Volume"], window_slow=pvo_wslow, window_fast=pvo_wfast,
                                          window_sign=pvo_wsign)
        df[f"pvo_{pvo_wslow}_{pvo_wfast}_{pvo_wsign}"] = pvos.pvo()
        return df

    @staticmethod
    def suggest(df, trial):
        params_dict = {}
        for param in PercentageVolumeOscillatorTransformer.params:
            params_dict.update({param: trial.suggest_int(param, 2, 50)})  # Adjust range as needed
        return PercentageVolumeOscillatorTransformer.transform(df, **params_dict)

    @staticmethod
    def transform_or_suggest(df, trial=None, **kwargs):
        if trial:
            return PercentageVolumeOscillatorTransformer.suggest(df, trial)
        else:
            return PercentageVolumeOscillatorTransformer.transform(df, **kwargs)


class ROCTransformer(TechnicalTransformer):
    params = ["roc_window"]

    @staticmethod
    def transform(df, roc_window=None, **kwargs):
        if roc_window is None:
            return df
        roci = ROCIndicator(close=df["Close"], window=roc_window)
        df[f"roc_{roc_window}"] = roci.roc()
        return df

    @staticmethod
    def suggest(df, trial):
        params_dict = {}
        for param in ROCTransformer.params:
            params_dict.update({param: trial.suggest_int(param, 2, 50)})  # Adjust range as needed
        return ROCTransformer.transform(df, **params_dict)

    @staticmethod
    def transform_or_suggest(df, trial=None, **kwargs):
        if trial:
            return ROCTransformer.suggest(df, trial)
        else:
            return ROCTransformer.transform(df, **kwargs)


class RSITransformer(TechnicalTransformer):
    params = ["rsi_window"]

    @staticmethod
    def transform(df, rsi_window=None, **kwargs):
        if rsi_window is None:
            return df
        rsii = RSIIndicator(close=df["Close"], window=rsi_window)
        df[f'rsi_{rsi_window}'] = rsii.rsi()
        return df

    @staticmethod
    def suggest(df, trial):
        params_dict = {}
        for param in RSITransformer.params:
            params_dict.update({param: trial.suggest_int(param, 2, 50)})  # Adjust range as needed
        return RSITransformer.transform(df, **params_dict)

    @staticmethod
    def transform_or_suggest(df, trial=None, **kwargs):
        if trial:
            return RSITransformer.suggest(df, trial)
        else:
            return RSITransformer.transform(df, **kwargs)


class StochRSITransformer(TechnicalTransformer):
    params = ["srsi_window", "srsi_smooth1", "srsi_smooth2"]

    @staticmethod
    def transform(df, srsi_window=None, srsi_smooth1=None, srsi_smooth2=None, **kwargs):
        if srsi_window is None or srsi_smooth1 is None or srsi_smooth2 is None:
            return df
        srsi = StochRSIIndicator(close=df["Close"], window=srsi_window, smooth1=srsi_smooth1,
                                 smooth2=srsi_smooth2)
        df[f'srsi_{srsi_window}_{srsi_smooth1}_{srsi_smooth2}'] = srsi.stochrsi()
        return df

    @staticmethod
    def suggest(df, trial):
        params_dict = {"srsi_window": trial.suggest_int("srsi_window", 2, 100),
                       "srsi_smooth1":trial.suggest_int("srsi_smooth1", 1, 8),
                       "srsi_smooth2":trial.suggest_int("srsi_smooth2", 1, 8)}
         # Adjust range as needed
        return StochRSITransformer.transform(df, **params_dict)

    @staticmethod
    def transform_or_suggest(df, trial=None, **kwargs):
        if trial:
            return StochRSITransformer.suggest(df, trial)
        else:
            return StochRSITransformer.transform(df, **kwargs)


class StochasticOscillatorTransformer(TechnicalTransformer):
    params = ["so_window", "so_smooth"]

    @staticmethod
    def transform(df, so_window=None, so_smooth=None, **kwargs):
        if so_window is None or so_smooth is None:
            return df
        so = StochasticOscillator(high=df["High"], low=df["Low"], close=df["Close"], window=so_window,
                                  smooth_window=so_smooth,
                                  )
        df[f'so_{so_window}_{so_smooth}'] = so.stoch()
        return df

    @staticmethod
    def suggest(df, trial):
        params_dict = {}
        for param in StochasticOscillatorTransformer.params:
            params_dict.update({param: trial.suggest_int(param, 2, 50)})  # Adjust range as needed
        return StochasticOscillatorTransformer.transform(df, **params_dict)

    @staticmethod
    def transform_or_suggest(df, trial=None, **kwargs):
        if trial:
            return StochasticOscillatorTransformer.suggest(df, trial)
        else:
            return StochasticOscillatorTransformer.transform(df, **kwargs)


class TSITransformer(TechnicalTransformer):
    params = ["tsi_window_slow", "tsi_window_fast"]

    @staticmethod
    def transform(df, tsi_window_slow=None, tsi_window_fast=None, **kwargs):
        if tsi_window_slow is None or tsi_window_fast is None:
            return df
        tsit = TSIIndicator(close=df["Close"], window_slow=tsi_window_slow,
                                  window_fast=tsi_window_fast,
                                  )
        df[f'tsi_{tsi_window_slow}_{tsi_window_fast}'] = tsit.tsi()
        return df

    @staticmethod
    def suggest(df, trial):
        params_dict = {}
        for param in TSITransformer.params:
            params_dict.update({param: trial.suggest_int(param, 2, 50)})  # Adjust range as needed
        return TSITransformer.transform(df, **params_dict)

    @staticmethod
    def transform_or_suggest(df, trial=None, **kwargs):
        if trial:
            return TSITransformer.suggest(df, trial)
        else:
            return TSITransformer.transform(df, **kwargs)



class UltimateOscillatorTransformer(TechnicalTransformer):
    params = ["ult_window_1", "ult_window_2","ult_window_3","ult_weight_1","ult_weight_2","ult_weight_3"]

    @staticmethod
    def transform(df, ult_window_1=None, ult_window_2=None,ult_window_3=None,ult_weight_1=None,ult_weight_2=None,ult_weight_3=None, **kwargs):
        if ult_window_1 is None or ult_window_2 is None or ult_window_3 is None or ult_weight_1 is None or ult_weight_2 is None or ult_weight_3 is None:
            return df
        uo = UltimateOscillator(high=df["High"], low=df["Low"], close=df["Close"], window1=ult_window_1,
                                  window2=ult_window_2,window3=ult_window_3,weight1=ult_weight_1,weight2=ult_weight_2,weight3=ult_weight_3
                                  )
        df[f'uo_{ult_window_1}/{ult_weight_1}_{ult_window_2}/{ult_weight_2}_{ult_window_3}/{ult_weight_3}'] = uo.ultimate_oscillator()
        return df

    @staticmethod
    def suggest(df, trial):
        params_dict = {"ult_window_1": trial.suggest_int("ult_window_1", 2, 20),
                       "ult_window_2": trial.suggest_int("ult_window_2", 20, 50),
                       "ult_window_3": trial.suggest_int("ult_window_3", 50, 100),
                       "ult_weight_1": trial.suggest_float("ult_weight_1", 0.5, 10),
                       "ult_weight_2": trial.suggest_float("ult_weight_2", 0.5, 10),
                       "ult_weight_3": trial.suggest_float("ult_weight_3", 0.5, 10),}# Adjust range as needed
        return UltimateOscillatorTransformer.transform(df, **params_dict)

    @staticmethod
    def transform_or_suggest(df, trial=None, **kwargs):
        if trial:
            return UltimateOscillatorTransformer.suggest(df, trial)
        else:
            return UltimateOscillatorTransformer.transform(df, **kwargs)


class WilliamsRTransformer(TechnicalTransformer):
    params = ["williams_lbp"]

    @staticmethod
    def transform(df, williams_lbp=None, **kwargs):
        if williams_lbp:
            wr = WilliamsRIndicator(high=df["High"], low=df["Low"], close=df["Close"], lbp=williams_lbp)
            df[f'wr_{williams_lbp}'] = wr.williams_r()
        return df

    @staticmethod
    def suggest(df, trial):
        params_dict = {"williams_lbp": trial.suggest_int("williams_lbp", 10, 200)}  # Adjust range as needed
        return WilliamsRTransformer.transform(df, **params_dict)

    @staticmethod
    def transform_or_suggest(df, trial=None, **kwargs):
        if trial:
            return WilliamsRTransformer.suggest(df, trial)
        else:
            return WilliamsRTransformer.transform(df, **kwargs)

