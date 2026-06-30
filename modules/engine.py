# [파일: engine.py]
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.isotonic import IsotonicRegression

# 모듈 1: 결정론적 데이터 품질 관리
class DataQualityManager:
    def __init__(self, schema):
        self.schema = schema
    def validate(self, df):
        if set(df.columns) != set(self.schema.keys()):
            raise ValueError("스키마 불일치")
        for col, bounds in self.schema.items():
            df[col] = df[col].fillna(bounds['median'])
            outliers = (df[col] < bounds['min']) | (df[col] > bounds['max'])
            df.loc[outliers, col] = bounds['median']
        return df

# 모듈 2: 확률적 예측 모델
class ProbabilisticModel:
    def __init__(self):
        self.models = {
            'lower': GradientBoostingRegressor(loss='quantile', alpha=0.1),
            'median': GradientBoostingRegressor(loss='quantile', alpha=0.5),
            'upper': GradientBoostingRegressor(loss='quantile', alpha=0.9)
        }
    def fit(self, X, y):
        for name, model in self.models.items():
            model.fit(X, y)
    def predict(self, X):
        return {name: model.predict(X) for name, model in self.models.items()}

# 모듈 3: 확률 보정 (Calibration)
class ProbabilityCalibrator:
    def __init__(self):
        self.calibrator = IsotonicRegression(out_of_bounds='clip')
    def fit(self, y_prob, y_true):
        self.calibrator.fit(y_prob, y_true)
    def calibrate(self, y_prob):
        return self.calibrator.transform(y_prob)

# 모듈 4: 확장 윈도우 백테스팅 엔진
class Backtester:
    def __init__(self, model_class):
        self.model_class = model_class
    def run_backtest(self, X, y, window_size=5):
        results = []
        for i in range(window_size, len(X)):
            train_X, train_y = X.iloc[:i], y[:i]
            test_X = X.iloc[i:i+1]
            model = self.model_class()
            model.fit(train_X, train_y)
            pred = model.predict(test_X)
            results.append(pred['median'][0])
        return results
