import xgboost as xgb
from sklearn.metrics import mean_absolute_error
import numpy as np

class BaselinePredictor:
    def __init__(self):
        # 예측 성능의 기준이 될 XGBoost 회귀 모델
        self.model = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5
        )

    def train_model(self, X_train, y_train):
        """모델 학습 수행"""
        self.model.fit(X_train, y_train)
        print("모델 학습 완료.")

    def predict(self, X_test):
        """성적 예측 수행"""
        return self.model.predict(X_test)

    def evaluate(self, X_test, y_test):
        """성능 지표(MAE) 측정"""
        predictions = self.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        return mae

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    # 학습용 가상 데이터 생성 (피처 4개, 타겟 1개)
    X_train = np.random.rand(100, 4)
    y_train = np.random.rand(100)
    
    predictor = BaselinePredictor()
    predictor.train_model(X_train, y_train)
    
    # 평가
    mae = predictor.evaluate(X_train, y_train)
    print(f"모델 베이스라인 MAE: {mae:.4f}")
