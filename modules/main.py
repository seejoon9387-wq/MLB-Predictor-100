# [파일: main.py]
import pandas as pd
from config import SCHEMA
from engine import DataQualityManager, ProbabilisticModel, Backtester, PerformanceEvaluator, DriftDetector

def run_analysis_engine(ref_data, current_data, target):
    # 1. 드리프트 체크
    drift_detector = DriftDetector()
    drift_status = drift_detector.detect(ref_data, current_data)
    
    # 2. 품질 관리
    dq = DataQualityManager(SCHEMA)
    clean_data = dq.validate(current_data)
    
    # 3. 백테스팅
    backtester = Backtester(ProbabilisticModel)
    results = backtester.run_backtest(clean_data, target)
    
    return results, drift_status

if __name__ == "__main__":
    ref_data = pd.DataFrame({'feature1': [10, 12, 15, 14, 20], 'feature2': [0.1, 0.12, 0.15, 0.14, 0.2]})
    current_data = pd.DataFrame({'feature1': [22, 25, 24, 30, 32], 'feature2': [0.22, 0.25, 0.24, 0.3, 0.32]})
    target = [1, 1, 0, 1, 1]
    
    results, drift = run_analysis_engine(ref_data, current_data, target)
    print("드리프트 감지 결과:", drift)
    print("분석 결과:", results)
