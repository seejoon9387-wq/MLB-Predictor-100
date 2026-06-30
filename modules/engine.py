# [파일: engine.py]
import numpy as np
import pandas as pd
import optuna
from scipy.stats import ks_2samp
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

class DataQualityManager:
    def __init__(self, schema):
        self.schema = schema
    def validate(self, df):
        for col, bounds in self.schema.items():
            df[col] = df[col].fillna(bounds['median'])
            outliers = (df[col] < bounds['min']) | (df[col] > bounds['max'])
            df.loc[outliers, col] = bounds['median']
        return df

# 모듈 6: 베이지안 최적화 엔진 (추가됨)
class BayesianOptimizer:
    def __init__(self, X, y):
        self.X, self.y = X, y
    def objective(self, trial):
        lr = trial.suggest_float("learning_rate", 0.01, 0.3, log=True)
        n_estimators = trial.suggest_int("n_estimators", 50, 300)
        model = GradientBoostingRegressor(learning_rate=lr, n_estimators=n_estimators)
        model.fit(self.X, self.y)
        preds = model.predict(self.X)
        return np.sqrt(mean_squared_error(self.y, preds))
    
    def optimize(self):
        study = optuna.create_study(direction="minimize")
        study.optimize(self.objective, n_trials=20)
        return study.best_params

class ProbabilisticModel:
    def __init__(self, params=None):
        self.params = params or {}
        self.models = {
            'lower': GradientBoostingRegressor(loss='quantile', alpha=0.1, **self.params),
            'median': GradientBoostingRegressor(loss='quantile', alpha=0.5, **self.params),
            'upper': GradientBoostingRegressor(loss='quantile', alpha=0.9, **self.params)
        }
    def fit(self, X, y):
        for name, model in self.models.items():
            model.fit(X, y)
    def predict(self, X):
        return {name: model.predict(X) for name, model in self.models.items()}
