# [파일: engine.py]
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import mean_squared_error

# 모듈 1: 데이터 품질 관리
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

# 모듈 2: 드리프트 감지 모듈 (추가됨)
class DriftDetector:
    def __init__(self, threshold=0.05):
        self.threshold = threshold
    def detect(self, reference_data, current_data):
        # K-S 검정을 통해 두 데이터의 분포 차이 계산
        drift_report = {}
        for col in reference_data.columns:
            stat, p_value = ks_2samp(reference_data[col], current_data[col])
            drift_report[col] = p_value < self.threshold
        return drift_report

# 모듈 3: 확률적 모델
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

# 모듈 4: 평가 모듈
class PerformanceEvaluator:
    @staticmethod
    def evaluate(y_true, y_pred):
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        return {"RMSE": rmse}

# 모듈 5: 백테스팅 엔진
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
