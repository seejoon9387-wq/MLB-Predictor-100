# [파일: engine.py]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
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

    def save_analysis_report(self, brief, importance_series):
        # 1. 시각화: 특성 중요도 차트 저장
        plt.figure(figsize=(8, 4))
        importance_series.plot(kind='barh', color='skyblue')
        plt.title('Analysis Key Factors')
        plt.savefig(f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.png")
        plt.close()
        
        # 2. 로그 기록: 분석 결과 텍스트 파일 저장
        with open("analysis_log.txt", "a") as f:
            f.write(f"\n--- {datetime.datetime.now()} ---\n")
            f.write(f"Result: {brief['predicted_score']:.2f}, Similar Index: {brief['similar_match_idx']}\n")

    def get_analysis_brief(self, X_input):
        pred = self.model.predict(X_input)
        distances = euclidean_distances(X_input, self.historical_data)
        closest_idx = np.argmin(distances)
        importance = pd.Series(self.model.feature_importances_, index=X_input.columns)
        
        brief = {
            "predicted_score": pred[0],
            "top_factors": importance.sort_values(ascending=False).head(3),
            "similar_match_idx": closest_idx,
            "confidence": "High" if pred[0] > 0.5 else "Moderate"
        }
        self.save_analysis_report(brief, brief['top_factors'])
        return brief
