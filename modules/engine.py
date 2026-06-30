# [파일: engine.py]
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

class MatchAnalysisEngine:
    def __init__(self, schema):
        self.schema = schema
        self.model = GradientBoostingRegressor()

    def clean(self, df):
        for col, bounds in self.schema.items():
            df[col] = df[col].fillna(bounds['median'])
            outliers = (df[col] < bounds['min']) | (df[col] > bounds['max'])
            df.loc[outliers, col] = bounds['median']
        return df

    def train(self, X, y):
        self.model.fit(X, y)

    def get_analysis_brief(self, X_input):
        # 예측 수행
        pred = self.model.predict(X_input)
        
        # 특성 중요도(Feature Importance) 추출 - 브리핑의 핵심 근거
        importance = pd.Series(self.model.feature_importances_, index=X_input.columns)
        top_factors = importance.sort_values(ascending=False).head(3)
        
        return {
            "predicted_score": pred[0],
            "top_factors": top_factors.to_dict(),
            "confidence": "High" if pred[0] > 0.5 else "Moderate"
        }
