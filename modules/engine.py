# [파일: main.py]
import pandas as pd
from config import SCHEMA
from engine import DataQualityManager, BayesianOptimizer, ProbabilisticModel

def run_optimized_engine(raw_data, target):
    # 1. 데이터 정제
    dq = DataQualityManager(SCHEMA)
    clean_data = dq.validate(raw_data)
    
    # 2. 베이지안 최적화 실행
    optimizer = BayesianOptimizer(clean_data, target)
    best_params = optimizer.optimize()
    print("최적화된 파라미터:", best_params)
    
    # 3. 최적 파라미터로 모델 학습
    model = ProbabilisticModel(params=best_params)
    model.fit(clean_data, target)
    return model.predict(clean_data)

if __name__ == "__main__":
    data = pd.DataFrame({
        'feature1': [10, 12, 15, 14, 20, 22, 25, 24, 30, 32, 35], 
        'feature2': [0.1, 0.12, 0.15, 0.14, 0.2, 0.22, 0.25, 0.24, 0.3, 0.32, 0.35]
    })
    target = [0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1]
    
    results = run_optimized_engine(data, target)
    print("예측 결과 (Median):", results['median'])
