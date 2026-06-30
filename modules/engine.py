# [파일: engine.py]
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics.pairwise import euclidean_distances

class MatchAnalysisEngine:
    def __init__(self, schema):
        self.schema = schema
        self.model = GradientBoostingRegressor()
        self.historical_data = None

    def clean(self, df):
        for col, bounds in self.schema.items():
            df[col] = df[col].fillna(bounds['median'])
            outliers = (df[col] < bounds['min']) | (df[col] > bounds['max'])
            df.loc[outliers, col] = bounds['median']
        return df

    def train(self, X, y):
        self.historical_data = X
        self.model.fit(X, y)

    def get_analysis_brief(self, X_input):
        # 1. 예측
        pred = self.model.predict(X_input)
        
        # 2. 가장 유사한 과거 경기 찾기 (비교 분석)
        distances = euclidean_distances(X_input, self.historical_data)
        closest_idx = np.argmin(distances)
        
        # 3. 특성 중요도
        importance = pd.Series(self.model.feature_importances_, index=X_input.columns)
        
        return {
            "predicted_score": pred[0],
            "top_factors": importance.sort_values(ascending=False).head(3).to_dict(),
            "similar_match_idx": closest_idx,
            "confidence": "High" if pred[0] > 0.5 else "Moderate"
        }
