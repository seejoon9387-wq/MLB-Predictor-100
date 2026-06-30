import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

class PerformanceEvaluator:
    def __init__(self, initial_capital=1000):
        self.initial_capital = initial_capital

    def evaluate_metrics(self, y_true, y_pred):
        """통계적 오차 지표 산출"""
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        return {'MAE': mae, 'RMSE': rmse}

    def calculate_roi(self, y_true, y_pred, threshold=0.05):
        """
        예측 기반 의사결정의 ROI 계산
        단순화: 예측값이 실제보다 높으면 베팅 성공, 낮으면 실패로 가정
        """
        success = np.where(y_pred >= y_true, 1, -1)
        roi = (np.sum(success) / len(success)) * 100
        return roi

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    y_true = np.array([0.700, 0.850, 0.600])
    y_pred = np.array([0.720, 0.820, 0.650])
    
    evaluator = PerformanceEvaluator()
    metrics = evaluator.evaluate_metrics(y_true, y_pred)
    roi = evaluator.calculate_roi(y_true, y_pred)
    
    print(f"통계적 평가 지표: {metrics}")
    print(f"시뮬레이션 기반 기대 ROI: {roi:.2f}%")
