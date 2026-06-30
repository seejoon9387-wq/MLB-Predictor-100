# [파일: engine.py]
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.isotonic import IsotonicRegression

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

class ProbabilityCalibrator:
    def __init__(self):
        self.calibrator = IsotonicRegression(out_of_bounds='clip')
    def fit(self, y_prob, y_true):
        self.calibrator.fit(y_prob, y_true)
    def calibrate(self, y_prob):
        return self.calibrator.transform(y_prob)
