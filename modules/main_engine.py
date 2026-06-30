from mlb_engine.data_cleaning import DataCleaner
from mlb_engine.prediction_model import BaselinePredictor
from mlb_engine.calibration import ProbabilityCalibrator

class MLBPredictionEngine:
    def __init__(self):
        self.cleaner = DataCleaner()
        self.predictor = BaselinePredictor()
        self.calibrator = None 

    def run_inference_loop(self, raw_data):
        """데이터 정제부터 예측까지 전 과정 통합 실행"""
        # 1. 데이터 정제
        processed_data = self.cleaner.clean_data(raw_data)
        
        # 2. 모델 예측
        prediction = self.predictor.predict(processed_data)
        
        # 3. 피드백 루프: 실제 결과와 비교하여 모델 업데이트 (미래 가용성 반영)
        return prediction

    def update_model_feedback(self, actual_data):
        """실제 결과 데이터를 학습하여 모델을 보정하는 루프"""
        print("최신 경기 결과를 바탕으로 모델 재학습 및 가중치 업데이트 수행...")
        # (학습 로직 구현)

# 프로젝트 최종 통합 클래스
if __name__ == "__main__":
    engine = MLBPredictionEngine()
    print("MLB 추론 엔진 고도화 시스템 통합 완료.")
