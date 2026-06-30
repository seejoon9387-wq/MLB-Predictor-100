# [파일: engine.py]
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

class LocalAnalysisEngine:
    def __init__(self, schema):
        self.schema = schema
        self.model = None

    def clean(self, df):
        # 결정론적 데이터 품질 관리
        for col, bounds in self.schema.items():
            df[col] = df[col].fillna(bounds['median'])
            outliers = (df[col] < bounds['min']) | (df[col] > bounds['max'])
            df.loc[outliers, col] = bounds['median']
        return df

    def train(self, X, y):
        # 확률적 예측 (개인용으로는 앙상블보다 단일 모델의 튜닝이 효율적)
        self.model = GradientBoostingRegressor(loss='quantile', alpha=0.5)
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
