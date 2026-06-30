# [파일: main.py]
import pandas as pd
from config import SCHEMA
from engine import DataQualityManager, ProbabilisticModel, ProbabilityCalibrator

def run_analysis_engine(raw_data, y_train):
    # 1. 데이터 품질 관리
    dq = DataQualityManager(SCHEMA)
    clean_data = dq.validate(raw_data)
    
    # 2. 모델 학습
    model = ProbabilisticModel()
    model.fit(clean_data, y_train)
    
    # 3. 예측 및 보정
    preds = model.predict(clean_data)
    calibrator = ProbabilityCalibrator()
    calibrator.fit(preds['median'], y_train)
    calibrated_result = calibrator.calibrate(preds['median'])
    
    return preds, calibrated_result

# 예시 실행 코드
if __name__ == "__main__":
    # 샘플 데이터 생성
    data = pd.DataFrame({'feature1': [10, 200, 50], 'feature2': [0.1, 0.9, 0.5]})
    target = [0, 1, 0]
    
    preds, final_res = run_analysis_engine(data, target)
    print("예측 완료:", preds['median'])
