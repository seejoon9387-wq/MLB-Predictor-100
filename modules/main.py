# [파일: main.py]
import pandas as pd
from config import SCHEMA
from engine import LocalAnalysisEngine

def main():
    # 1. 데이터 준비
    raw_data = pd.DataFrame({
        'feature1': [10, 200, 50, 30], 
        'feature2': [0.1, 0.9, 0.5, 0.2]
    })
    target = [0, 1, 0, 1]
    
    # 2. 엔진 초기화 및 정제
    engine = LocalAnalysisEngine(SCHEMA)
    clean_data = engine.clean(raw_data)
    
    # 3. 학습 및 예측
    engine.train(clean_data, target)
    prediction = engine.predict(clean_data)
    
    print("예측 결과:", prediction)

if __name__ == "__main__":
    main()
