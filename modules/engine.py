# [파일: engine.py]
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import mean_squared_error

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

# 모듈 3: 평가 모듈 (추가됨)
class PerformanceEvaluator:
    @staticmethod
    def evaluate(y_true, y_pred):
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        # 예측값과 실제값의 차이 분포를 통한 단순 신뢰도 지표 계산
        calibration_score = np.mean(np.abs(np.array(y_true) - np.array(y_pred)))
        return {"RMSE": rmse, "Calibration_Error": calibration_score}

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
