# [파일: main.py]
import pandas as pd
from config import SCHEMA
from engine import DataQualityManager, ProbabilisticModel, Backtester, PerformanceEvaluator

def run_analysis_engine(raw_data, target):
    # 1. 품질 관리
    dq = DataQualityManager(SCHEMA)
    clean_data = dq.validate(raw_data)
    
    # 2. 백테스팅
    backtester = Backtester(ProbabilisticModel)
    results = backtester.run_backtest(clean_data, target)
    
    # 3. 평가
    # 백테스팅 시점 이후의 실제 타겟 데이터와 비교
    evaluator = PerformanceEvaluator()
    metrics = evaluator.evaluate(target[5:], results)
    
    return results, metrics

if __name__ == "__main__":
    data = pd.DataFrame({
        'feature1': [10, 12, 15, 14, 20, 22, 25, 24, 30, 32, 35], 
        'feature2': [0.1, 0.12, 0.15, 0.14, 0.2, 0.22, 0.25, 0.24, 0.3, 0.32, 0.35]
    })
    target = [0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1]
    
    results, metrics = run_analysis_engine(data, target)
    print("예측 결과:", results)
    print("평가 지표:", metrics)
