import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso

class EnvironmentWeightOptimizer:
    def __init__(self):
        # L1 규제(Lasso)를 사용하여 중요하지 않은 변수의 가중치를 0으로 만듦
        self.model = Lasso(alpha=0.01)

    def calculate_weights(self, X, y):
        """
        환경 변수(X)가 성적(y)에 미치는 영향력(가중치)을 산출합니다.
        """
        self.model.fit(X, y)
        weights = dict(zip(X.columns, self.model.coef_))
        return weights

    def apply_weights(self, X, weights):
        """산출된 가중치를 기반으로 최종 환경 보정 지수를 산출합니다."""
        weighted_score = sum(X[col] * weights.get(col, 0) for col in X.columns)
        return weighted_score

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    # 환경 변수 데이터 및 타겟 성적(성적 향상분) 가정
    X = pd.DataFrame({
        'park_factor': [1.1, 1.0, 0.9],
        'temp_dev': [5, 0, -5],
        'pitcher_hand_val': [0, 1, 0]
    })
    y = np.array([0.05, 0.0, -0.04])
    
    optimizer = EnvironmentWeightOptimizer()
    weights = optimizer.calculate_weights(X, y)
    
    print("환경 변수별 산출된 가중치:")
    print(weights)
